import os
import urllib

from openapi_server.models.groups import Groups  # noqa: E501
from openapi_server.models.people import People  # noqa: E501

from backbone_server.ldap.ldap_model import LDAPModel

class IdentityController():

    def __init__(self):

        self._ldap_server = os.getenv('BB_LDAP_SERVER')
        self._ldap_user = os.getenv('BB_LDAP_USER')
        self._ldap_passwd = os.getenv('BB_LDAP_PASSWORD')

    def token_info(self, token_info):

        # In theory it may be possible to extract the LDAP credentials here
        # Otherwise can use group membership
        # print(token_info)
        public_only = True
        if 'cn=peopleRead,ou=manage,ou=groups,dc=malariagen,dc=net' in token_info['memberOf']:
            public_only = False
        res = {
            'ldap_user': self._ldap_user,
            'ldap_password': self._ldap_passwd,
            'public_only': public_only
        }
        return res

    def download_groups(self, search_filter, start=None, count=None, user=None,
                        auths=None):  # noqa: E501
        """fetches groups

         # noqa: E501

        :param search_filter: search filter e.g. studyId:0000, attr:name:value,
        :type search_filter: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Groups
        """

        ldap_model = LDAPModel(self._ldap_server, auths['ldap_user'],
                               auths['ldap_password'])


        study = None
        base = None
        group = None
        if search_filter:
            search_filter = urllib.parse.unquote_plus(search_filter)
            for option in search_filter.split(';'):
                options = option.split(':')
                if options[0] == 'study':
                    study = options[1]
                elif options[0] == 'base':
                    base = options[1]
                elif options[0] == 'group':
                    group = options[1]
        ret = ldap_model.list_group_members(study, base, group, auths)

        return ret, 200


    def download_people(self, search_filter, start=None, count=None, user=None,
                        auths=None):  # noqa: E501
        """fetches people

         # noqa: E501

        :param search_filter: search filter e.g. studyId:0000, attr:name:value, location:locationId, taxa:taxId, eventSet:setName
        :type search_filter: str
        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: People
        """
        ldap_model = LDAPModel(self._ldap_server, auths['ldap_user'],
                               auths['ldap_password'])

        ldap_filter = ldap_model.people_filter

        if search_filter:
            search_filter = urllib.parse.unquote_plus(search_filter)
            options = search_filter.split(':')
            ldap_filter = f'(&{ldap_filter}({options[0]}={options[1]}))'
        ret = ldap_model.list_ldap(ldap_model.base, ldap_filter,
                                   ldap_model.ldap_fields, auths)

        return ret, 200
