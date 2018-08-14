import sqlalchemy
import pandas as pd

from bannerman.data import connect_to_db
from bannerman.reports import build_last_five_iterations_report

query = """
select
	case project.Name
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	else project.Name end AS ProjectName,
	iteration.Name  as IterationName,
	DATETIME(iteration.StartDate) AS IterationStartDate,
	DATETIME(iteration.EndDate) as IterationEndDate,
	defect.Name  as DefectName,
	case when 
	defect.Severity = 'Major Problem' then 2 
	else case when defect.severity = 'Minor Problem' then 1
	else case when defect.Name is not null then 0
	end end end as DefectSeverity,
	ifnull(defect.DefectState, 'Not Indicated') as DefectState,
	ifnull(defect.Environment, 'Not Indicated') as Environment
from
	'Projects.Iterations' iteration
left join
	'Projects.Defects' defect
on
	defect.IterationId = iteration.Id
inner join
	'Workspace.Projects' project
on
	iteration.ProjectId = project.Id
where
    iteration.EndDate < date('now')
"""

def build_in_flight_defects_report():
    defect_df = pd.read_sql_query(
            sql=query,
            con=connect_to_db()
        )

    def_df = defect_df[['ProjectName', 'IterationName', 'IterationStartDate', 'Environment', 'DefectState']].sort_values(
        ['ProjectName','IterationStartDate'], ascending=False).reset_index()
    def_df.drop('index', inplace=True, axis=1)
    def_df = def_df.drop_duplicates()

    last_5_df = build_last_five_iterations_report()

    defects_in_iter = defect_df.groupby(
        ['ProjectName', 'IterationName', 'Environment', 'DefectState']
    ).count().reset_index().drop(['IterationStartDate', 'IterationEndDate', 'DefectName'], axis=1)
    defects_in_iter.columns = ['ProjectName', 'IterationName', 'Environment', 'DefectState', 'NumberOfDefects']

    """
    if_def_report = defect_df[defect_df.DefectName != None].groupby(['ProjectName', 'DefectSeverity']).count().drop(
        ['IterationName', 'IterationStartDate', 'IterationEndDate'], axis=1
        )
    """
    defect_report = last_5_df.merge(
        defects_in_iter, how='left', on=['ProjectName', 'IterationName']
    ).fillna(value=0).drop('Recency', axis=1)

    return defect_report

if __name__ == '__main__':
    report_df = build_in_flight_defects_report().groupby(
        ['ProjectName', 'Environment', 'DefectState']
    ).sum().reset_index()
    report_df = report_df[(report_df['DefectState'] != 'Not Indicated') | (report_df['Environment'] != 'Not Indicated')]
    report_df.to_csv(path_or_buf='in_flight_defects.csv', sep=',', index=False)