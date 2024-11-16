from src.logic.adapter import Adapter

class Tour:
    def __init__(self, name, countries=None, uuid=None):
        self.name = name
        self.countries = countries or []
        self.events = []
        self.uuid = uuid or str(uuid.uuid4())

    def add_event(self, event):
        self.events.append(event)

    def add_country(self, country):
        if country not in self.countries:
            self.countries.append(country)

    def remove_country(self, country):
        if country in self.countries:
            self.countries.remove(country)

    def __str__(self):
        return f"Tour: {self.name}, Countries: {self.countries}, Events: {self.events}"

    def __repr__(self):
        return self.__str__()

    def save_to_repository(self):
        adapter = Adapter()
        existing_tour = adapter.select_sth_by_uuid('*', 'tours', self.uuid)
        if existing_tour:
            update_request = f"name='{self.name}', countries='{self.countries}', events='{self.events}'"
            adapter.update('tours', update_request, self.uuid)
        else:
            columns = "uuid, name, countries, events"
            values = f"'{self.uuid}', '{self.name}', '{self.countries}', '{self.events}'"
            adapter.insert('tours', columns, values)

    def get_uuid(self):
        return self.uuid

    @staticmethod
    def get_tour_by_uuid(uuid):
        adapter = Adapter()
        tour_data = adapter.select_sth_by_uuid('*', 'tours', uuid)
        if tour_data:
            tour_data = tour_data[0]
            tour = Tour(tour_data[1], tour_data[2], tour_data[0])
            return tour
        return None