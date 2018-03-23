import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase

import copy
import uuid

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
    def test_create(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()

            created = api_instance.create_location(loc)
            fetched = api_instance.download_location(created.location_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.location_id = None
            self.assertEqual(loc, fetched, "upload != download response")
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_create: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_delete(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            created = api_instance.create_location(loc)
            api_instance.delete_location(created.location_id)
            with self.assertRaises(Exception) as context:
                fetched = api_instance.download_location(created.location_id)
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete: Exception when calling LocationApi->create_location: %s\n" % error)


    """
    """
    def test_delete_missing(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                api_instance.delete_location(str(uuid.uuid4()))
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete_missing: Exception when calling LocationApi->delete_location: %s\n" % error)

    """
    """
    def test_duplicate_key(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            created = api_instance.create_location(loc)

            with self.assertRaises(Exception) as context:
                created = api_instance.create_location(loc)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_duplicate_partner_name(self):

        api_instance = swagger_client.LocationApi(self._api_client)

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

            with self.assertRaises(Exception) as context:
                created1 = api_instance.create_location(loc1)
                api_instance.delete_location(created1.location_id)

            self.assertEqual(context.exception.status, 422)
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling LocationApi->create_location: %s\n" % error)


    """
    """
    def test_duplicate_study_name(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON'),
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='location name', study_name='5002')
            ]

            with self.assertRaises(Exception) as context:
                created = api_instance.create_location(loc)

            self.assertEqual(context.exception.status, 422)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling LocationApi->create_location: %s\n" % error)


    """
    """
    def test_gps_lookup_negative(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = swagger_client.Location(None, 15.82083, -9.4145, None, None, None, None)
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='Kobeni', study_name='5002-PF-MR-ANON')
            ]
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_gps_location(15.82083, -9.4145)

            fetched = api_instance.download_location(looked_up.location_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.location_id = None
            self.assertEqual(loc, fetched, "upload != download response")
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_gps_lookup(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_gps_location(loc.latitude, loc.longitude)

            fetched = api_instance.download_location(looked_up.location_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.location_id = None
            self.assertEqual(loc, fetched, "upload != download response")
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_gps_lookup_not_found(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                looked_up = api_instance.download_gps_location(27.46362, 90.49542)

            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_gps_lookup_invalid(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            with self.assertRaises(Exception) as context:
                looked_up = api_instance.download_gps_location('27.46362', 'y90.49542')

            self.assertEqual(context.exception.status, 422)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_partner_lookup(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            looked_up_locs = api_instance.download_partner_location(loc.identifiers[0].identifier_value)
            looked_up = looked_up_locs.locations[0]

            fetched = api_instance.download_location(looked_up.location_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.location_id = None
            self.assertEqual(loc, fetched, "upload != download response")
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_partner_lookup_multiple(self):

        api_instance = swagger_client.LocationApi(self._api_client)

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
            self.assertEqual(looked_up_locs.count, 2, 'Wrong number of locations')
            looked_up = looked_up_locs.locations[0]

            api_instance.delete_location(created.location_id)
            api_instance.delete_location(created1.location_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update(self):

        api_instance = swagger_client.LocationApi(self._api_client)

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
            self.assertEqual(updated, fetched, "update response != download response")
            fetched.location_id = None
            self.assertEqual(newloc, fetched, "update != download response")
            api_instance.delete_location(looked_up.location_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update_identifiers(self):

        api_instance = swagger_client.LocationApi(self._api_client)

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
            self.assertEqual(updated, fetched, "update response != download response")
            fetched.location_id = None
            self.assertEqual(newloc, fetched, "update != download response")
            api_instance.delete_location(looked_up.location_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update_duplicate(self):

        api_instance = swagger_client.LocationApi(self._api_client)

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
            with self.assertRaises(Exception) as context:
                new_created.identifiers = [
                    swagger_client.Identifier(identifier_type='partner_name',
                                              identifier_value='bhutan', study_name='1234-PV')
                ]
                updated = api_instance.update_location(new_created.location_id, new_created)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_location(looked_up.location_id)
            api_instance.delete_location(new_created.location_id)

        except ApiException as error:
            self.fail("test_update_duplicate: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update_missing(self):

        api_instance = swagger_client.LocationApi(self._api_client)

        try:

            loc = self.get_next_location()
            newloc = swagger_client.Location(None, 28.46362, 91.49542, 'location',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
            fake_id = uuid.uuid4()
            newloc.location_id = str(fake_id)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_location(newloc.location_id, newloc)

            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_update_missing: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_get_location_identifiers(self):

        metadata_api_instance = swagger_client.MetadataApi(self._api_client)
        api_instance = swagger_client.LocationApi(self._api_client)

        try:
            loc = self.get_next_location()
            loc = swagger_client.Location(None, 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BTN')
            loc.identifiers = [
                swagger_client.Identifier(identifier_type='partner_name', identifier_value='bhutan', study_name='1234-PV')
            ]
            created = api_instance.create_location(loc)
            
            idents = metadata_api_instance.get_location_identifier_types()

            self.assertIn('partner_name', idents)

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_update: Exception when calling SamplingEventApi->create_sampling_event: %s\n" % error)

