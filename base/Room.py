import random
import time

from base.Members_fix2 import Member
from base.Members_fix2 import Members_list
from base.Bills import Bill
from base.Bills import BillList

WIN_COUNT_DEFAULT = 1
MEM_LIMIT_DEFAULT = 9000
TIMEOUT_DEFAULT = 9000
SUMM_LIMIT_DEFAULT = 100000

class Room:
    """Необязательная строка документации класса"""  

    def __init__(self, name, mem_limit = MEM_LIMIT_DEFAULT, timeout = TIMEOUT_DEFAULT):
        self.__mem_list = Members_list()
        self.__bill_list = BillList()
        self.__name = name
        self.__mem_limit = mem_limit
        self.__win_count = WIN_COUNT_DEFAULT
        self.__summ_limit = SUMM_LIMIT_DEFAULT
        self.__timeout = timeout
        self.__bank_num = ""
        self.__total_summ = 0

    def get_mem_list(self):
        return self.__mem_list

    def get_bill_list(self):
        return self.__bill_list

    def get_name(self):
        return self.__name

    def get_mem_limit(self):
        return self.__mem_limit

    def get_win_count(self):
        return self.__win_count


    def get_summ_limit(self):
        return self.__summ_limit

    def get_timeout(self):
        return self.__timeout

    def get_bank_num(self):
        return self.__bank_num

    def get_total_summ(self):
        return self.__total_summ
    
    def set_win_count(self, win_count):
        if win_count > 0:
            self.__win_count = win_count
            return 0
        else:
            return -1

    def set_summ_limit(self, summ_limit):
        if summ_limit > 0:
            self.__summ_limit = summ_limit
            return 0
        else:
            return -1

    def set_timeout(self, timeout):
        if timeout >= 0:
            self.__timeout = timeout
            return 0
        else:
            return -1


    def set_bank_num(self, summ_bank_num):
        self.__bank_num = summ_bank_num

    def set_name(self, name):
        self.__name = name

    def set_total_summ(self, summ_total_summ):
        if summ_total_summ>=0:
            self.__total_summ = summ_total_summ
            return 0
        else:
            return  -1

    def del_mem_bills(self, global_id):
        #k = 0
        i = 0
        m = self.__mem_list.get_member_by_global_id(global_id)
        #print("bill count: " + str(self.__bill_list.get_bill_coint()))
        while (i < self.__bill_list.get_bill_count()):
            #print(i)
            b = self.__bill_list.get_bill(i)
            if b.get_member() is m:
                self.__bill_list.del_bill(b)
                i -= 1
                #k += 0
            i += 1
        #print("deleted bills: " + str(k))
        
    def set_payment(self):
        self.set_total_summ(self.__bill_list.get_AllSumm())
        one_pay = self.__total_summ / self.__win_count
        
        random.seed(time.time())
        winners = random.sample(range(self.__mem_list.get_member_num()), self.__win_count)
        for winner in winners:
            m = self.__mem_list.get_member(winner)
            m.set_status([one_pay, False])
        return winners
    
    
