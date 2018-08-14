import re

def set_item_type(extracted_item):
    ref_match = re.match("([a-zA-Z]+)/.*", extracted_item.ref)
    extracted_item.RallyItemType = ref_match.group(1).upper()
    return