import sys

import logging

import ldap
import ldap.sasl

from openapi_server.models.group import Group  # noqa: E501
from openapi_server.models.groups import Groups  # noqa: E501


from openapi_server.models.people import People  # noqa: E501
from openapi_server.models.person import Person  # noqa: E501

from backbone_server.errors.missing_key_exception import MissingKeyException

class LDAPModel():

    def __init__(self, ldap_server, user_dn, user_pw):
        # server = self._plugin_settings["ldapServer"]
        # user_dn = self._plugin_settings['ldapUserDN']
        # user_pw = self._plugin_settings['ldapUserPassword']
        self._ldap_server = ldap_server
        self._user_dn = user_dn
        self._user_pw = user_pw

        self.logger = logging.getLogger(__name__)
        self.base = 'ou=people,dc=malariagen,dc=net'
        self.groups_base = 'ou=groups,dc=malariagen,dc=net'
        self.people_filter = '(objectClass=OpenLDAPperson)'
        self.public_group = b'cn=websitePeople,ou=malariagen,ou=groups,dc=malariagen,dc=net'
        self.dummy_user = 'cn=pwmTestUser,ou=users,ou=people,dc=malariagen,dc=net'
        self.ldap_fields = [
            'cn',
            'mail',
            'jobTitle1',
            'givenName',
            'sn',
            'jobTitle1',
            'o1',
            'jobTitle2',
            'o2',
            'jobTitle3',
            'o3',
            'oProfile1',
            'oProfile2',
            'oProfile3',
            'linkedInURL',
            'twitterURL',
            'researchGateURL',
            'scholarURL',
            'ORCID',
            'malariagenUID',
            'uid',
            'memberOf']


    def open_ldap(self):

        if self._ldap_server == None:
            return

        l = ldap.initialize(self._ldap_server)
        try:
            # l.start_tls_s()
            l.bind_s(self._user_dn, self._user_pw)
        except ldap.INVALID_CREDENTIALS:
            self.logger.error("Your username or password is incorrect.")
        except ldap.LDAPError as e:
            self.logger.error(str(e))
        return l
        auth_tokens = ldap.sasl.digest_md5(self._user_dn, self._user_pw)
        try:
          l.sasl_interactive_bind_s("", auth_tokens)
        except ldap.INVALID_CREDENTIALS as e:
          self.logger.error(str(e))
        return l

    def camel_to_snake(self, str):
        from functools import reduce

        return reduce(lambda x, y: x + ('_' if y.isupper() else '') + y, str).lower()

    def handle_ldap_entry(self, dn, entry, fields, auths):

        if not 'malariagenUID' in entry:
            self.logger.warn(("No malariagenUID in ", dn, " ", str(entry)))
            return

        person = Person()

        for field in fields:
            if field in entry:
                key = self.camel_to_snake(field)
                if field == 'memberOf':
                    if self.public_group not in entry[field]:
                        if auths['public_only']:
                            return None
                else:
                    if hasattr(person, key):
                        setattr(person, key, entry[field][0].decode("utf-8"))

        return person

    def list_ldap(self, base, search_filter, fields, auths):
        l = self.open_ldap()

        ret = People()

        if l == None:
            return ret
        r = l.search_s(base, ldap.SCOPE_SUBTREE,
                       search_filter, [str(x) for x in fields])
        ret.people = []
        ret.count = 0

        for dn, entry in r:
    #      print 'Processing',repr(dn)
            person = self.handle_ldap_entry(dn, entry, fields, auths)
            if person:
                ret.people.append(person)
                ret.count += 1
        l.unbind()

        return ret

    def list_ldap_member(self, ldap_conn, member, auths):
        try:
            r = ldap_conn.search_s(member, ldap.SCOPE_BASE,
                                   '(objectClass=*)',
                                   [str(x) for x in self.ldap_fields])
        except ldap.NO_SUCH_OBJECT:
            raise MissingKeyException(f'Failed search {member}')
        person = None
        for dn, entry in r:
    #      print 'Processing',repr(dn)
            person = self.handle_ldap_entry(dn, entry, self.ldap_fields, auths)

        return person

    def handle_ldap_group(self, ldap_conn, dn, entry, auths):

        members = []
        for member in entry['member']:
            if not member == self.dummy_user:
                try:
                    ldap_member = self.list_ldap_member(ldap_conn,
                                                        member.decode("utf-8"),
                                                        auths)
                    members.append(ldap_member)
                except MissingKeyException as mke:
                    # Log and ignore because LDAP is not configured for foreign
                    # key integrity
                    self.logger.error(f'Missing member {member} from {dn}')

        return members

    def list_group_members(self, study, base, group, auths):
        ldap_con = self.open_ldap()

        if not base:
            base = self.groups_base
        if study:
            base = 'ou=' + study + ',ou=studies,' + self.groups_base
        search_filter = '(objectClass=groupOfNames)'
        if group:
            search_filter = '(&(cn=' + group + ')(objectClass=groupOfNames))'
        try:
            results = ldap_con.search_s(base,
                                        ldap.SCOPE_SUBTREE,
                                        search_filter)
        except ldap.NO_SUCH_OBJECT:
            raise MissingKeyException(f'Failed search {base} {search_filter}')

        ret = Groups()
        ret.groups = []
        ret.count = 0

        for key, entry in results:
  #    print 'Processing',repr(dn)
            members = self.handle_ldap_group(ldap_con, key, entry, auths)
            group = Group()
            group.description = entry['description'][0].decode("utf-8")
            group.cn = entry['cn'][0].decode("utf-8")
            group.members = members
            ret.groups.append(group)
            ret.count += 1

        ldap_con.unbind()

        return ret
