import sqlalchemy
import pandas as pd

from bannerman.data import connect_to_db
from bannerman.reports import build_last_five_iterations_report

query = """
select	
	task.Name as TaskName,
	case project.Name 
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	else project.Name end as ProjectName,
	story.Name as StoryName,
	iteration.Name as IterationName,
	user.DisplayName,
	user.EmailAddress,
	task.Actuals as TaskActuals_hrs,
	task.Estimate as TaskEstimate_hrs,
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
	'Workspace.Users' as user
on
	task.OwnerId = user.Id
left join
    'Projects.Iterations' iteration
on
    story.IterationId = iteration.Id
where
	task.State = 'Completed'
and
    task.Estimate > 0
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
"""

def build_tts_estimate_v_actual_report():
    """Builds reporting dataframe to provide details on task hours to story points."""
    df = pd.read_sql_query(
            sql=query,
            con=connect_to_db()
        )

    #last_5_df = build_last_five_iterations_report()

    #df = df.merge(last_5_df, on='IterationName', how='inner')
    df.drop(['IterationName'], axis=1,
            inplace=True)

    df.columns = [
        'TaskName',
        'ProjectName',
        'StoryName',
        'EmployeeName',
        'EmployeeEmail',
        'TaskActuals_hrs',
        'TaskEstimate_hrs',
        'StoryEstimate_pts'
    ]

    tts_df = df.copy().groupby(
        ['ProjectName', 'StoryName']
    ).sum().reset_index().drop(['StoryEstimate_pts'], axis=1)

    join_table = df[df['StoryEstimate_pts'] > 0].copy().drop(
            ['TaskName', 'EmployeeName', 'EmployeeEmail', 'TaskActuals_hrs', 'TaskEstimate_hrs'],
            axis=1
        ).drop_duplicates().reset_index()

    tts_df = tts_df.merge(join_table, on=['ProjectName', 'StoryName'])
    tts_df.drop('index', axis=1, inplace=True)

    tts_df['ActualVsEstimatePercentDiff'] = (tts_df['TaskActuals_hrs'] - tts_df['TaskEstimate_hrs'])/tts_df['TaskEstimate_hrs']
    tts_df['EstimatedHoursPerPoint'] = tts_df['TaskEstimate_hrs']/tts_df['StoryEstimate_pts']
    tts_df['ActualHoursPerPoint'] = tts_df['TaskActuals_hrs']/tts_df['StoryEstimate_pts']

    return tts_df

if __name__ == '__main__':
    report_df = build_tts_estimate_v_actual_report().groupby('ProjectName').mean().round(2).reset_index()
    df_out = report_df[
        [
            'ProjectName',
            'ActualVsEstimatePercentDiff',
            'EstimatedHoursPerPoint',
            'ActualHoursPerPoint'
        ]
    ].round(
        {
            'ActualVsEstimatePercentDiff' : 4,
            'EstimatedHoursPerPoint' : 2,
            'ActualHoursPerPoint' : 2
        }
    )
    df_out.columns = [
            'ProjectName',
            'MeanActualVsEstimatePercentDiff',
            'MeanEstimatedHoursPerPoint',
            'MeanActualHoursPerPoint'
        ]
    df_out.to_csv(path_or_buf='task_to_story_averages.csv', sep=',')
