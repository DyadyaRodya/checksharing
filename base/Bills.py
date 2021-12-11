

class Bill:
    """Необязательная строка документации класса"""  
    #__rest_name = ""
    #__summ = 0
    #__id = 0
    #__member = None

    def __init__(self, member, id, name = "", summ = 0):
        self.__member = member
        self.__id = id
        self.__rest_name = name
        self.__summ = summ

    def get_name(self):  
        return self.__rest_name

    def get_summ(self):
        return self.__summ
        
    def get_member(self):
        return self.__member

    def get_id(self):
        return self.__id
  
    def set_name(self, name):  
        self.__rest_name = name
    
    def set_summ(self, summ):
        if summ > 0:
            self.__summ = summ
            return True
        else:
            return False


class BillList:
    """Необязательная строка документации класса"""  

    def __init__(self):
        self.__billList = list()

    def get_bill(self, num):
        return self.__billList[num]

    def add_bill(self, member, id, name, summ):
        bill = Bill(member, id, name, summ)
        member.add_bill(bill)
        self.__billList.append(bill)
        return self.__billList[len(self.__billList) - 1]
  
    def del_bill(self, billToDel):
        for bill in self.__billList:
            #print("BILL " + str(bill.get_name()) + " " + str(bill.get_summ()) + " " + str(bill.get_member().get_global_id()))
            if ((billToDel.get_name() == bill.get_name()) and (billToDel.get_summ() == bill.get_summ()) and (billToDel.get_member() == bill.get_member())):
                #print("DELETING")
                self.__billList.remove(bill)
                break
        #self.__billList.remove(billToDel) НЕ РАБОТАЕТ
    
    def get_bill_count(self):
        return len(self.__billList)
    
    def get_AllSumm(self):
        summ = 0
        for bill in self.__billList:
            summ += bill.get_summ()
        return summ
    


#print("Hello world\n")
#
#listt = BillList()
#billl = Bill(None, 0)
#billl.set_name("OOGA")
#billl.set_summ(5555)
#print(billl.get_name() + " " + str(billl.get_summ()))
#bill2 = Bill(None, 0)
#bill2.set_name("BOOGA")
#bill2.set_summ(7777)
#print(bill2.get_name() + " " + str(bill2.get_summ()))
#bill3 = Bill(None, 0, "CLOUD MONET", 3333)
#print(bill3.get_name() + " " + str(bill3.get_summ()))

#listt.add_bill(billl)
#listt.add_bill(bill2)
#print(lisst.get_AllSumm())

