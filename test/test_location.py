import swagger_client
from swagger_client.rest import ApiException

from test_base import TestBase

import copy
import uuid

import pytest

class TestLocation(TestBase):

    _location_number = 0.1234

    def get_next_location(self):
    
        loc = swagger_client.Location(None)

        loc.latitude = self._location_number
        loc.longitude = self._location_number
        loc.curated_name = 'Test Location{}'.format(self._location_number)
        loc.country = 'BTN'
        loc.notes = 'Generated location'

        self._location_number = self._location_number + 1

        return loc

    """
    """
    def test_create(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()

            created = api_instance.create_location(loc)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_location succeeded')

            fetched = api_instance.download_location(created.location_id)
            assert created == fetched, "create response != download response"
            fetched.location_id = None
            assert loc == fetched, "upload != download response"
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_delete(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            created = api_instance.create_location(loc)
            api_instance.delete_location(created.location_id)
            with pytest.raises(ApiException, status=404):
                fetched = api_instance.download_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_delete_missing(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    api_instance.delete_location(str(uuid.uuid4()))
            else:
                with pytest.raises(ApiException, status=403):
                    api_instance.delete_location(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->delete_location", error)

    """
    """
    def test_duplicate_key(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            created = api_instance.create_location(loc)

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_location(loc)

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_create_duplicate_ident(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            ident = swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5003-PF-MR-ANON')
            loc.identifiers = [
                ident,
                ident
            ]

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.create_location(loc)

            with pytest.raises(ApiException, status=404):
                looked_up = api_instance.download_gps_location(loc.latitude, loc.longitude)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_duplicate_partner_name(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON'),
            ]

            loc1 = swagger_client.Location(None, 28.46362, 91.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BTN')
            loc1.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON'),
            ]

            created = api_instance.create_location(loc)

            with pytest.raises(ApiException, status=422):
                created1 = api_instance.create_location(loc1)
                api_instance.delete_location(created1.location_id)

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_duplicate_study_name(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON'),
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='location name', study_name='5002')
            ]

            with pytest.raises(ApiException, status=422):
                created = api_instance.create_location(loc)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_gps_lookup_negative(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = swagger_client.Location(None, 15.82083, -9.4145, None, None, None, None)
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON')
            ]
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_gps_location(15.82083, -9.4145)

            fetched = api_instance.download_location(looked_up.location_id)
            assert created == fetched, "create response != download response"
            fetched.location_id = None
            assert loc == fetched, "upload != download response"
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_gps_lookup(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_gps_location(loc.latitude, loc.longitude)

            fetched = api_instance.download_location(looked_up.location_id)
            assert created == fetched, "create response != download response"
            fetched.location_id = None
            assert loc == fetched, "upload != download response"
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_gps_lookup_not_found(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:


            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    looked_up = api_instance.download_gps_location(27.46362, 90.49542)
            else:
                with pytest.raises(ApiException, status=403):
                    looked_up = api_instance.download_gps_location(27.46362, 90.49542)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->download_gps_location", error)

    """
    """
    def test_gps_lookup_invalid(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            with pytest.raises(ApiException, status=422):
                looked_up = api_instance.download_gps_location('27.46362', 'y90.49542')

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->download_gps_location", error)

    """
    """
    def test_partner_lookup(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            looked_up = looked_up_locs.locations[0]

            fetched = api_instance.download_location(looked_up.location_id)
            assert created == fetched, "create response != download response"
            fetched.location_id = None
            assert loc == fetched, "upload != download response"
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_partner_lookup_missing(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    looked_up_locs = api_instance.download_partner_location('404')
            else:
                with pytest.raises(ApiException, status=403):
                    looked_up_locs = api_instance.download_partner_location('404')

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->download_partner_location", error)

    """
    """
    def test_download_locations(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='5000-PV')
            ]
            created = api_instance.create_location(loc)
            loc1 = self.get_next_location()
            loc1.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='5001-PV')
            ]
            created1 = api_instance.create_location(loc1)
            looked_up_locs = api_instance.download_locations()
            assert looked_up_locs.count == 2, 'Wrong number of locations'
            looked_up = looked_up_locs.locations[0]

            looked_up_locs = api_instance.download_locations(start=0, count=1)
            assert looked_up_locs.count == 2, 'Wrong number of locations'
            assert len(looked_up_locs.locations) == 1, 'Wrong number of locations'

            looked_up_locs = api_instance.download_locations(start=10, count=2)
            assert looked_up_locs.count == 2, 'Wrong number of locations'
            assert len(looked_up_locs.locations) == 0, 'Wrong number of locations'

            api_instance.delete_location(created.location_id)
            api_instance.delete_location(created1.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_download_location_permission(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    looked_up_locs = api_instance.download_location(str(uuid.uuid4()))

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->download_location", error)

    """
    """
    def test_download_locations_permission(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            if not api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=403):
                    looked_up_locs = api_instance.download_locations()

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->download_location", error)

    """
    """
    def test_partner_lookup_multiple(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='5000-PV')
            ]
            created = api_instance.create_location(loc)
            loc1 = self.get_next_location()
            loc1.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='5001-PV')
            ]
            created1 = api_instance.create_location(loc1)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            assert looked_up_locs.count == 2, 'Wrong number of locations'
            looked_up = looked_up_locs.locations[0]

            api_instance.delete_location(created.location_id)
            api_instance.delete_location(created1.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            looked_up = looked_up_locs.locations[0]
            newloc = self.get_next_location()
            newloc.country = 'IND'
            newloc.accuracy = 'region'
            newloc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='nepal', study_name='1235-PV')
            ]
            updated = api_instance.update_location(looked_up.location_id, newloc)
            fetched = api_instance.download_location(looked_up.location_id)
            assert updated == fetched, "update response != download response"
            fetched.location_id = None
            assert newloc == fetched, "update != download response"
            api_instance.delete_location(looked_up.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update_identifiers(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            looked_up = looked_up_locs.locations[0]
            newloc = copy.deepcopy(loc)
            newloc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='nepal', study_name='1235-PV')
            ]
            updated = api_instance.update_location(looked_up.location_id, newloc)
            fetched = api_instance.download_location(looked_up.location_id)
            assert updated == fetched, "update response != download response"
            fetched.location_id = None
            assert newloc == fetched, "update != download response"
            api_instance.delete_location(looked_up.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update_duplicate(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc = swagger_client.Location(None, 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BTN')
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            looked_up = looked_up_locs.locations[0]
            newloc = swagger_client.Location(None, 28.46362, 91.49542, 'location',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
            new_created = api_instance.create_location(newloc)
            with pytest.raises(ApiException, status=422):
                new_created.identifiers = [
                    swagger_client.Identifier(identifier_type='partner_name',
                                              identifier_value='bhutan', study_name='1234-PV')
                ]
                updated = api_instance.update_location(new_created.location_id, new_created)


            api_instance.delete_location(looked_up.location_id)
            api_instance.delete_location(new_created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

    """
    """
    def test_update_missing(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            newloc = swagger_client.Location(None, 28.46362, 91.49542, 'location',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
            fake_id = uuid.uuid4()
            newloc.location_id = str(fake_id)

            if api_factory.is_authorized(None):
                with pytest.raises(ApiException, status=404):
                    updated = api_instance.update_location(newloc.location_id, newloc)
            else:
                with pytest.raises(ApiException, status=403):
                    updated = api_instance.update_location(newloc.location_id, newloc)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->update_location", error)

    """
    """
    def test_get_location_identifiers(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()
        api_instance = api_factory.LocationApi()

        try:
            loc = self.get_next_location()
            loc = swagger_client.Location(None, 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BTN')
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)

            idents = metadata_api_instance.get_location_identifier_types()

            assert 'partner_name' in idents

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    Used to check permissions
    """
    def test_get_location_identifier_types(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()

        try:

            idents = metadata_api_instance.get_location_identifier_types()

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

