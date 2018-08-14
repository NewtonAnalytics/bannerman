from bannerman.banner import db
from bannerman.data import connect_to_rally
from bannerman.data.get_rally_item_set import get_rally_item_set

def populate_db(config_file='', item_set=''):
    rally_api_connection = connect_to_rally(['--rallyConfig=' + config_file])
    """
    with Pool(len(df_get.index)) as p:
        p.starmap(
            get_rally_item_set,
            rally_items
        )
    """
    for rally_item in item_set:
        print(
            'Extracting data for the configuration: \n'
              '\t{}\n'
              '\t{}'.format(config_file, rally_item)
        )
        get_rally_item_set(rally_item=rally_item, connection=rally_api_connection)
    db.session.commit()
