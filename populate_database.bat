call workon bannerman
pause
cd bannerman
python db_manager.py dropdb
python db_manager.py initdb
python db_manager.py extract_workspace_items
python db_manager.py extract_project_items -rc config/mdc.cfg
python db_manager.py extract_project_items -rc config/tsquare.cfg
python db_manager.py extract_project_items -rc config/seurat.cfg
python db_manager.py extract_project_items -rc config/compliance_workbench.cfg
python db_manager.py extract_project_items -rc config/theq.cfg
python db_manager.py extract_project_items -rc config/suntrust.cfg
python db_manager.py extract_project_items -rc config/suntrust2.cfg
python db_manager.py extract_project_items -rc config/suntrust3.cfg
pause