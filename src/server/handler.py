from src.logic.user import User
from src.logic.event import Event, EventType, EventDate
from datetime import datetime

def handle_add_event(data):
    user_email = data.get('user_email')
    tour_uuid = data.get('tour_uuid')
    event_name = data.get('event_name')
    event_type_str = data.get('event_type')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    event_data = data.get('event_data', {})

    if not user_email or not event_name or not event_type_str or not start_date_str:
        return {'error': 'Недостаточно данных для создания события'}

    user = User(user_email)
    event_type = EventType(event_type_str)
    start_date = datetime.fromisoformat(start_date_str)
    end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
    event_date = EventDate(start_date, end_date)
    event = Event(event_name, event_type, event_date, event_data)
    event.save_to_repository()

    if tour_uuid:
        user.add_event(event.get_uuid(), tour_uuid)
    else:
        user.add_event(event.get_uuid())

    return {'success': True, 'event_uuid': event.get_uuid()}