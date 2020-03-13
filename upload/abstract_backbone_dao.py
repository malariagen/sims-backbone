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
    def create_event_set(self, event_set_id, studies=None, user=None):

        api_response = self.es_api_instance.create_event_set(event_set_id, studies=None, user=user)

        return api_response

    @abc.abstractmethod
    def download_event_set(self, eventSetId, studies=None, user=None):
        return self.es_api_instance.download_event_set(eventSetId, studies=None, user=user)

    def delete_event_set(self, eventSetId, studies=None, user=None):
        return self.es_api_instance.delete_event_set(eventSetId, studies=None, user=user)


    @abc.abstractmethod
    def create_event_set_item(self, event_set_id, sampling_event_id, studies=None, user=None):
        self.es_api_instance.create_event_set_item(event_set_id, sampling_event_id, studies=None, user=user)

    @abc.abstractmethod
    def create_location(self, location, studies=None, user=None):

        created = self.location_api_instance.create_location(location, studies=None, user=user)

        return created

    @abc.abstractmethod
    def create_sampling_event(self, sampling_event, studies=None, user=None):
        created = self.se_api_instance.create_sampling_event(sampling_event, studies=None, user=user)

        return created

    @abc.abstractmethod
    def merge_sampling_events(self, sampling_event_id1, sampling_event_id2, studies=None, user=None):
        self.se_api_instance.merge_sampling_events(sampling_event_id1, sampling_event_id2, studies=None, user=user)

    @abc.abstractmethod
    def delete_sampling_event(self, sampling_event_id, studies=None, user=None):
        self.se_api_instance.delete_sampling_event(sampling_event_id, studies=None, user=user)

    @abc.abstractmethod
    def download_gps_location(self, latitude, longitude, studies=None, user=None):

        ret = self.location_api_instance.download_gps_location(latitude, longitude, studies=None, user=user)
        return ret

    @abc.abstractmethod
    def download_location(self, location_id, studies=None, user=None):

        ret = self.location_api_instance.download_location(location_id, studies=None, user=user)

        return ret

    @abc.abstractmethod
    def download_locations_by_attr(self, attr_type, attr_value,
                                   study_name=None, value_type=None,
                                   start=None, count=None, studies=None, user=None):

        ret = self.location_api_instance.download_locations_by_attr(attr_type,
                                                                    attr_value,
                                                                    study_name,
                                                                    value_type=value_type,
                                                                    start=start,
                                                                    count=count, studies=None, user=user)

        return ret

    def delete_location(self, location_id, studies=None, user=None):
        ret = self.location_api_instance.delete_location(location_id, studies=None, user=user)

        return ret

    @abc.abstractmethod
    def download_partner_location(self, partner_name, studies=None, user=None):

        ret = self.location_api_instance.download_partner_location(partner_name, studies=None, user=user)
        return ret

    @abc.abstractmethod
    def download_sampling_event(self, sampling_event_id, studies=None, user=None):

        existing = self.se_api_instance.download_sampling_event(sampling_event_id, studies=None, user=user)

        return existing

    @abc.abstractmethod
    def download_sampling_events_by_event_set(self, eventSetId, studies=None, user=None):
        return self.se_api_instance.download_sampling_events_by_event_set(eventSetId, studies=None, user=user)

    @abc.abstractmethod
    def download_sampling_events_by_attr(self, attr_type, attr_value,
                                         value_type=None, start=None,
                                         count=None, studies=None, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_attr(attr_type,
                                                                             attr_value,
                                                                             value_type=value_type,
                                                                             start=start,
                                                                             count=count, studies=None, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_study(self, study_name, start=None,
                                          count=None, studies=None, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_study(study_name,
                                                                              start=None,
                                                                              count=None, studies=None, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_os_attr(self, attr_type, attr_value,
                                            value_type=None, start=None,
                                            count=None, studies=None, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_os_attr(attr_type,
                                                                                attr_value,
                                                                                value_type=value_type,
                                                                                start=start,
                                                                                count=count, studies=None, user=user)

        return found_events

    @abc.abstractmethod
    def download_sampling_events_by_location(self, location_id, studies=None, user=None):

        found_events = self.se_api_instance.download_sampling_events_by_location(location_id, studies=None, user=user)

        return found_events

    @abc.abstractmethod
    def update_location(self, location_id, location, studies=None, user=None):

        updated = self.location_api_instance.update_location(location_id, location, studies=None, user=user)

        return updated

    @abc.abstractmethod
    def update_sampling_event(self, sampling_event_id, sampling_event, studies=None, user=None):
        ret = self.se_api_instance.update_sampling_event(sampling_event_id, sampling_event, studies=None, user=user)
        return ret

    @abc.abstractmethod
    def get_country_metadata(self, country_value, studies=None, user=None):
        metadata = self.metadata_api_instance.get_country_metadata(country_value, studies=None, user=user)

        return metadata

    @abc.abstractmethod
    def create_original_sample(self, original_sample, studies=None, user=None):

        return self.os_api_instance.create_original_sample(original_sample, studies=None, user=user)


    @abc.abstractmethod
    def update_original_sample(self, original_sample_id, original_sample, studies=None, user=None):

        return self.os_api_instance.update_original_sample(original_sample_id,
                                                                            original_sample, studies=None, user=user)

    @abc.abstractmethod
    def merge_original_samples(self, original_sample_id1, original_sample_id2, studies=None, user=None):

        return self.os_api_instance.merge_original_samples(original_sample_id1,
                                                                            original_sample_id2, studies=None, user=user)

    @abc.abstractmethod
    def delete_original_sample(self, original_sample_id , studies=None, user=None):

        return self.os_api_instance.delete_original_sample(original_sample_id, studies=None, user=user)

    @abc.abstractmethod
    def download_original_sample(self, original_sample_id, studies=None, user=None):

        return self.os_api_instance.download_original_sample(original_sample_id, studies=None, user=user)

    @abc.abstractmethod
    def download_original_samples(self, search_filter, studies=None, user=None):
        pass

    @abc.abstractmethod
    def download_original_samples_by_attr(self, attr_type, attr_value,
                                          value_type=None, start=None,
                                          count=None, studies=None, user=None):

        return self.os_api_instance.download_original_samples_by_attr(attr_type,
                                                                      attr_value,
                                                                      value_type=value_type,
                                                                      start=start,
                                                                      count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_original_samples_by_study(self, study_name, start=None,
                                           count=None, studies=None, user=None):

        return self.os_api_instance.download_original_samples_by_study(study_name,
                                                                       start=start,
                                                                       count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_original_samples_by_event_set(self, event_set_id, start=None,
                                               count=None, studies=None, user=None):

        return self.os_api_instance.download_original_samples_by_event_set(event_set_id,
                                                                start, count, studies=None, user=user)


    @abc.abstractmethod
    def create_derivative_sample(self, derivative_sample, studies=None, user=None):

        return self.ds_api_instance.create_derivative_sample(derivative_sample, studies=None, user=user)


    @abc.abstractmethod
    def update_derivative_sample(self, derivative_sample_id, derivative_sample, studies=None, user=None):

        return self.ds_api_instance.update_derivative_sample(derivative_sample_id,
                                                                            derivative_sample, studies=None, user=user)

    @abc.abstractmethod
    def delete_derivative_sample(self, derivative_sample_id , studies=None, user=None):

        return self.ds_api_instance.delete_derivative_sample(derivative_sample_id, studies=None, user=user)

    @abc.abstractmethod
    def download_derivative_sample(self, derivative_sample_id, studies=None, user=None):

        return self.ds_api_instance.download_derivative_sample(derivative_sample_id, studies=None, user=user)

    @abc.abstractmethod
    def download_derivative_samples_by_attr(self, attr_type, attr_value,
                                            value_type=None, start=None,
                                            count=None, studies=None, user=None):

        return self.ds_api_instance.download_derivative_samples_by_attr(attr_type,
                                                                        attr_value,
                                                                        value_type=value_type,
                                                                        start=start,
                                                                        count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_derivative_samples_by_study(self, study_name, start=None, count=None, studies=None, user=None):

        return self.ds_api_instance.download_derivative_samples_by_study(study_name,
                                                                         start=start,
                                                                         count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_derivative_samples_by_os_attr(self, attr_type, attr_value,
                                               value_type=None,
                                               start=None, count=None, studies=None, user=None):

        return self.ds_api_instance.download_derivative_samples_by_os_attr(attr_type,
                                                                           attr_value,
                                                                           value_type=value_type,
                                                                           start=start,
                                                                           count=count, studies=None, user=user)


    @abc.abstractmethod
    def create_assay_datum(self, assay_datum, studies=None, user=None):

        return self.ad_api_instance.create_assay_datum(assay_datum, studies=None, user=user)


    @abc.abstractmethod
    def update_assay_datum(self, assay_datum_id, assay_datum, studies=None, user=None):

        return self.ad_api_instance.update_assay_datum(assay_datum_id, assay_datum, studies=None, user=user)

    @abc.abstractmethod
    def delete_assay_datum(self, assay_datum_id, studies=None, user=None):

        return self.ad_api_instance.delete_assay_datum(assay_datum_id, studies=None, user=user)

    @abc.abstractmethod
    def download_assay_data_by_attr(self, attr_type, attr_value,
                                    value_type=None, start=None, count=None, studies=None, user=None):

        return self.ad_api_instance.download_assay_data_by_attr(attr_type,
                                                                attr_value,
                                                                value_type=value_type,
                                                                start=start,
                                                                count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_study(self, study_code, studies=None, user=None):
        return self.study_api_instance.download_study(study_code, studies=None, user=user)

    @abc.abstractmethod
    def download_studies(self, studies=None, user=None):
        return self.study_api_instance.download_studies(studies=None, user=user)

    @abc.abstractmethod
    def update_study(self, study_code, study_detail, studies=None, user=None):
        return self.study_api_instance.update_study(study_code, study_detail, studies=None, user=user)

    @abc.abstractmethod
    def create_individual(self, individual, studies=None, user=None):

        return self.i_api_instance.create_individual(individual, studies=None, user=user)


    @abc.abstractmethod
    def update_individual(self, individual_id, individual, studies=None, user=None):

        return self.i_api_instance.update_individual(individual_id, individual, studies=None, user=user)

    @abc.abstractmethod
    def merge_individuals(self, individual_id1, individual_id2, studies=None, user=None):

        return self.i_api_instance.merge_individuals(individual_id1, individual_id2, studies=None, user=user)

    @abc.abstractmethod
    def delete_individual(self, individual_id , studies=None, user=None):

        return self.i_api_instance.delete_individual(individual_id, studies=None, user=user)

    @abc.abstractmethod
    def download_individual(self, individual_id, studies=None, user=None):

        return self.i_api_instance.download_individual(individual_id, studies=None, user=user)

    @abc.abstractmethod
    def download_individuals(self, search_filter, study_name=None, studies=None, user=None):
        pass

    @abc.abstractmethod
    def download_individuals_by_attr(self, prop_name, prop_value,
                                     study_name=None, value_type=None,
                                     start=None, count=None, studies=None, user=None):

        return self.i_api_instance.download_individuals_by_attr(prop_name,
                                                                prop_value,
                                                                study_name=study_name,
                                                                value_type=value_type,
                                                                start=start,
                                                                count=count, studies=None, user=user)

    @abc.abstractmethod
    def download_history(self, record_type, record_id, studies=None, user=None):
        history = self.metadata_api_instance.download_history(record_type,
                                                              record_id, studies=None, user=user)

        return history
