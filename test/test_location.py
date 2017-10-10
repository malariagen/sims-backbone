import swagger_client
from swagger_client.rest import ApiException
from test_base import TestBase

import uuid

class TestLocation(TestBase):


    """
    """
    def test_create(self):

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
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

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
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

        api_instance = swagger_client.LocationApi()

        try:

            with self.assertRaises(Exception) as context:
                api_instance.delete_location(str(uuid.uuid4()))
            self.assertEqual(context.exception.status, 404)

        except ApiException as error:
            self.fail("test_delete_missing: Exception when calling LocationApi->delete_location: %s\n" % error)

    """
    """
    def test_duplicate_key(self):

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
            created = api_instance.create_location(loc)

            with self.assertRaises(Exception) as context:
                created = api_instance.create_location(loc)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_duplicate_key: Exception when calling LocationApi->create_location: %s\n" % error)


    """
    """
    def test_partner_lookup(self):

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_partner_location(loc.partner_name)
            fetched = api_instance.download_location(looked_up.location_id)
            self.assertEqual(created, fetched, "create response != download response")
            fetched.location_id = None
            self.assertEqual(loc, fetched, "upload != download response")
            api_instance.delete_location(created.location_id)

        except ApiException as error:
            self.fail("test_partner_lookup: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update(self):

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_partner_location(loc.partner_name)
            newloc = swagger_client.Location(None, 'new_partner_name', 28.46362, 91.49542, 'new_country',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
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

        api_instance = swagger_client.LocationApi()

        try:

            loc = swagger_client.Location(None, 'partner_name', 27.46362, 90.49542, 'country',
                                          'Trongsa, Trongsa, Bhutan', 'pv_3_locations.txt', 'BHU')
            created = api_instance.create_location(loc)
            looked_up = api_instance.download_partner_location(loc.partner_name)
            newloc = swagger_client.Location(None, 'new_partner_name', 28.46362, 91.49542, 'new_country',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
            new_created = api_instance.create_location(newloc)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_location(looked_up.location_id, newloc)

            self.assertEqual(context.exception.status, 422)

            api_instance.delete_location(looked_up.location_id)
            api_instance.delete_location(new_created.location_id)

        except ApiException as error:
            self.fail("test_update_duplicate: Exception when calling LocationApi->create_location: %s\n" % error)

    """
    """
    def test_update_missing(self):

        api_instance = swagger_client.LocationApi()

        try:

            newloc = swagger_client.Location(None, 'new_partner_name', 28.46362, 91.49542, 'new_country',
                                        'new_Trongsa, Trongsa, Bhutan', 'new_pv_3_locations.txt', 'IND')
            fake_id = uuid.uuid4()
            newloc.location_id = str(fake_id)
            with self.assertRaises(Exception) as context:
                updated = api_instance.update_location(newloc.location_id, newloc)

            self.assertEqual(context.exception.status, 404)


        except ApiException as error:
            self.fail("test_update_missing: Exception when calling LocationApi->create_location: %s\n" % error)

