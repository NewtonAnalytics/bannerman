from pyral.entity import UnreferenceableOIDError
from pyral.rallyresp import RallyResponseError
from bannerman.data.set_item_type import set_item_type
from bannerman.data.get_object_ids import get_object_ids
from bannerman.data.add_to_db import add_to_db

def get_rally_item_set(rally_item, connection):
    rally = connection
    extracted_items = []
    if rally_item == 'User':
        response = rally.getAllUsers()
    else:
        response = rally.get(rally_item)
    for item in response:
        try:
            item.details()
        except UnreferenceableOIDError:
            print('Encountered UnreferenceableOIDError in {} : {}'.format(rally_item, item.ref))
            continue
        except RallyResponseError:
            print('Encountered RallyResponseError in {} : {}'.format(rally_item,item.ref))
            continue
        if item is not None:
            extracted_items.append(item)
    for extracted_item in extracted_items:
        if extracted_item.oid is not None and extracted_item.oid != '':
            set_item_type(extracted_item)
            get_object_ids(extracted_item)
            add_to_db(extracted_item)
    return