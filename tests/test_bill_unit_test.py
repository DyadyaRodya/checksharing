import unittest

from base.Bills import Bill
from base.Members_fix2 import Member

class TestBill(unittest.TestCase):
    def setUp(self):
        self.member = Member("Max", 100)
        self.bill = Bill(self.member, 0, "Claude monet", 999)

    def test_get_id(self):
        self.assertEqual(self.bill.get_id(), 0)

    def test_get_name(self):
        self.assertEqual(self.bill.get_name(), "Claude monet")

    def test_get_summ(self):
        self.assertEqual(self.bill.get_summ(), 999)
        
    def test_get_member(self):
        self.assertEqual(self.member, self.bill.get_member())

    def test_set_name(self):
        self.bill.set_name("Oguzok")
        self.assertEqual(self.bill.get_name(), "Oguzok")

    def test_set_summ(self):
        self.assertFalse(self.bill.set_summ(-1))
        self.assertFalse(self.bill.set_summ(0))
        self.assertTrue(self.bill.set_summ(799))
        self.assertEqual(self.bill.get_summ(), 799)

if __name__ == "__main__":
  unittest.main()
