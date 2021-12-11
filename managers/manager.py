from base.Members_fix2 import Member
from base.Members_fix2 import Members_list
from base.Bills import Bill
from base.Bills import BillList
from base.Room import Room, WIN_COUNT_DEFAULT, MEM_LIMIT_DEFAULT, TIMEOUT_DEFAULT, SUMM_LIMIT_DEFAULT


class BaseManager:
    def __init__(self):
        pass

    def _get_object(self, **kwargs):
        raise NotImplementedError("_get_object must be implemented in child class")

    def obj_from_dict(self, **kwargs):
        try:
            return self._get_object(**kwargs)
        except Exception as e:
            print(f'Invalid input data for {self.__class__.__name__} dict. Error: {e}')
            return None

    def _to_dict(self, obj):
        raise NotImplementedError("obj_to_json must be implemented in child class")

    def obj_to_dict(self, *args):
        try:
            return self._to_dict(*args)
        except Exception as e:
            print(f'Invalid input object for {self.__class__.__name__}. Error: {e}')
            return None


class BillManager(BaseManager):
    @staticmethod
    def _get_object(data):
        if 'member' in data.keys() and isinstance(data['member'], Member) and \
                'id' in data.keys() and isinstance(data['id'], int) and \
                ('name' not in data.keys() or isinstance(data.get('name'), str)) and \
                ('summ' not in data.keys() or isinstance(data.get('summ'), int)):
            return Bill(member=data['member'], id=data['id'],
                        name=data['name'] if 'name' in data.keys() else "",
                        summ=data['summ'] if 'summ' in data.keys() else 0)
        else:
            raise AttributeError(f"Bad data dict: {data}")

    @staticmethod
    def _to_dict(obj: Bill, *args):
        return {
            'name': obj.get_name(),
            'id': obj.get_id(),
            'summ': obj.get_summ(),
            'member_id': obj.get_member().get_global_id()
        }


class BillListManager(BaseManager):
    @staticmethod
    def _get_object():
        return BillList()


class MemberManager(BaseManager):
    @staticmethod
    def _get_object(data):
        if 'name' in data.keys() and isinstance(data['name'], str) and \
                'global_id' in data.keys() and isinstance(data['global_id'], int) and \
                ('status' not in data.keys() or isinstance(data.get('status'), list)):
            return Member(name=data['name'], global_id=data['global_id'],
                          status=data['status'] if 'status' in data.keys() else [])
        else:
            raise AttributeError(f"Bad data dict: {data}")


class MembersListManager(BaseManager):
    @staticmethod
    def _get_object(data):
        if 'member' in data.keys() and isinstance(data['member'], Member):
            return Members_list(data['member'])
        else:
            return Members_list()


class RoomManager(BaseManager):
    @staticmethod
    def _get_object(data):
        if 'name' in data.keys() and isinstance(data['name'], str) and \
                ('mem_limit' not in data.keys() or isinstance(data.get('mem_limit'), int)) and \
                ('timeout' not in data.keys() or isinstance(data.get('timeout'), int)):
            return Room(name=data['name'],
                        mem_limit=data['mem_limit'] if 'mem_limit' in data.keys() else MEM_LIMIT_DEFAULT,
                        timeout=data['timeout'] if 'timeout' in data.keys() else TIMEOUT_DEFAULT)
        else:
            raise AttributeError(f"Bad data dict: {data}")
