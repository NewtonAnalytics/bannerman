import unittest
from bannerman.data import connect_to_rally, get_object_ids, set_item_type, add_to_db

class rally_item_extraction_test(unittest.TestCase):

    def test_for_correct_object_assignment(self):
        rally = connect_to_rally(
            ['--rallyConfig=test.cfg']
        )
        response = rally.get('Function', query='FormattedId = FU557')
        function = response.next()
        set_item_type(function)
        get_object_ids(function)
        db_item = add_to_db(function)
        self.assertEqual(db_item.StateId, 15607812226)

if __name__ == '__main__':
    unittest.main()