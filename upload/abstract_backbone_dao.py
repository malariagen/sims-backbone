import abc

class AbstractBackboneDAO(abc.ABC):

    @abc.abstractmethod
    def setup(self, config):
        pass

    def create_event_set(self, event_set_id):

        api_response = self.es_api_instance.create_event_set(event_set_id)

        return api_response

    def download_event_set(self, eventSetId):
        return self.es_api_instance.download_event_set(eventSetId)

    def delete_event_set(self, eventSetId):
        return self.es_api_instance.delete_event_set(eventSetId)


    def create_event_set_item(self, event_set_id, sampling_event_id):
        self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id)

    def create_location(self, location):

        created = self.location_api_instance.create_location(location)

        return created

    def create_sampling_event(self, sampling_event):
        created = self.se_api_instance.create_sampling_event(sampling_event)

        return created

    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2):
        self.se_api_instance.merge_sampling_events(sampling_event_id1, sampling_event_id2)

    def delete_sampling_event(self, sampling_event_id):
        self.se_api_instance.delete_sampling_event(sampling_event_id)

    def download_gps_location(self, latitude, longitude):

        ret = self.location_api_instance.download_gps_location(latitude, longitude)
        return ret

    def download_location(self, location_id):

        ret = self.location_api_instance.download_location(location_id)

        return ret

    def delete_location(self, location_id):
        ret = self.location_api_instance.delete_location(location_id)

        return ret

    def download_partner_location(self, partner_name):

        ret = self.location_api_instance.download_partner_location(partner_name)
        return ret

    def download_sampling_event(self, sampling_event_id):

        existing = self.se_api_instance.download_sampling_event(sampling_event_id)

        return existing

    def download_sampling_events_by_event_set(self, eventSetId):
        return self.se_api_instance.download_sampling_events_by_event_set(eventSetId)

    def download_sampling_events_by_attr(self, attr_type, attr_value):

        found_events = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                                   attr_value)

        return found_events

    def download_sampling_events_by_study(self, study_name):

        found_events = self.se_api_instance.download_sampling_events_by_study(study_name)

        return found_events

    def download_sampling_events_by_os_attr(self, attr_type, attr_value):

        found_events = self.se_api_instance.download_sampling_events_by_os_attr(attr_type,
                                                                                   attr_value)

        return found_events

    def download_sampling_events_by_location(self, location_id):

        found_events = self.se_api_instance.download_sampling_events_by_location(location_id)

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

    def create_original_sample(self, original_sample):

        return self.os_api_instance.create_original_sample(original_sample)


    def update_original_sample(self, original_sample_id, original_sample):

        return self.os_api_instance.update_original_sample(original_sample_id,
                                                                            original_sample)

    def merge_original_samples(self, original_sample_id1, original_sample_id2):

        return self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2)

    def delete_original_sample(self, original_sample_id ):

        return self.os_api_instance.delete_original_sample(original_sample_id)

    def download_original_sample(self, original_sample_id):

        return self.os_api_instance.download_original_sample(original_sample_id)

    def download_original_samples_by_attr(self, attr_type, attr_value):

        return self.os_api_instance.download_original_samples_by_attr(attr_type, attr_value)


    def create_derivative_sample(self, derivative_sample):

        return self.ds_api_instance.create_derivative_sample(derivative_sample)


    def update_derivative_sample(self, derivative_sample_id, derivative_sample):

        return self.ds_api_instance.update_derivative_sample(derivative_sample_id,
                                                                            derivative_sample)

    def delete_derivative_sample(self, derivative_sample_id ):

        return self.ds_api_instance.delete_derivative_sample(derivative_sample_id)

    def download_derivative_sample(self, derivative_sample_id):

        return self.ds_api_instance.download_derivative_sample(derivative_sample_id)

    def download_derivative_samples_by_attr(self, attr_type, attr_value):

        return self.ds_api_instance.download_derivative_samples_by_attr(attr_type, attr_value)


    def create_assay_datum(self, assay_datum):

        return self.ad_api_instance.create_assay_datum(assay_datum)


    def update_assay_datum(self, assay_datum_id, assay_datum):

        return self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum)

    def delete_assay_datum(self, assay_datum_id):

        return self.ad_api_instance.delete_assay_datum(assay_datum_id)

    def download_assay_data_by_attr(self, attr_type, attr_value):

        return self.ad_api_instance.download_assay_data_by_attr(attr_type, attr_value)

    def download_study(self, study_code):
        return self.study_api_instance.download_study(study_code)

    def download_studies(self):
        return self.study_api_instance.download_studies()

    def update_study(self, study_code, study_detail):
        return self.study_api_instance.update_study(study_code, study_detail)

    def create_individual(self, individual):

        return self.i_api_instance.create_individual(individual)


    def update_individual(self, individual_id, individual):

        return self.i_api_instance.update_individual(individual_id, individual)

    def merge_individuals(self, individual_id1, individual_id2):

        return self.i_api_instance.merge_individuals(individual_id1, individual_id2)

    def delete_individual(self, individual_id ):

        return self.i_api_instance.delete_individual(individual_id)

    def download_individual(self, individual_id):

        return self.i_api_instance.download_individual(individual_id)

    def download_individuals_by_attr(self, prop_name, prop_value, study_name=None):

        return self.i_api_instance.download_individuals_by_attr(prop_name,
                                                                prop_value,
                                                                study_name=study_name)

