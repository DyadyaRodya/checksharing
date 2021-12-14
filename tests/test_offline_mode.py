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
        self.rc.add_member(name="Mary", global_id=200)
        self.rc.add_bill_to_room("local", self.m_id, 1, "Claude Monet", 20000)
        total_sum = self.rc.add_bill_to_room("local", 200, 2, "Claude Monet", 20000)
        self.assertEqual(total_sum, 40000)

        total_sum = self.rc.edit_bill_room("local", 2, 200, 3, "Claude Monet", 30000)
        self.assertIsNone(self.rc.add_bill_to_room("local", 200, 4, "Claude Monet", 70000))
        self.assertIsNone(self.rc.add_bill_to_room("newroom", 200, 4, "Claude Monet", 1000))
        self.assertIsNone(self.rc.add_bill_to_room("local", 555, 4, "Claude Monet", 1000))
        self.assertEqual(total_sum, 50000)

        self.assertIsNone(self.rc.del_bill_from_room("local", 2))
        self.assertIsNone(self.rc.del_bill_from_room("newroom", 3))
        total_sum = self.rc.del_bill_from_room("local", 3)
        self.assertEqual(total_sum, 20000)

        winners = self.rc.get_winners_in_the_room()
        self.assertIsInstance(winners, list)
        print(winners)


class TestMembersListEdit(unittest.TestCase):
    def setUp(self):
        self.rc = RoomController()
        self.m_id = self.rc.add_member("John")

    def test_get_room(self):
        room = self.rc.get_room_by_name('local')
        self.assertIsInstance(room, Room)
        self.assertEqual(room.get_name(), 'local')

    def test_members_list_edit(self):
        # m_id = self.rc.add_member("John")
        self.assertIsInstance(self.m_id, UUID)
        # self.assertFalse(self.rc.add_member(name="John", global_id=self.m_id))
        m2_id = self.rc.add_member(name="Mary", global_id=self.m_id)
        self.assertFalse(m2_id)
        m2_id = self.rc.add_member(name="John", room_name="second_room")
        self.assertIsNone(m2_id)

    def test_delete_member(self):
        self.assertTrue(self.rc.del_member(global_id=self.m_id))


if __name__ == "__main__":
    unittest.main()
