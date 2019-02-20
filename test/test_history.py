import openapi_client
from openapi_client.rest import ApiException

from openapi_server.models.sampling_event import SamplingEvent  # noqa: E501
from openapi_server.models.original_sample import OriginalSample  # noqa: E501
from openapi_server.models.derivative_sample import DerivativeSample  # noqa: E501
from flask.json import JSONDecoder
from test_base import TestBase
from datetime import date

import urllib
import pytest
import json

class TestHistory(TestBase):



    def create_test_samples(self, api_factory):

        created_es = None
        created_se = None
        created = None
        created1 = None
        created2 = None

        try:

            api_instance = api_factory.OriginalSampleApi()
            se_api_instance = api_factory.SamplingEventApi()
            es_api_instance = api_factory.EventSetApi()
            ds_api_instance = api_factory.DerivativeSampleApi()
            study_api = api_factory.StudyApi()

            event_set_name = 'test_hist_event_set_lookup'
            study_name = '8004-MD-UP'

            created_es = es_api_instance.create_event_set(event_set_name)

            sampling_event = openapi_client.SamplingEvent(None, date(2017, 10, 10),
                                                          doc_accuracy='month')

            created_se = se_api_instance.create_sampling_event(sampling_event)

            es_api_instance.create_event_set_item(event_set_name, created_se.sampling_event_id)

            samp = openapi_client.OriginalSample(None, study_name=study_name,
                                                 partner_species='PF')
            samp.attrs = [
                openapi_client.Attr(attr_type='ds_os_attr', attr_value='123456')
            ]
            created = api_instance.create_original_sample(samp)
            study_detail = study_api.download_study(study_name)
            study_detail.partner_species[0].taxa = [openapi_client.Taxonomy(taxonomy_id=5833)]
            study_api.update_study(study_name, study_detail)

            samp1 = openapi_client.DerivativeSample(None)
            samp2 = openapi_client.DerivativeSample(None)

            samp1.attrs = [
                openapi_client.Attr(attr_type='test1', attr_value='test1',
                                    attr_source='ds_os_attr')
            ]
            samp2.attrs = [
                openapi_client.Attr(attr_type='test2', attr_value='test2',
                                    attr_source='ds_os_attr')
            ]
            samp1.original_sample_id = created.original_sample_id
            samp2.original_sample_id = created.original_sample_id

            created1 = ds_api_instance.create_derivative_sample(samp1)
            created2 = ds_api_instance.create_derivative_sample(samp2)

            created.sampling_event_id = created_se.sampling_event_id

            api_instance.update_original_sample(created.original_sample_id,
                                                created)

        except ApiException as error:
            self.check_api_exception(api_factory, "OriginalSampleApi->create_original_sample", error)

        return created_es, created_se, created, created1, created2

    def delete_test_samples(self, api_factory, created_es, created_se, created, created1, created2):

        api_instance = api_factory.OriginalSampleApi()
        se_api_instance = api_factory.SamplingEventApi()
        es_api_instance = api_factory.EventSetApi()
        ds_api_instance = api_factory.DerivativeSampleApi()

        se_api_instance.delete_sampling_event(created_se.sampling_event_id)

        es_api_instance.delete_event_set(created_es.event_set_name)

        ds_api_instance.delete_derivative_sample(created1.derivative_sample_id)
        ds_api_instance.delete_derivative_sample(created2.derivative_sample_id)
        api_instance.delete_original_sample(created.original_sample_id)

    def test_se_history(self, api_factory):

        created_es, created_se, created, created1, created2 = self.create_test_samples(api_factory)

        if api_factory.is_authorized(None):
            metadata_api_instance = api_factory.MetadataApi()

            se_history = metadata_api_instance.download_history('sampling_event',
                                                                created_se.sampling_event_id)

            assert len(se_history.log_items) == 1

            for log_item in se_history.log_items:
                se = SamplingEvent.from_dict(json.loads(log_item.output_value,
                                                        cls=JSONDecoder))
                assert se.sampling_event_id == created_se.sampling_event_id
                assert log_item.action == 'create_sampling_event'
                assert log_item.result == 201
                assert log_item.action_date == date.today()


            self.delete_test_samples(api_factory, created_es, created_se, created, created1, created2)
        else:
            assert not created_es


    def test_os_history(self, api_factory):

        created_es, created_se, created_os, created1, created2 = self.create_test_samples(api_factory)

        if api_factory.is_authorized(None):
            metadata_api_instance = api_factory.MetadataApi()

            os_history = metadata_api_instance.download_history('original_sample',
                                                                created_os.original_sample_id)

            assert len(os_history.log_items) == 2

            for log_item in os_history.log_items:
                se = OriginalSample.from_dict(json.loads(log_item.output_value,
                                                        cls=JSONDecoder))
                assert se.original_sample_id == created_os.original_sample_id
                assert log_item.action_date == date.today()


            assert os_history.log_items[0].action == 'create_original_sample'
            assert os_history.log_items[1].action == 'update_original_sample'
            assert os_history.log_items[0].result == 201
            assert os_history.log_items[1].result == 200

            self.delete_test_samples(api_factory, created_es, created_se,
                                     created_os, created1, created2)
        else:
            assert not created_es

    def test_ds_history(self, api_factory):

        created_es, created_se, created, created1, created2 = self.create_test_samples(api_factory)

        if api_factory.is_authorized(None):
            metadata_api_instance = api_factory.MetadataApi()

            ds_history = metadata_api_instance.download_history('derivative_sample',
                                                                created1.derivative_sample_id)

            assert len(ds_history.log_items) == 1

            samples = []

            for log_item in ds_history.log_items:
                ds = DerivativeSample.from_dict(json.loads(log_item.output_value,
                                                        cls=JSONDecoder))
                samples.append(ds)
                assert log_item.action == 'create_derivative_sample'
                assert log_item.result == 201
                assert log_item.action_date == date.today()

            #Can't compare objects because one is a server object, and one a client object
            assert samples[0].derivative_sample_id == created1.derivative_sample_id

            self.delete_test_samples(api_factory, created_es, created_se, created, created1, created2)
        else:
            assert not created_es
