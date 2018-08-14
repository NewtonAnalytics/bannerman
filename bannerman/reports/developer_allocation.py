import pandas as pd
import numpy as np

from bannerman.data import connect_to_db
from bannerman.reports import build_last_five_iterations_report

query = """
select
	case project.Name 
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	else project.Name end as ProjectName,
	iteration.Name as IterationName,
	user.DisplayName as StoryOwner,
	user.Role as OwnerRole,
	sum(story.PlanEstimate) as TotalStoryPoints
from
	'Projects.Stories' story
left join
	'Projects.Iterations' iteration
on
	story.IterationId = iteration.Id
inner join
	'Workspace.Users' user
on
	story.OwnerId = user.Id
inner join
	'Workspace.Projects' project
on
	story.ProjectId = project.Id
where
	story.PlanEstimate > 0
and
	story.Name not like '%defect%'
and
	story.Name not like '%Defect%'
group by
	case project.Name 
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	else project.Name end,
	user.DisplayName,
	iteration.Name,
	user.Role
"""

def build_developer_allocation_report():
    df = pd.read_sql_query(
        sql=query,
        con=connect_to_db()
    )

    last_5_df = build_last_five_iterations_report()
    last_iteration_df = last_5_df[last_5_df.Recency == 0]

    alloc_df = df.merge(last_iteration_df, how='inner', on=['IterationName', 'ProjectName'])

    """
    start_date_df = alloc_df[['StoryOwner', 'IterationStartDate']].groupby('StoryOwner').min().reset_index()
    start_date_df.columns = ['StoryOwner', 'EarliestDate']

    end_date_df = alloc_df[['StoryOwner', 'IterationEndDate']].groupby('StoryOwner').max().reset_index()
    end_date_df.columns = ['StoryOwner', 'LatestDate']

    time_dilation_df = start_date_df.merge(end_date_df, on='StoryOwner', how='inner')
    time_dilation_df['EarliestDate'] = pd.to_datetime(time_dilation_df['EarliestDate'])
    time_dilation_df['LatestDate'] = pd.to_datetime(time_dilation_df['LatestDate'])

    time_dilation_df['developer_timespan'] = time_dilation_df.apply(
        lambda row : np.busday_count(row['EarliestDate'], row['LatestDate']), axis=1
    )

    time_dilation_df.drop(['EarliestDate', 'LatestDate'], axis=1, inplace=True)
    
    report_df = alloc_df.merge(time_dilation_df, on='StoryOwner').drop(['Recency'], axis=1)
    """
    report_df = alloc_df.copy().drop('Recency', axis=1)
    report_df['IterationStartDate'] = pd.to_datetime(report_df['IterationStartDate'])
    report_df['IterationEndDate'] = pd.to_datetime(report_df['IterationEndDate'])
    report_df['iteration_timespan'] = report_df.apply(
        lambda row: np.busday_count(row['IterationStartDate'], row['IterationEndDate']), axis=1
    )

    report_df['allocation_by_project'] = report_df['TotalStoryPoints']/report_df['iteration_timespan']
    #report_df['allocation_over_timeframe'] = report_df['TotalStoryPoints']/report_df['developer_timespan']

    totals_df = report_df.drop(
        ['TotalStoryPoints', 'iteration_timespan'], axis=1
    ).groupby('StoryOwner').sum().reset_index()
    totals_df.columns = ['StoryOwner', 'TotalAllocation']

    report_df = report_df.merge(totals_df, on='StoryOwner', how='inner')
    report_df['ProjectAllocationNormalized'] = report_df['allocation_by_project']/report_df['TotalAllocation']
    report_df.drop(['IterationName', 'IterationStartDate', 'IterationEndDate',
                    'iteration_timespan', 'TotalAllocation'], axis=1, inplace=True)

    report_df.columns = ['ProjectName', 'Employee', 'EmployeeRole', 'TotalStoryPoints',
                       '5PtsPerWeekAllocation', 'NormalizedAllocation']

    return report_df.sort_values(by='Employee')

if __name__ == '__main__':
    print(build_developer_allocation_report())