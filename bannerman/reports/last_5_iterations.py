import sqlalchemy
import pandas as pd
import dateutil

from bannerman.data import connect_to_db

query = """
select
	case project.Name
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	else project.Name end AS ProjectName,
	iteration.Name  as IterationName,
	DATETIME(iteration.StartDate) AS IterationStartDate,
	DATETIME(iteration.EndDate) as IterationEndDate
from
	'Projects.Iterations' iteration
inner join
	'Workspace.Projects' project
on
	iteration.ProjectId = project.Id
where
    iteration.EndDate < date('now')
"""

def build_last_five_iterations_report():
    iteration_df = pd.read_sql_query(
            sql=query,
            con=connect_to_db()
        )

    iteration_df = iteration_df.sort_values(
        ['ProjectName','IterationStartDate'], ascending=False).reset_index()
    iteration_df.drop('index', inplace=True, axis=1)
    iteration_df = iteration_df.drop_duplicates()

    rolling_count = iteration_df.groupby(['ProjectName']).cumcount()
    rolling_count.name = 'RollCount'
    iteration_df = iteration_df.join(rolling_count)
    last_5_df = iteration_df[iteration_df['RollCount'] < 7].reset_index().drop('index', axis=1)
    last_5_df.columns = ['ProjectName', 'IterationName', 'IterationStartDate', 'IterationEndDate', 'Recency']

    last_5_df['IterationStartDate'] = last_5_df.apply(
        lambda row: dateutil.parser.parse(row['IterationStartDate']), axis=1
    )
    last_5_df['IterationEndDate'] = last_5_df.apply(
        lambda row: dateutil.parser.parse(row['IterationEndDate']), axis=1
    )

    last_5_df['IterationStartDate'] = pd.to_datetime(last_5_df['IterationStartDate'])
    last_5_df['IterationEndDate'] = pd.to_datetime(last_5_df['IterationEndDate'])

    return last_5_df

if __name__ == '__main__':
    print(build_last_five_iterations_report())