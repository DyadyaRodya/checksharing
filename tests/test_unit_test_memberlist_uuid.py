import unittest
import uuid

from base.Members_fix2 import Member
from base.Members_fix2 import Members_list
from base.Bills import Bill

class TestMember_list(unittest.TestCase):

    def setUp(self):
        self.id = uuid.uuid1()
        self.member = Member("John", self.id, [400, 1])
        self.member_list = Members_list(self.member)

    def test_get_member_by_global_id(self):
        self.assertEqual(self.member_list.get_member_by_global_id(self.id), self.member)

    def test_get_member(self):
        self.assertEqual(self.member_list.get_member(0), self.member)

    def test_get_member_num(self):
        self.assertEqual(self.member_list.get_member_num(), 1)

    def test_add_member(self):
        id1 = uuid.uuid1()
        member = Member("Max", id1, [300, 0])
        self.member_list.add_member(member)
        self.assertEqual(self.member_list.get_member_by_global_id(id1), member)

    def test_del_member(self):
        self.member_list.del_member(self.member)
        self.assertIsNone(self.member_list.get_member_by_global_id(self.member.get_global_id()))


if __name__ == "__main__":
        unittest.main()
