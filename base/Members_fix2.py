import random
import subprocess

class Member:

    def __init__(self, name, global_id, status = []):
        self.__name = name
        self.__global_id = global_id
        self.__bills = []
        self.__status = status

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_global_id(self):
        return self.__global_id

    def get_status(self):
        return self.__status

    def get_bill_num(self):
        return len(self.__bills)

    def get_bill(self, id):
        return self.__bills[id]

    def IsPayed(self):
        return self.__status[1]

    def set_status(self, new_status):
        self.__status = new_status
    
    def update_status(self, payed):
        self.__status[1] = payed

    def add_bill(self, bill):
        self.__bills.append(bill)

    def del_bill(self, bill):
        self.__bills.remove(bill)



class Members_list:

    def __init__(self, member = None):
        self.__members = []
        if member != None:
            self.__members.append(member)

    def get_member_by_global_id(self, global_id):
        participant = None
        for p in self.__members:
            if p.get_global_id() == global_id:
                participant = p
        return participant

    def add_member(self, member):
        self.__members.append(member)

    def del_member(self, member):
        self.__members.remove(member)

    def get_member_num(self):
        return len(self.__members)

    def get_member(self, id):
        return self.__members[id]


