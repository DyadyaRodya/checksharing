import uuid

from managers.manager import RoomManager, BillManager, BillListManager, MemberManager, MembersListManager
from workers.workers import RoomWorker, BillWorker, BillListWorker, MemberWorker, MemberListWorker
from base.Members_fix2 import Member
from base.Members_fix2 import Members_list
from base.Bills import Bill
from base.Bills import BillList
from base.Room import Room
from helpers.helpers import python_way_wrapper


class RoomController:
    __rooms: dict[str, Room]

    def __init__(self):
        self.__room_manager = RoomManager()
        self.__room_worker = RoomWorker()
        self.__rooms = {'local': Room(name='local')}
        db_rooms = self.__room_worker.get_rooms_info()  # TODO: кто БД будет делать, в зависимости от реализации допилит
        for room in db_rooms:
            self.__rooms[room.get_name()] = room

    @python_way_wrapper
    def get_room_by_name(self, name: str = 'local'):
        return self.__rooms.get(name)

    @python_way_wrapper
    def make_local_room_online(self, new_name: str):
        """переносит локальную комнату под другой ключ чтобы она созранилась в БД (None если ключ занят)"""
        if new_name not in self.__rooms.keys():
            self.__rooms[new_name] = self.__rooms['local']
            self.__rooms[new_name].set_name(new_name)
            self.reset_local_room()
            return new_name
        return None

    @python_way_wrapper
    def save_to_bd(self):
        """отдает воркеру список комнат для сохраниения в БД
        (подразумевается, что воркер сам надет комнаты для удаления, обновления или добавления и всё сделает сам)
        должен вернут результат сохранения в БД"""
        list_to_save = []
        for key, value in self.__rooms.items():
            if key != 'local':
                list_to_save.append(value)
        return self.__room_worker.save(list_to_save)

    @python_way_wrapper
    def reset_local_room(self):
        """Возвращает имя локальной комнаты из списка"""
        self.__rooms['local'] = Room(name='local')
        return 'local'

    @python_way_wrapper
    def start_new_room(self, name: str):
        """Возвращает имя созданной комнаты или None (если имя уже есть)"""
        if name not in self.__rooms.keys():
            new_room = Room(name=name)
            self.__rooms[name] = new_room
            return name
        return None

    @python_way_wrapper
    def delete_room(self, name: str):
        """Удаляет комнату по имени, если комната удалена успешно или ее нет вернет True"""
        if name in self.__rooms.keys():
            del self.__rooms[name]
        return True

    @python_way_wrapper
    def is_room_exists(self, name: str):
        """проверяет, есть ли комната"""
        return name in self.__rooms.keys()

    @python_way_wrapper
    def add_bill_to_room(self, room_name, member_global_id, rest_name, summ, bill_id = None):
        """проверяет, что есть такой участник, комната
        и что (предел суммы счета не превышен или платят больше 1 человека)
        bill_id возвращает при успехе, иначе None"""
        if room_name in self.__rooms.keys():
            current_room = self.__rooms[room_name]
            member: Member = current_room.get_mem_list().get_member_by_global_id(member_global_id)
            new_summ = current_room.get_total_summ() + summ
            if member is not None and (current_room.get_win_count() > 1 or new_summ <= current_room.get_summ_limit()):
                current_room_bills = current_room.get_bill_list()
                bill: Bill or None = None
                if bill_id is None:
                    bill_id = uuid.uuid1()
                else:
                    for i in range(current_room_bills.get_bill_count()):
                        if current_room_bills.get_bill(i).get_id() == bill_id:
                            bill = current_room_bills.get_bill(i)
                            break
                if bill is not None and (bill.get_name() != rest_name or bill.get_summ() != summ or
                                         bill.get_member() != member):  # bill_id exists but diffs
                    return False
                elif bill is not None:  # bill exists
                    return bill_id
                added_bill = current_room_bills.add_bill(member, bill_id, rest_name, summ)
                member.add_bill(added_bill)
                current_room.set_total_summ(current_room_bills.get_AllSumm())
                return bill_id
        return None

    @python_way_wrapper
    def edit_bill_room(self, room_name, old_bill_id, member_global_id, bill_id, rest_name, summ):
        """проверяет, что есть такой участник, комната, счет
        и что (предел суммы счета не превышен или платят больше 1 человека)
        новую сумму возвращает при успехе, иначе None"""
        if room_name in self.__rooms.keys():
            current_room = self.__rooms[room_name]
            member: Member = current_room.get_mem_list().get_member_by_global_id(member_global_id)
            current_room_bills = current_room.get_bill_list()
            bill: Bill or None = None
            for i in range(current_room_bills.get_bill_count()):
                if current_room_bills.get_bill(i).get_id() == old_bill_id:
                    bill = current_room_bills.get_bill(i)
                    break
            if bill is not None:
                new_summ = current_room.get_total_summ() + summ - bill.get_summ()
                if member is not None and \
                        (current_room.get_win_count() > 1 or new_summ <= current_room.get_summ_limit()):
                    # remove old bill
                    current_room_bills.del_bill(bill)
                    added_bill = current_room_bills.add_bill(member, bill_id, rest_name, summ)
                    current_room.set_total_summ(current_room_bills.get_AllSumm())
                    # upd member
                    old_member: Member = bill.get_member()
                    old_member.del_bill(bill)
                    member.add_bill(added_bill)
                    return current_room.get_total_summ()
        return None

    @python_way_wrapper
    def del_bill_from_room(self, room_name, bill_id):
        """проверяет, что есть такая комната, счет
        новую сумму возвращает при успехе, иначе None"""
        if room_name in self.__rooms.keys():
            current_room = self.__rooms[room_name]
            current_room_bills = current_room.get_bill_list()
            bill: Bill or None = None
            for i in range(current_room_bills.get_bill_count()):
                if current_room_bills.get_bill(i).get_id() == bill_id:
                    bill = current_room_bills.get_bill(i)
                    break
            if bill is not None:
                current_room_bills.del_bill(bill)
                current_room.set_total_summ(current_room_bills.get_AllSumm())
                # upd member
                member: Member = bill.get_member()
                member.del_bill(bill)
                return current_room.get_total_summ()
        return None

    @python_way_wrapper
    def add_member(self, name: str, room_name: str = 'local', global_id: int = None):
        """None если нет комнаты, false если global_id есть и имя отличается,
        global_id если добавлен или уже есть с таким global_id и именем"""
        if room_name in self.__rooms.keys():
            member = None
            current_room: Room = self.__rooms[room_name]
            if global_id is None:
                global_id = uuid.uuid1()
                while current_room.get_mem_list().get_member_by_global_id(global_id):
                    global_id = uuid.uuid1()
            else:
                member: Member = current_room.get_mem_list().get_member_by_global_id(global_id)
            if member is not None and member.get_name() != name:  # member exists but diff name
                return False
            elif member is not None and member.get_name() == name:  # member exists
                return global_id
            # member is none == need to add member
            member = Member(name, global_id)
            current_room.get_mem_list().add_member(member)
            return global_id
        return None

    @python_way_wrapper
    def del_member(self, room_name: str = 'local', global_id: int = None):
        """None если нет комнаты или мембера, True если удален"""
        if room_name in self.__rooms.keys():
            current_room: Room = self.__rooms[room_name]
            member = current_room.get_mem_list().get_member_by_global_id(global_id)
            if member is not None:
                current_room.del_mem_bills(global_id)
                current_room.get_mem_list().del_member(member)
                return True
        return None

    @python_way_wrapper
    def edit_payment_settings(self, room_name: str = 'local', win_count: int = None):
        """None если нет комнаты, True если успешно, False если плохое число"""
        if room_name in self.__rooms.keys():
            current_room: Room = self.__rooms[room_name]
            res = current_room.set_win_count(win_count)
            return not res  # not -1 == False, not 0 == True
        return None

    @python_way_wrapper
    def set_winners_in_the_room(self, room_name: str = 'local'):
        if room_name in self.__rooms.keys():
            current_room: Room = self.__rooms[room_name]
            winners = current_room.set_payment()
            mem_list: Members_list = current_room.get_mem_list()
            winners_list = []
            for winner in winners:
                winners_list.append(mem_list.get_member(winner))
            return winners_list
        return None

    @python_way_wrapper
    def get_winners_in_the_room(self, room_name: str = 'local'):
        if room_name in self.__rooms.keys():
            current_room: Room = self.__rooms[room_name]
            mem_list: Members_list = current_room.get_mem_list()
            winners_number = mem_list.get_member_num()
            winners_list = []
            for num in range(winners_number):
                mem: Member = mem_list.get_member(num)
                if mem.get_status():
                    winners_list.append(mem)
            return winners_list
        return None
