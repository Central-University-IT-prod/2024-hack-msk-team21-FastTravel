from src.logic.adapter import Adapter
from dotenv import load_dotenv
import os
from src.logic.tour import Tour

load_dotenv(dotenv_path='./.env', verbose=True)

class User:
    def __init__(self, email):
        db = Adapter(host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME'), sslmode="verify-full", user="Admin", password=os.getenv('DB_PASSWORD'), target_session_attrs="read-write")
        userdata = db.sel_userdata_by_email(email=email)
        self.uuid = userdata['uuid']
        print(userdata)
        self.name = userdata['username']
        self.email = email
        self.tour_uuids = userdata.get('tour_uuids', [])
        self.event_uuids = userdata.get('event_uuids', [])
        self.db = db
        self.is_active = userdata['is_active']

    def add_tour(self, tour_uuid):
        if tour_uuid not in self.tour_uuids:
            self.tour_uuids.append(tour_uuid)
            self._update_user_data()

    def remove_tour(self, tour_uuid):
        if tour_uuid in self.tour_uuids:
            self.tour_uuids.remove(tour_uuid)
            self._update_user_data()

    def add_event(self, event_uuid, tour_uuid=None):
        if tour_uuid:
            tour = Tour.get_tour_by_uuid(tour_uuid)
            if tour:
                tour.add_event(event_uuid)
                return
        if event_uuid not in self.event_uuids:
            self.event_uuids.append(event_uuid)
            self._update_user_data()

    def remove_event(self, event_uuid, tour_uuid=None):
        if tour_uuid:
            tour = Tour.get_tour_by_uuid(tour_uuid)
            if tour:
                tour.remove_event(event_uuid)
        if event_uuid in self.event_uuids:
            self.event_uuids.remove(event_uuid)
            self._update_user_data()

    def get_all_tours(self):
        return self.tour_uuids

    def get_all_events(self):
        return self.event_uuids

    def _update_user_data(self):
        tour_uuids_str = '{' + ','.join(map(str, self.tour_uuids)) + '}'
        event_uuids_str = '{' + ','.join(map(str, self.event_uuids)) + '}'
        print(tour_uuids_str, event_uuids_str)
        update_request = f"tour_uuids = '{tour_uuids_str}', event_uuids = '{event_uuids_str}'"
        self.db.update('users', update_request, self.uuid)