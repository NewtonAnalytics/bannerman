import sqlalchemy
import pandas as pd
import nltk
from nltk.stem.snowball import SnowballStemmer

from bannerman.data import connect_to_db
from bannerman.reports.experimental.penn_treebank_tags import pb_tags

query = """
select
	case project.Name 
	when 'Stormtrooper Accuracy' then 'SUN::FunTrust'
	when 'Bantha Rodeo' then 'SUN::FunTrust'
	else project.Name end as ProjectName,
	story.Name as StoryName,
	user.EmailAddress as StoryOwner,
	user.Role as OwnerRole,
	story.PlanEstimate,
	case defect.Severity
	when 'Major Problem' then 2
	when 'Minor Problem' then 1
	else 0 end as SeverityAdjustment,
	SUM(case when ifnull(defect.ShortName, 0) = 0 then 0
	else 1 end) as NumberOfDefects
from
	'Projects.Stories' story
left join
	'Projects.Defects' defect
on
	defect.StoryId = story.Id
inner join
	'Workspace.Users' user
on
	story.OwnerId = user.Id
inner join
	'Workspace.Projects' project
on
	story.ProjectId = project.Id
where
	story.ScheduleState in ('Accepted', 'Completed')
and
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
	story.Name,
	user.EmailAddress,
	user.Role,
	story.PlanEstimate,
	case defect.Severity
	when 'Major Problem' then 2
	when 'Minor Problem' then 1
	else 0 end"""

def build_developer_affinity_report():
    stories_df = pd.read_sql_query(
            sql=query,
            con=connect_to_db()
        )

    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

    stemmer = SnowballStemmer("english")
    lemmatizer = nltk.stem.WordNetLemmatizer()

    stories_df['tagged_tokens'] = stories_df.apply(
        lambda row: nltk.pos_tag(
             [lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(row['StoryName'])]
        ), axis=1
    )

    s = stories_df.apply(lambda x : pd.Series(x['tagged_tokens']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'tagged_token'

    stories_df = stories_df.drop('tagged_tokens', axis=1).join(s)

    stories_df[['token', 'token_tag']] = stories_df['tagged_token'].apply(pd.Series)
    stories_df = stories_df.merge(pb_tags, how='left', left_on='token_tag', right_on='tag').drop('tag', axis=1)
    stories_df['rel1'] = stories_df['description'].str.contains('noun')
    stories_df['rel2'] = stories_df['description'].str.contains('verb')

    relevant_tags_df = stories_df[(stories_df['rel1']) | (stories_df['rel2'])].drop_duplicates()
    affinity_df = relevant_tags_df.groupby(['StoryOwner', 'token']).sum().reset_index().sort_values(
        by=['StoryOwner','PlanEstimate'], ascending=False).reset_index()
    top_five_affinities = affinity_df.groupby('StoryOwner').cumcount()
    top_five_affinities.name = 'affinity_rank'

    affinity_df = affinity_df.join(top_five_affinities)

    return affinity_df[(affinity_df.affinity_rank < 5)]


if __name__ == '__main__':
    report_df = build_developer_affinity_report()
    print(report_df)
