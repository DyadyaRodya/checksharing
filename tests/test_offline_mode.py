import unittest
from uuid import UUID

from base.Members_fix2 import Member
from base.Room import Room
from controllers.controller import RoomController


class TestOfflineRoom(unittest.TestCase):
    def setUp(self):
        self.rc = RoomController()
        self.m_id = self.rc.add_member("John")
        self.rc.add_member(name="Rob", global_id=300)

    def test_local_room_bills(self):
        b_id1 = self.rc.add_bill_to_room("local", self.m_id, "Claude Monet", 20000)
        b_id2 = self.rc.add_bill_to_room("local", 300, "Claude Monet", 20000)
        self.assertIsInstance(b_id2, UUID)
        self.assertEqual(self.rc.get_room_info("local").get_total_summ(), 40000)

        edit_id = self.rc.edit_bill_room("local", b_id2, 300, "Claude Monet", 30000)
        self.assertEqual(edit_id, b_id2)
        self.assertIsNone(self.rc.add_bill_to_room("local", 300, "Claude Monet", 70000))
        self.assertIsNone(self.rc.add_bill_to_room("newroom", 100, "Claude Monet", 1000))
        self.assertIsNone(self.rc.add_bill_to_room("local", 555, "Claude Monet", 1000))
        self.assertEqual(self.rc.get_room_info("local").get_total_summ(), 50000)

        self.assertIsNone(self.rc.del_bill_from_room("local", 132))
        self.assertIsNone(self.rc.del_bill_from_room("newroom", b_id2))
        self.rc.del_bill_from_room("local", b_id2)
        self.assertEqual(self.rc.get_room_info("local").get_total_summ(), 20000)

        self.rc.set_winners_in_the_room()
        winners_l = self.rc.get_winners_in_the_room()
        self.assertIsInstance(winners_l, list)

    def test_get_room(self):
        room = self.rc.get_room_by_name('local')
        self.assertIsInstance(room, Room)
        self.assertEqual(room.get_name(), 'local')

    def test_members_list_edit(self):
        self.assertIsInstance(self.m_id, UUID)
        m2_id = self.rc.add_member(name="Mary", global_id=self.m_id)
        self.assertFalse(m2_id)
        m2_id = self.rc.add_member(name="John", room_name="second_room")
        self.assertIsNone(m2_id)

    def test_delete_member(self):
        self.assertTrue(self.rc.del_member(global_id=self.m_id))


if __name__ == "__main__":
    unittest.main()
