from base.Room import Room


class BaseWorker:
    def __init__(self):
        pass


class RoomWorker(BaseWorker):
    def get_rooms_info(self) -> list[Room]:
        return []  # TODO: реализуют вместе с БД - должен отдавать список из Room

    def save(self, list_to_save: list[Room]):
        return True  # TODO: тоже пока заглушка


class BillWorker(BaseWorker):
    pass


class BillListWorker(BaseWorker):
    pass


class MemberWorker(BaseWorker):
    pass


class MemberListWorker(BaseWorker):
    pass
