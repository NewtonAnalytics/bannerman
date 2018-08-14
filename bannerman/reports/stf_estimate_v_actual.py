import sqlalchemy
import pandas as pd

from bannerman.data import connect_to_db


query = """
select	
	function.Name as FunctionName,
	case project.Name
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	else project.Name end AS ProjectName,
	story.Name AS StoryName,
	CAST(function.PreliminaryEstimate as int) as FunctionPrelimEstimate_pts,
	SUM(task.Actuals) as StoryActuals_hrs,
    SUM(task.Estimate) as StoryEstimateByTask_hrs,
    story.PlanEstimate as StoryEstimate_pts
from
	'Projects.Tasks' as task
left join
	'Projects.Stories' as story
on
	task.StoryId = story.Id
left join
	'Workspace.Projects' as project
on
	task.ProjectId = project.Id
left join
	'Projects.Functions' function
on
	story.FunctionId = function.Id
left join
    'Projects.Iterations' iteration
on
    story.IterationId = iteration.Id
where
	task.State = 'Completed'
and
	function.Name is not null
and
    function.ActualEndDate is not null
and
    story.PlanEstimate > 0
and
    story.ScheduleState = 'Accepted'
and
    (
        (
        project.Name = 'Market Data Connection'
        and
        iteration.Name IN ('Iteration 2018.01', 'Iteration 2018.02', 'Iteration 2018.03', 'Iteration 2018.04', 'Iteration 2018.05', 'Iteration 2018.06')
        )
        or
        (
        project.Name IN ('Bantha Rodeo', 'SUN::FunTrust', 'Stormtrooper Accuracy')
        and
        iteration.Name IN ('Iteration 15', 'Iteration 16', 'Iteration 17', 'Iteration 18', 'Iteration 19', 'Iteration 20', 'Iteration 21')
        )
    )
group by
	function.Name,
	project.Name,
	function.PreliminaryEstimate,
	story.Name,
	story.PlanEstimate
having
    sum(task.Actuals) > 0 and sum(task.Estimate) > 0
"""

def build_stf_estimate_v_actual_report():
    df = pd.read_sql_query(
                sql=query,
                con=connect_to_db()
            )

    stf_df = df.copy().groupby(['ProjectName', 'FunctionName']).sum().reset_index().drop(
        ['FunctionPrelimEstimate_pts'], axis=1
    )

    join_table = df[df['FunctionPrelimEstimate_pts'] > 0].copy()
    join_table = join_table.drop(
            ['StoryName','StoryActuals_hrs', 'StoryEstimateByTask_hrs', 'StoryEstimate_pts'],
            axis=1
        ).drop_duplicates().reset_index().drop('index', axis=1)

    stf_df = stf_df.merge(join_table, on=['ProjectName', 'FunctionName'])

    stf_df['PercentDiffStoriesToFunction'] = (stf_df['StoryEstimate_pts'] - stf_df['FunctionPrelimEstimate_pts'])/stf_df['FunctionPrelimEstimate_pts']
    stf_df['ActualVsEstimateTasksPercentDiff'] = (stf_df['StoryActuals_hrs'] - stf_df['StoryEstimateByTask_hrs'])/stf_df['StoryEstimateByTask_hrs']
    stf_df['TaskActualHoursPerStoryEstimate'] = stf_df['StoryActuals_hrs']/stf_df['StoryEstimate_pts']
    stf_df['TaskEstimatedHoursPerStoryEstimate'] = stf_df['StoryEstimateByTask_hrs']/stf_df['StoryEstimate_pts']
    stf_df['TaskActualHoursPerFunctionPrelimEstimate'] = stf_df['StoryActuals_hrs']/stf_df['FunctionPrelimEstimate_pts']
    stf_df['TaskEstimatedHoursPerFunctionPrelimEstimate'] = stf_df['StoryEstimateByTask_hrs']/stf_df['FunctionPrelimEstimate_pts']

    stf_df.columns = [
        'ProjectName',
        'FunctionName',
        'TotalStoryActualHours',
        'TotalStoryEstimatedHours',
        'TotalStoryPoints',
        'FunctionPrelimEstimate',
        'PercentDiffStoriesToFunction',
        'ActualVsEstimateTaskHours',
        'ActualHoursPerStoryPoint',
        'EstimatedHoursPerStoryPoint',
        'ActualHoursPerFunctionPoint',
        'EstimatedHoursPerFunctionPoint'
    ]

    return stf_df

if __name__ == '__main__':
    report_df = build_stf_estimate_v_actual_report().groupby('ProjectName').mean().reset_index()
    df_out = report_df[
        [
            'ProjectName',
            'PercentDiffStoriesToFunction',
            'ActualHoursPerFunctionPoint'
        ]
    ].round(
        {
            'PercentDiffStoriesToFunction' : 4,
            'ActualHoursPerFunctionPoint' : 2,
        }
    )
    df_out.to_csv(path_or_buf='story_to_function_averages.csv', sep=',', index_label='Project')