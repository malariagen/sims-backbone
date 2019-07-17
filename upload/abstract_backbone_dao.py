import abc

class AbstractBackboneDAO(abc.ABC):

    def __init__(self, user, auths):
        self._user = user
        self._auths = auths
        self.es_api_instance = None
        self.location_api_instance = None
        self.se_api_instance = None
        self.os_api_instance = None
        self.ds_api_instance = None
        self.ad_api_instance = None
        self.metadata_api_instance = None
        self.study_api_instance = None
        self.i_api_instance = None

    @abc.abstractmethod
    def setup(self, config):
        pass

    @abc.abstractmethod
    def create_event_set(self, event_set_id, user=None):

        api_response = self.es_api_instance.create_event_set(event_set_id, user=user)

        return api_response

    @abc.abstractmethod
    def download_event_set(self, eventSetId, user=None):
        return self.es_api_instance.download_event_set(eventSetId, user=user)

    def delete_event_set(self, eventSetId, user=None):
        return self.es_api_instance.delete_event_set(eventSetId, user=user)


    @abc.abstractmethod
    def create_event_set_item(self, event_set_id, sampling_event_id, user=None):
        self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id, user=user)

    @abc.abstractmethod
    def create_location(self, location, user=None):

        created = self.location_api_instance.create_location(location, user=user)

        return created

    @abc.abstractmethod
    def create_sampling_event(self, sampling_event, user=None):
        created = self.se_api_instance.create_sampling_event(sampling_event, user=user)

        return created

    @abc.abstractmethod
    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2, user=None):
        self.se_api_instance.merge_sampling_events(sampling_event_id1, sampling_event_id2, user=user)

    @abc.abstractmethod
    def delete_sampling_event(self, sampling_event_id, user=None):
        self.se_api_instance.delete_sampling_event(sampling_event_id, user=user)

    @abc.abstractmethod
    def download_gps_location(self, latitude, longitude, user=None):

        ret = self.location_api_instance.download_gps_location(latitude, longitude, user=user)
        return ret

    @abc.abstractmethod
    def download_location(self, location_id, user=None):

        ret = self.location_api_instance.download_location(location_id, user=user)

        return ret

    @abc.abstractmethod
    def download_locations_by_attr(self, attr_type, attr_value,
                                   study_name=None, user=None):

        ret = self.location_api_instance.download_locations_by_attr(attr_type,
                                                                    attr_value,
                                                                    study_name, user=user)

        return ret

    def delete_location(self, location_id, user=None):
        ret = self.location_api_instance.delete_location(location_id, user=user)

        return ret

    @abc.abstractmethod
    def download_partner_location(self, partner_name, user=None):

        ret = self.location_api_instance.download_partner_location(partner_name, user=user)
        return ret

    @abc.abstractmethod
    def download_sampling_event(self, sampling_event_id, user=None):

        existing = self.se_api_instance.download_sampling_event(sampling_event_id, user=user)

        return existing

    @abc.abstractmethod
    def download_sampling_events_by_event_set(self, eventSetId, user=None):
        return self.se_api_instance.download_sampling_events_by_event_set(eventSetId, user=user)

    @abc.abstractmethod
    def download_sampling_events_by_attr(self, attr_type, attr_value, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                                   attr_value, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_study(self, study_name, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_study(study_name, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_os_attr(self, attr_type, attr_value, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_os_attr(attr_type,
                                                                                   attr_value, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_location(self, location_id, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_location(location_id, user=user)

        return found_events

    @abc.abstractmethod
    def update_location(self, location_id, location, user=None):

        updated = self.location_api_instance.update_location(location_id, location, user=user)

        return updated

    @abc.abstractmethod
    def update_sampling_event(self, sampling_event_id, sampling_event, user=None):
        ret = self.se_api_instance.update_sampling_event(sampling_event_id, sampling_event, user=user)
        return ret

    @abc.abstractmethod
    def get_country_metadata(self, country_value, user=None):
        metadata = self.metadata_api_instance.get_country_metadata(country_value, user=user)

        return metadata

    @abc.abstractmethod
    def create_original_sample(self, original_sample, user=None):

        return self.os_api_instance.create_original_sample(original_sample, user=user)


    @abc.abstractmethod
    def update_original_sample(self, original_sample_id, original_sample, user=None):

        return self.os_api_instance.update_original_sample(original_sample_id,
                                                                            original_sample, user=user)

    @abc.abstractmethod
    def merge_original_samples(self, original_sample_id1, original_sample_id2, user=None):

        return self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2, user=user)

    @abc.abstractmethod
    def delete_original_sample(self, original_sample_id , user=None):

        return self.os_api_instance.delete_original_sample(original_sample_id, user=user)

    @abc.abstractmethod
    def download_original_sample(self, original_sample_id, user=None):

        return self.os_api_instance.download_original_sample(original_sample_id, user=user)

    @abc.abstractmethod
    def download_original_samples_by_attr(self, attr_type, attr_value, user=None):

        return self.os_api_instance.download_original_samples_by_attr(attr_type, attr_value, user=user)

    @abc.abstractmethod
    def download_original_samples_by_event_set(self, event_set_id, start=None,
                                               count=None, user=None):

        return self.os_api_instance.download_original_samples_by_event_set(event_set_id,
                                                                start, count, user=user)


    @abc.abstractmethod
    def create_derivative_sample(self, derivative_sample, user=None):

        return self.ds_api_instance.create_derivative_sample(derivative_sample, user=user)


    @abc.abstractmethod
    def update_derivative_sample(self, derivative_sample_id, derivative_sample, user=None):

        return self.ds_api_instance.update_derivative_sample(derivative_sample_id,
                                                                            derivative_sample, user=user)

    @abc.abstractmethod
    def delete_derivative_sample(self, derivative_sample_id , user=None):

        return self.ds_api_instance.delete_derivative_sample(derivative_sample_id, user=user)

    @abc.abstractmethod
    def download_derivative_sample(self, derivative_sample_id, user=None):

        return self.ds_api_instance.download_derivative_sample(derivative_sample_id, user=user)

    @abc.abstractmethod
    def download_derivative_samples_by_attr(self, attr_type, attr_value, user=None):

        return self.ds_api_instance.download_derivative_samples_by_attr(attr_type, attr_value, user=user)

    @abc.abstractmethod
    def download_derivative_samples_by_attr(self, attr_type, attr_value, user=None):

        return self.ds_api_instance.download_derivative_samples_by_os_attr(attr_type, attr_value, user=user)


    @abc.abstractmethod
    def create_assay_datum(self, assay_datum, user=None):

        return self.ad_api_instance.create_assay_datum(assay_datum, user=user)


    @abc.abstractmethod
    def update_assay_datum(self, assay_datum_id, assay_datum, user=None):

        return self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum, user=user)

    @abc.abstractmethod
    def delete_assay_datum(self, assay_datum_id, user=None):

        return self.ad_api_instance.delete_assay_datum(assay_datum_id, user=user)

    @abc.abstractmethod
    def download_assay_data_by_attr(self, attr_type, attr_value, user=None):

        return self.ad_api_instance.download_assay_data_by_attr(attr_type, attr_value, user=user)

    @abc.abstractmethod
    def download_study(self, study_code, user=None):
        return self.study_api_instance.download_study(study_code, user=user)

    @abc.abstractmethod
    def download_studies(self, user=None):
        return self.study_api_instance.download_studies(user=user)

    @abc.abstractmethod
    def update_study(self, study_code, study_detail, user=None):
        return self.study_api_instance.update_study(study_code, study_detail, user=user)

    @abc.abstractmethod
    def create_individual(self, individual, user=None):

        return self.i_api_instance.create_individual(individual, user=user)


    @abc.abstractmethod
    def update_individual(self, individual_id, individual, user=None):

        return self.i_api_instance.update_individual(individual_id, individual, user=user)

    @abc.abstractmethod
    def merge_individuals(self, individual_id1, individual_id2, user=None):

        return self.i_api_instance.merge_individuals(individual_id1, individual_id2, user=user)

    @abc.abstractmethod
    def delete_individual(self, individual_id , user=None):

        return self.i_api_instance.delete_individual(individual_id, user=user)

    @abc.abstractmethod
    def download_individual(self, individual_id, user=None):

        return self.i_api_instance.download_individual(individual_id, user=user)

    @abc.abstractmethod
    def download_individuals_by_attr(self, prop_name, prop_value,
                                     study_name=None, user=None):

        return self.i_api_instance.download_individuals_by_attr(prop_name,
                                                                prop_value,
                                                                study_name=study_name, user=user)

    @abc.abstractmethod
    def download_history(self, record_type, record_id, user=None):
        history = self.metadata_api_instance.download_history(record_type,
                                                              record_id, user=user)

        return history
