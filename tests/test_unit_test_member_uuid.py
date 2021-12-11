import unittest

from base.Members_fix2 import Member
from base.Bills import Bill

class TestMember(unittest.TestCase):
    def setUp(self):
        self.member = Member("Max", 100, [200, 1])

    def test_name(self):
        self.assertEqual(self.member.get_name(), "Max")
        self.member.set_name("Maxim")
        self.assertEqual(self.member.get_name(), "Maxim")

    def test_get_global_id(self):
        self.assertEqual(self.member.get_global_id(), 100)

    def test_get_status(self):
        self.assertListEqual(self.member.get_status(), [200, 1])

    def test_IsPayed(self):
        self.assertEqual(self.member.IsPayed(), 1)

    def test_set_name(self):
        self.member.set_name("John")
        self.assertEqual(self.member.get_name(), "John")

    def test_set_status(self):
        self.member.set_status([300, 0])
        self.assertListEqual(self.member.get_status(), [300, 0])

    def test_update_status(self):
        self.member.update_status(0)
        self.assertEqual(self.member.IsPayed(),0)

    def test_get_bill_num(self):
        self.assertEqual(self.member.get_bill_num(), 0)

    def test_add_bill(self):
        self.member.add_bill(Bill(self.member, 1000))
        self.assertEqual(self.member.get_bill_num(), 1)

    def test_get_bill(self):
        bill = Bill(self.member, 1000)
        self.member.add_bill(bill)
        self.assertEqual(self.member.get_bill(0), bill)

    def test_del_bill(self):
        bill = Bill(self.member, 1000)
        self.member.add_bill(bill)
        self.member.del_bill(bill)
        b = None
        for i in range(self.member.get_bill_num()):
            if self.member.get_bill(i) == bill:
                b = bill
        self.assertIsNone(b)

if __name__ == "__main__":
  unittest.main()
