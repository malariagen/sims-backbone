import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase

import copy
import uuid

import pytest

class TestIndividual(TestBase):

    _individual_number = 1

    def get_next_individual(self):

        indiv = openapi_client.Individual(None)

        ident = openapi_client.Attr(attr_type='patient_id',
                                    attr_value=f'Patient{self._individual_number}',
                                    attr_source='TestIndividual',
                                    study_name='6003-PF-MR-ANON')
        indiv.attrs = [
            ident
        ]

        self._individual_number = self._individual_number + 1

        return indiv

    """
    """
    def test_create(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()

            created = api_instance.create_individual(indiv)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_individual succeeded')

            fetched = api_instance.download_individual(created.individual_id)
            assert created == fetched, "create response != download response"
            fetched.individual_id = None
            assert indiv == fetched, "upload != download response"
            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)


    """
    """
    def test_delete(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)
            api_instance.delete_individual(created.individual_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)


    """
    """
    def test_delete_missing(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_individual(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_individual(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->delete_individual", error)

    """
    """
    def test_duplicate_key(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)

            newindiv = copy.deepcopy(indiv)
            newindiv.attrs[0].study_name = '6004'
            created1 = api_instance.create_individual(newindiv)

            assert created.individual_id != created1.individual_id

            api_instance.delete_individual(created.individual_id)
            api_instance.delete_individual(created1.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)


    """
    """
    def test_create_duplicate_ident(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            indiv.attrs.append(indiv.attrs[0])

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.create_individual(indiv)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)


    """
    """
    def test_download_individuals(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)
            indiv1 = self.get_next_individual()
            created1 = api_instance.create_individual(indiv1)
            looked_up_indivs = api_instance.download_individuals()
            assert looked_up_indivs.count == 2, 'Wrong number of individuals'
            looked_up = looked_up_indivs.individuals[0]

            looked_up_indivs = api_instance.download_individuals(start=0, count=1)
            assert looked_up_indivs.count == 2, 'Wrong number of individuals'
            assert len(looked_up_indivs.individuals) == 1, 'Wrong number of individuals'

            looked_up_indivs = api_instance.download_individuals(study_name=indiv1.attrs[0].study_name)
            assert looked_up_indivs.count == 2, 'Wrong number of individuals'
            assert len(looked_up_indivs.individuals) == 2, 'Wrong number of individuals'

            looked_up_indivs = api_instance.download_individuals(orderby='study_name')
            assert looked_up_indivs.count == 2, 'Wrong number of individuals'
            assert len(looked_up_indivs.individuals) == 2, 'Wrong number of individuals'

            looked_up_indivs = api_instance.download_individuals(study_name='XXXXX')
            assert looked_up_indivs.count == 0, 'Wrong number of individuals'
            assert len(looked_up_indivs.individuals) == 0, 'Wrong number of individuals'

            looked_up_indivs = api_instance.download_individuals(start=10, count=2)
            assert looked_up_indivs.count == 2, 'Wrong number of individuals'
            assert len(looked_up_indivs.individuals) == 0, 'Wrong number of individuals'

            api_instance.delete_individual(created.individual_id)
            api_instance.delete_individual(created1.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_download_individual_permission(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    looked_up_indivs = api_instance.download_individual(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->download_individual", error)

    """
    """
    def test_download_individuals_permission(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    looked_up_indivs = api_instance.download_individuals()

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->download_individual", error)


    """
    """
    def test_update(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)

            newindiv = self.get_next_individual()

            updated = api_instance.update_individual(created.individual_id, newindiv)
            fetched = api_instance.download_individual(created.individual_id)
            assert updated == fetched, "update response != download response"
            fetched.individual_id = None
            assert newindiv == fetched, "update != download response"
            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_update_attrs(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)
            newindiv = copy.deepcopy(indiv)
            newindiv.attrs = [
                openapi_client.Attr(attr_type='individual_id',
                                    attr_value='indiv', study_name='1235-PV')
            ]
            updated = api_instance.update_individual(created.individual_id, newindiv)
            fetched = api_instance.download_individual(created.individual_id)
            assert updated == fetched, "update response != download response"
            fetched.individual_id = None
            assert newindiv == fetched, "update != download response"
            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_update_duplicate(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)
            original_id = created.individual_id
            newindiv = self.get_next_individual()
            new_created = api_instance.create_individual(newindiv)
            with pytest.raises(ApiException, status=422):
                created.individual_id = new_created.individual_id
                updated = api_instance.update_individual(new_created.individual_id, created)


            api_instance.delete_individual(original_id)
            api_instance.delete_individual(new_created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_update_missing(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            indiv = self.get_next_individual()
            fake_id = uuid.uuid4()
            indiv.individual_id = str(fake_id)

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_individual(indiv.individual_id, indiv)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_individual(indiv.individual_id, indiv)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->update_individual", error)

    """
    """
    def test_get_by_attr(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:
            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)

            fetched = api_instance.download_individuals_by_attr(indiv.attrs[0].attr_type,indiv.attrs[0].attr_value,indiv.attrs[0].study_name)

            assert len(fetched.individuals) == 1
            assert fetched.individuals[0].individual_id == created.individual_id

            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_get_by_attr_missing(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:

            if api_factory.is_authorized(None):
                fetched = api_instance.download_individuals_by_attr('','')

                assert not fetched.individuals
                assert fetched.count == 0
            else:
                with pytest.raises(ApiException, status=403):
                    fetched = api_instance.download_individuals_by_attr('','')

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_merge_individual(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:
            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)
            indiv1 = self.get_next_individual()
            created1 = api_instance.create_individual(indiv1)

            merged_res = api_instance.merge_individuals(created.individual_id,
                                                    created1.individual_id)

            merged = api_instance.download_individual(merged_res.individual_id)

            assert merged_res == merged

            assert len(merged.attrs) == len(indiv.attrs) + len(indiv1.attrs)

            assert merged.attrs[0] != merged.attrs[1]

            with pytest.raises(ApiException, status=404):
                api_instance.delete_individual(created1.individual_id)
            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)

    """
    """
    def test_merge_individual_missing(self, api_factory):

        api_instance = api_factory.IndividualApi()

        try:
            indiv = self.get_next_individual()
            created = api_instance.create_individual(indiv)

            with pytest.raises(ApiException, status=404):
                merged_res = api_instance.merge_individuals(str(uuid.uuid4()),
                                                        created.individual_id)

            with pytest.raises(ApiException, status=404):
                merged_res = api_instance.merge_individuals(created.individual_id,
                                                            str(uuid.uuid4()))
            with pytest.raises(ApiException, status=404):
                merged_res = api_instance.merge_individuals(str(uuid.uuid4()),
                                                            str(uuid.uuid4()))


            api_instance.delete_individual(created.individual_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "IndividualApi->create_individual", error)
#
#    """
#    Used to check permissions
#    """
#    def test_get_individual_attr_types(self, api_factory):
#
#        metadata_api_instance = api_factory.MetadataApi()
#
#        try:
#
#            idents = metadata_api_instance.get_individual_attr_types()
#
#        except ApiException as error:
#            self.check_api_exception(api_factory,
#                                     "IndividualApi->create_individual", error)
#
