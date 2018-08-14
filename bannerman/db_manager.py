import pandas as pd
from bannerman.banner import app, db
from flask_script import Manager, prompt_bool
from bannerman.data import populate_db

manager = Manager(app)

#This dictionary defines what objects will be collected and loaded into the database. "Project Items" are those items
#that differ from project-to-project, whilst "Workspace Items" are those items defined at the workspace level. These are
#run separately to ensure uniqueness of database entries. Hardening of this feature may be required in future iterations.
items_to_collect = {
    "Project Items" : [
        "Function",
        "Feature",
        "Capability",
        "Iteration",
        "Task",
        "Story",
        "Defect",
        "Release",
        "TestCase",
        "TestFolder"
    ],
    'Workspace Items' : [
        "Project",
        "User",
        "State"
        ]
}

#This command initializes bannerman.db with the schema defined within bannerman.entities.models.
@manager.command
def initdb():
    db.create_all()
    print('Initialized the database.')

#This command drops the pre-existing database, allowing for a full refresh.
@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to drop the database?"
    ):
        db.drop_all()
        print('Dropped the database.')

#This command will extract "Project Items" for the project within the configuration file that's passed on the command
#line. Then, it will populate bannerman.db with the extracted data. Config files reside in bannerman/config.
@manager.option('--rallyConfig', '-rc', dest='config_file')
def extract_project_items(config_file):
    print('Collecting Project Items and populating bannerman.db using {}...'.format(config_file))
    populate_db(config_file=config_file, item_set=items_to_collect['Project Items'])
    print('Project Items populated for {}.'.format(config_file))

#This command will extract "Workspace Items", then populate bannerman.db with the extracted data.
@manager.command
def extract_workspace_items():
    print('Collecting Workspace Items and populating bannerman.db.')
    populate_db(config_file='config/mdc.cfg', item_set=items_to_collect['Workspace Items'])
    print('Workspace Items populated.')

if __name__ == '__main__':
    manager.run()