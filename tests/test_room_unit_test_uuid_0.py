import unittest

from base.Members_fix2 import Member
from base.Members_fix2 import Members_list
from base.Bills import Bill
from base.Bills import BillList
import uuid
from base.Room import Room, WIN_COUNT_DEFAULT, MEM_LIMIT_DEFAULT, TIMEOUT_DEFAULT, SUMM_LIMIT_DEFAULT

class TestRoom(unittest.TestCase):
    def setUp(self):
        self.room = Room("TestRoom")
        self.mlist = []
        self.blist = []

    def test_name(self):
        self.assertEqual("TestRoom", self.room.get_name())
        self.room.set_name("TestRoom2")
        self.assertEqual("TestRoom2", self.room.get_name())

    def test_mem_limit(self):
        self.assertEqual(MEM_LIMIT_DEFAULT, self.room.get_mem_limit())

    def test_win_count(self):
        self.assertEqual(WIN_COUNT_DEFAULT, self.room.get_win_count())
        self.assertEqual(self.room.set_win_count(-2), -1)
        
    def test_summ_limit(self):
        self.assertEqual(SUMM_LIMIT_DEFAULT, self.room.get_summ_limit())
        self.room.set_summ_limit(7777)
        self.assertEqual(7777, self.room.get_summ_limit())
        self.assertEqual(self.room.set_summ_limit(-100), -1)
    def test_timeout(self):
        self.assertEqual(TIMEOUT_DEFAULT, self.room.get_timeout())
        self.room.set_timeout(9000)
        self.assertEqual(9000, self.room.get_timeout())
        self.assertEqual(self.room.set_timeout(-100),-1)
        
    def test_summ_bank_num(self):
        self.assertEqual("", self.room.get_bank_num())
        self.room.set_bank_num("7777777")
        self.assertEqual("7777777", self.room.get_bank_num())
        
    def test_total_summ(self):
        self.assertEqual(0, self.room.get_total_summ())
        self.room.set_total_summ(10000)
        self.assertEqual(10000, self.room.get_total_summ())
        self.assertEqual(self.room.set_total_summ(-1000), -1)

################################################################

    def test_mem_bill_list(self):
        self.mlist = self.room.get_mem_list()

        id1 = uuid.uuid1()
        id2 = uuid.uuid1()
        id3 = uuid.uuid1()

        m = Member("Max", id1)
        m2 = Member("Moonlover", id2)
        m3 = Member("Ghettoboi", id3)
        self.mlist.add_member(m)
        self.mlist.add_member(m2)
        self.assertEqual(m, self.room.get_mem_list().get_member(0))
        self.assertEqual(self.mlist.get_member(0), self.room.get_mem_list().get_member(0))
        self.assertEqual(None, self.room.get_mem_list().add_member(m))
        
        self.blist = self.room.get_bill_list()
        self.blist.add_bill(m, m.get_bill_num(), "Claude monet", 1000)
        self.blist.add_bill(m2, m2.get_bill_num(), "Claude monet2", 2000)
        self.blist.add_bill(m, m.get_bill_num(), "Claude monet3", 40000)
        self.blist.add_bill(m3, m3.get_bill_num(), "Claude monet", 20000)
        self.blist.add_bill(m3, m3.get_bill_num(), "Claude monet3", 500)
        self.assertEqual(63500, self.room.get_bill_list().get_AllSumm())
        
        ######################################################
        ## esli kto-to vishel - bill udalilsa
        self.room.del_mem_bills(id1)
        self.assertEqual(22500, self.room.get_bill_list().get_AllSumm())
        
        btd = m3.get_bill(m3.get_bill_num() - 1)
        self.room.get_bill_list().del_bill(btd)
        self.assertEqual(22000, self.room.get_bill_list().get_AllSumm())
        
    def test_payment(self):
        win_cnt = 2
        m = Member("Max", uuid.uuid1())
        m2 = Member("Moonlover", uuid.uuid1())
        m3 = Member("Ghettoboi", uuid.uuid1())
        self.mlist = self.room.get_mem_list()
        self.mlist.add_member(m)
        self.mlist.add_member(m2)
        self.mlist.add_member(m3)
        self.blist = self.room.get_bill_list()
        self.blist.add_bill(m, m.get_bill_num(), "Claude monet", 1000)
        self.blist.add_bill(m2, m2.get_bill_num(), "Claude monet2", 5000)
        self.blist.add_bill(m3, m3.get_bill_num(), "Claude monet", 20000)
        self.blist.add_bill(m3, m3.get_bill_num(), "Claude monet3", 500)
        self.room.set_bank_num("7777777")
        self.room.set_win_count(win_cnt)
        wnnrs = self.room.set_payment()
        
        #for i in range(self.mlist.get_member_num()):
        #    print(self.mlist.get_member(i).get_status())
        ok = 0
        to_pay = self.blist.get_AllSumm() / win_cnt
        
        for i in range(self.mlist.get_member_num()):
            #print(self.mlist.get_member(i).get_status())
            st = self.mlist.get_member(i).get_status()
            if (len(st) and st[0] == to_pay):
                ok += 1
        
        self.assertEqual(win_cnt, ok)
        
        self.mlist.get_member(wnnrs[0]).update_status(True)
        self.assertEqual(True, self.mlist.get_member(wnnrs[0]).IsPayed())
        
        
        
    

if __name__ == "__main__":
  unittest.main()
