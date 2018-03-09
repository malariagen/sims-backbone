import abc

class AbstractBackboneDAO(abc.ABC):

    @abc.abstractmethod
    def setup(self, config):
        pass

    def create_event_set(self, event_set_id):

        api_response = self.es_api_instance.create_event_set(event_set_id)

        return api_response

    def create_event_set_item(self, event_set_id, sampling_event_id):
        self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id)

    def create_location(self, location):

        created = self.location_api_instance.create_location(location)

        return created

    def create_sampling_event(self, sampling_event):
        created = self.se_api_instance.create_sampling_event(sampling_event)

        return created

    def delete_sampling_event(self, sampling_event_id):
        self.se_api_instance.delete_sampling_event(sampling_event_id)

    def download_gps_location(self, latitude, longitude):

        ret = self.location_api_instance.download_gps_location(latitude, longitude)
        return ret

    def download_location(self, location_id):

        ret = self.location_api_instance.download_location(location_id)

        return ret

    def download_partner_location(self, partner_name):

        ret = self.location_api_instance.download_partner_location(partner_name)
        return ret

    def download_sampling_event(self, sampling_event_id):

        existing = self.se_api_instance.download_sampling_event(sampling_event_id)

        return existing

    def download_sampling_events_by_identifier(self, identifier_type, identifier_value):

        found_events = self.se_api_instance.download_sampling_events_by_identifier(identifier_type,
                                                                                   identifier_value)

        return found_events

    def update_location(self, location_id, location):

        updated = self.location_api_instance.update_location(location_id, location)

        return updated

    def update_sampling_event(self, sampling_event_id, sampling_event):
        ret = self.se_api_instance.update_sampling_event(sampling_event_id, sampling_event)
        return ret

    def get_country_metadata(self, country_value):
        metadata = self.metadata_api_instance.get_country_metadata(country_value)

        return metadata
