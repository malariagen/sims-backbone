import os

import openapi_client

from local.event_set_api import LocalEventSetApi
from local.location_api import LocalLocationApi
from local.individual_api import LocalIndividualApi
from local.metadata_api import LocalMetadataApi
from local.sampling_event_api import LocalSamplingEventApi
from local.study_api import LocalStudyApi
from local.original_sample_api import LocalOriginalSampleApi
from local.derivative_sample_api import LocalDerivativeSampleApi
from local.assay_data_api import LocalAssayDataApi
from local.report_api import LocalReportApi
from local.document_api import LocalDocumentApi
from local.manifest_api import LocalManifestApi
from local.identity_api import LocalIdentityApi

import logging

class ApiFactory():

    def __init__(self, user, auths, method, api_client):
        self._user = user
        self._auths = auths
        self._method = method
        self._api_client = api_client

        if self.isLocal():
            from backbone_server.controllers.base_controller import BaseController
            self.base_controller = BaseController()


    def isLocal(self):

        if os.getenv('LOCAL_TEST'):
            return True
        else:
            return False


    def is_filtered(self, study_id):
        if self.isLocal():
            if 'memberOf' not in self._auths or not self._auths['memberOf']:
                return False
            pi = f'cn=pi,ou={study_id},ou=studies,ou=groups,dc=malariagen,dc=net' in self._auths['memberOf']
            data = f'cn=data,ou={study_id},ou=studies,ou=groups,dc=malariagen,dc=net' in self._auths['memberOf']
            all_studies = 'cn=all_studies,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' in self._auths['memberOf']
            return pi or data or all_studies
        else:
            return self.is_authorized(study_id)

    def is_authorized(self, study_id):

        if self.isLocal():

            if self._auths and self._auths['memberOf']:
                return 'cn=editor,ou=sims,ou=projects,ou=groups,dc=malariagen,dc=net' in self._auths['memberOf']
            else:
                return False

        else:
            #Assumes if authenticated then authorized
            #Local test does this better
            logging.getLogger().error(dir(self._api_client))
            if self._api_client.configuration.access_token and not \
            self._api_client.configuration.access_token == 'abcd':
                return True
            else:
                return False


    def EventSetApi(self):

        ret = None

        if self.isLocal():
            ret = LocalEventSetApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.EventSetApi(self._api_client)

        return ret


    def LocationApi(self):

        ret = None

        if self.isLocal():
            ret = LocalLocationApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.LocationApi(self._api_client)

        return ret


    def MetadataApi(self):

        ret = None

        if self.isLocal():
            ret = LocalMetadataApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.MetadataApi(self._api_client)

        return ret


    def SamplingEventApi(self):

        ret = None

        if self.isLocal():
            ret = LocalSamplingEventApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.SamplingEventApi(self._api_client)

        return ret

    def OriginalSampleApi(self):

        ret = None

        if self.isLocal():
            ret = LocalOriginalSampleApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.OriginalSampleApi(self._api_client)

        return ret


    def DerivativeSampleApi(self):

        ret = None

        if self.isLocal():
            ret = LocalDerivativeSampleApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.DerivativeSampleApi(self._api_client)

        return ret

    def AssayDataApi(self):

        ret = None

        if self.isLocal():
            ret = LocalAssayDataApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.AssayDataApi(self._api_client)

        return ret

    def StudyApi(self):

        ret = None

        if self.isLocal():
            ret = LocalStudyApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.StudyApi(self._api_client)

        return ret

    def IndividualApi(self):

        ret = None

        if self.isLocal():
            ret = LocalIndividualApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.IndividualApi(self._api_client)

        return ret

    def ReportApi(self):

        ret = None

        if self.isLocal():
            ret = LocalReportApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.ReportApi(self._api_client)

        return ret

    def DocumentApi(self):

        ret = None

        if self.isLocal():
            ret = LocalDocumentApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.DocumentApi(self._api_client)

        return ret

    def ManifestApi(self):

        ret = None

        if self.isLocal():
            ret = LocalManifestApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.ManifestApi(self._api_client)

        return ret

    def IdentityApi(self):

        ret = None

        if self.isLocal():
            ret = LocalIdentityApi(self._api_client, self._user, self._auths, self._method)
        else:
            ret = openapi_client.IdentityApi(self._api_client)

        return ret
