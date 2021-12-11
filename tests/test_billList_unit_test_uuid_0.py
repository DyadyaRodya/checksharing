import unittest
import uuid

from base.Bills import Bill
from base.Bills import BillList
from base.Members_fix2 import Member

class TestBillList(unittest.TestCase):
    def setUp(self):
        self.billList = BillList()
        #print(len(self.billList.__billList))
        self.mem_id = uuid.uuid1()
        self.bill_id = uuid.uuid1()
        self.member = Member("Max", self.mem_id)
        self.bill = Bill(self.member, self.bill_id, "Claude monet", 1000)
    
    def test_add_bill(self):
        tmp_bill = self.billList.add_bill(self.member, self.bill_id, "Claude monet", 1000)
        self.assertEqual(tmp_bill.get_name(), self.bill.get_name())
        self.assertEqual(tmp_bill.get_summ(), self.bill.get_summ())
        self.assertEqual(tmp_bill.get_member(), self.bill.get_member())
        self.assertEqual(tmp_bill, self.member.get_bill(0))
        
        
    def test_del_bill(self):
        id1 = uuid.uuid1()
        self.billList.add_bill(self.member, id1, "Oguzok", 599)
        #self.billList.del_bill(self.bill) НЕ РАБОТАЕТ
        self.assertEqual(1, self.billList.get_bill_count())
        self.billList.del_bill(Bill(self.member, id1, "Oguzok", 599))
        self.assertEqual(0, self.billList.get_bill_count())

    def test_get_AllSumm(self):
        self.billList.add_bill(self.member, uuid.uuid1(), "Oguzok", 500)
        self.billList.add_bill(self.member, uuid.uuid1(), "Claude monet", 1000)
        self.assertEqual(1500, self.billList.get_AllSumm())
        


if __name__ == "__main__":
  unittest.main()
