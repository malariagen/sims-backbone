import openapi_client
from openapi_client.rest import ApiException

from test_base import TestBase

import copy
import uuid

import pytest

class TestLocation(TestBase):

    _location_number = 0.1234

    def get_next_location(self):

        loc = openapi_client.Location(None)

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
    def test_create_loc_with_attrs(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5002-PF-MR-ANON'),
                openapi_client.Attr(attr_type='src_location_id',
                                    attr_value='roma_loc_1',
                                    study_name='5002-PF-MR-ANON'),
            ]

            created = api_instance.create_location(loc)
            if not api_factory.is_authorized(None):
                pytest.fail('Unauthorized call to create_location succeeded')

            fetched = api_instance.download_location(created.location_id)
            assert created == fetched, "create response != download response"
            fetched.location_id = None
            assert loc == fetched, "upload != download response"

            downloaded = api_instance.download_locations_by_attr(loc.attrs[1].attr_type,
                                                    loc.attrs[1].attr_value)

            assert downloaded.count == 1
            assert downloaded.locations[0] == created

            downloaded = api_instance.download_locations_by_attr(loc.attrs[1].attr_type,
                                                    loc.attrs[1].attr_value,
                                                    study_name=loc.attrs[1].study_name)

            assert downloaded.count == 1
            assert downloaded.locations[0] == created
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

            created1 = api_instance.create_location(loc)

            assert created.location_id != created1.location_id

            api_instance.delete_location(created.location_id)
            api_instance.delete_location(created1.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_create_duplicate_ident(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            ident = openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5003-PF-MR-ANON')
            loc.attrs = [
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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5002-PF-MR-ANON'),
            ]

            loc1 = openapi_client.Location(None, latitude=28.46362,
                                           longitude=91.49542, accuracy='country',
                                           curated_name='Trongsa, Trongsa, Bhutan',
                                           notes='pv_3_locations.txt',
                                           country='BTN')
            loc1.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5002-PF-MR-ANON'),
            ]

            created = api_instance.create_location(loc)

            created1 = api_instance.create_location(loc1)

            assert created.location_id != created1.location_id

            api_instance.delete_location(created.location_id)
            api_instance.delete_location(created1.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    """
    def test_duplicate_study_name(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5002-PF-MR-ANON'),
                openapi_client.Attr(attr_type='partner_name', attr_value='location name', study_name='5002')
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

            loc = openapi_client.Location(None, 15.82083, -9.4145, None, None, None, None)
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='Kobeni', study_name='5002-PF-MR-ANON')
            ]
            created = api_instance.create_location(loc)

            looked_up = api_instance.download_gps_location(15.82083, -9.4145)

            fetched = looked_up.locations[0]

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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_gps_location(loc.latitude, loc.longitude)

            fetched = looked_up.locations[0]

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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.attrs[0].attr_value)
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
                looked_up_locs = api_instance.download_partner_location('404')

                assert not looked_up_locs.locations
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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='5000-PV')
            ]
            created = api_instance.create_location(loc)
            loc1 = self.get_next_location()
            loc1.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='5001-PV')
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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='5000-PV')
            ]
            created = api_instance.create_location(loc)
            loc1 = self.get_next_location()
            loc1.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='5001-PV')
            ]
            created1 = api_instance.create_location(loc1)
            looked_up_locs = api_instance.download_partner_location(loc.attrs[0].attr_value)
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
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.attrs[0].attr_value)
            looked_up = looked_up_locs.locations[0]
            newloc = self.get_next_location()
            newloc.country = 'IND'
            newloc.accuracy = 'region'
            newloc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='nepal', study_name='1235-PV')
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
    def test_update_attrs(self, api_factory):

        api_instance = api_factory.LocationApi()

        try:

            loc = self.get_next_location()
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.attrs[0].attr_value)
            looked_up = looked_up_locs.locations[0]
            newloc = copy.deepcopy(loc)
            newloc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='nepal', study_name='1235-PV')
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
            loc = openapi_client.Location(None, latitude=27.46362,
                                          longitude=90.49542, accuracy='country',
                                          curated_name='Trongsa, Trongsa, Bhutan', notes='pv_3_locations.txt',
                                          country='BTN')
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.attrs[0].attr_value)
            looked_up = looked_up_locs.locations[0]
            newloc = openapi_client.Location(None, latitude=28.46362,
                                             longitude=91.49542, accuracy='location',
                                             curated_name='new_Trongsa, Trongsa, Bhutan',
                                             notes='new_pv_3_locations.txt',
                                             country='IND')
            new_created = api_instance.create_location(newloc)
            with pytest.raises(ApiException, status=422):
                created.location_id = new_created.location_id
                updated = api_instance.update_location(new_created.location_id, created)


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
            newloc = openapi_client.Location(None, 28.46362, 91.49542, 'location',
                                             curated_name='new_Trongsa, Trongsa, Bhutan',
                                             notes='new_pv_3_locations.txt',
                                             country='IND')
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
    def test_get_location_attrs(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()
        api_instance = api_factory.LocationApi()

        try:
            loc = self.get_next_location()
            loc = openapi_client.Location(None, latitude=27.46362,
                                          longitude=90.49542, accuracy='country',
                                          curated_name='Trongsa, Trongsa, Bhutan',
                                          notes='pv_3_locations.txt', country='BTN')
            loc.attrs = [
                openapi_client.Attr(attr_type='partner_name', attr_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)

            idents = metadata_api_instance.get_location_attr_types()

            assert 'partner_name' in idents

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)


    """
    Used to check permissions
    """
    def test_get_location_attr_types(self, api_factory):

        metadata_api_instance = api_factory.MetadataApi()

        try:

            idents = metadata_api_instance.get_location_attr_types()

        except ApiException as error:
            self.check_api_exception(api_factory, "LocationApi->create_location", error)

