from datetime import datetime
from src.logic.adapter import Adapter
import uuid


class EventType:
    def __init__(self, event_type):
        self.event_type = event_type

    def __str__(self):
        return self.event_type

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_event_types():
        # TODO: Нужно чтобы из базы данных подтягивались возможные типы событий
        return ['transfer', 'hotel', 'other']


class EventDate:
    def __init__(self, start_date: datetime, end_date: datetime):
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"Start: {self.start_date}, End: {self.end_date}, Duration: {self.get_duration()}"

    def __repr__(self):
        return self.__str__()

    def get_duration(self):
        """
        Возвращает длительность события. Если она больше часа, то в часах. Если в днях, то в днях.
        """
        if self.end_date is None:
            return None
        duration = self.end_date - self.start_date
        duration_minutes = duration.total_seconds() / 60
        if duration_minutes < 60:
            return f'{duration_minutes} min'
        if duration_minutes < 1440:
            return f'{duration_minutes // 60} h'
        return f'{duration_minutes // 1440} d'

class Event:
    def __init__(self, name: str, event_type: EventType, event_date: EventDate, event_data: dict = {}):
        self.name = name
        self.event_type = event_type
        self.event_date = event_date
        self.event_data = event_data
        self.uuid = str(uuid.uuid4())

    def save_to_repository(self):
        adapter = Adapter()
        existing_event = adapter.select_sth_by_uuid('*', 'events', self.uuid)
        if existing_event:
            update_request = f"name='{self.name}', event_type='{self.event_type}', start_date='{self.event_date.start_date}', end_date='{self.event_date.end_date}', event_data='{self.event_data}'"
            adapter.update('events', update_request, self.uuid)
        else:
            columns = "uuid, name, event_type, start_date, end_date, event_data"
            end_date_value = f"'{self.event_date.end_date}'" if self.event_date.end_date else "NULL"
            values = f"'{self.uuid}', '{self.name}', '{self.event_type}', '{self.event_date.start_date}', {end_date_value}, '{self.event_data}'"
            adapter.insert('events', columns, values)

    def get_uuid(self):
        return self.uuid