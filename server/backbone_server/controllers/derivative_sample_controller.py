
import logging
import urllib

from backbone_server.model.derivative_sample import BaseDerivativeSample

from backbone_server.controllers.base_controller import BaseController

from backbone_server.errors.duplicate_key_exception import DuplicateKeyException
from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.permission_exception import PermissionException

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class DerivativeSampleController(BaseController):

    def create_derivative_sample(self, derivative_sample, studies=None, user=None, auths=None):  # noqa: E501
        """create_derivative_sample

        Create a DerivativeSample # noqa: E501

        :param derivativeSample: The derivative sample to create
        :type derivativeSample: dict | bytes

        :rtype: DerivativeSample
        """
        retcode = 201
        samp = None

        try:
            post = BaseDerivativeSample(self.get_engine(), self.get_session())

            samp = post.post(derivative_sample, None, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug("create_derivativeSample: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("create_derivativeSample: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode

    def delete_derivative_sample(self, derivative_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """deletes an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to fetch
        :type derivativeSampleId: str

        :rtype: None
        """
        delete = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200

        try:
            delete.delete(derivative_sample_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "delete_derivativeSample: %s", repr(dme))
            retcode = 404
        except PermissionException as dke:
            logging.getLogger(__name__).debug("delete_derivative_sample: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return None, retcode

    def download_derivative_sample(self, derivative_sample_id, studies=None, user=None, auths=None):  # noqa: E501
        """fetches an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to fetch
        :type derivativeSampleId: str

        :rtype: DerivativeSample
        """

        get = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get(derivative_sample_id, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_derivativeSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_derivative_sample: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode

    def download_derivative_samples(self, search_filter, value_type=None,
                                    start=None, count=None,
                                    studies=None, user=None, auths=None):
        """
        fetches derivativeSamples for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: DerivativeSamples
        """

        retcode = 200
        samp = None

        # print(f'search_filter {search_filter} vt {value_type} start {start} count {count}')
        search_filter = urllib.parse.unquote_plus(search_filter)
        options = search_filter.split(':')
        if len(options) < 2:
            samp = 'Filter must be of the form type:arg(s)'
            retcode = 422
            return samp, retcode
        search_funcs = {
            "eventSet": self.download_derivative_samples_by_event_set,
            "studyId": self.download_derivative_samples_by_study,
            "taxa": self.download_derivative_samples_by_taxa,
        }
        func = search_funcs.get(options[0])
        if func:
            return func(options[1], start=start, count=count, studies=studies,
                        user=user, auths=auths)
        elif options[0] == 'attr':
            study_name = None
            if len(options) > 3 and options[3]:
                study_name = options[3]
            if len(options) < 3:
                return 'attr filter must have name and value', 422
            return self.download_derivative_samples_by_attr(options[1],
                                                            options[2],
                                                            study_name,
                                                            value_type=value_type,
                                                            start=start,
                                                            count=count,
                                                            studies=studies,
                                                            user=user,
                                                            auths=auths)
        else:
            samp = 'Invalid filter option'
            retcode = 422

        return samp, retcode

    def download_derivative_samples_by_event_set(self, event_set_id, start, count, studies=None, user=None, auths=None):
        """
        fetches derivativeSamples for a event_set

        :param event_set_id: event_set
        :type event_set_id: str

        :rtype: DerivativeSamples
        """

        retcode = 200
        samp = None

        try:
            get = BaseDerivativeSample(self.get_engine(), self.get_session())
            event_set_id = urllib.parse.unquote_plus(event_set_id)
            samp = get.get_by_event_set(event_set_id, studies, start, count)

        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_derivative_samples_by_event_set: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_derivative_samples_by_event_set: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode

    def download_derivative_samples_by_attr(self, prop_name, prop_value,
                                            study_name=None, value_type=None,
                                            start=None, count=None,
                                            studies=None, user=None, auths=None):  # noqa: E501
        """fetches one or more DerivativeSample by property value

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivativeSamples
        """

        get = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        samp = get.get_by_attr(prop_name, prop_value, study_name, value_type, start,
                               count, studies)

        return samp, retcode

    def download_derivative_samples_by_os_attr(self, prop_name, prop_value,
                                               study_name=None, value_type=None,
                                               start=None, count=None,
                                               studies=None, user=None, auths=None):  # noqa: E501
        """fetches one or more derivativeSamples by property value of associated derivative samples

         # noqa: E501

        :param propName: name of property to search
        :type propName: str
        :param propValue: matching value of property to search
        :type propValue: str
        :param studyName: if you want to restrict the search to a study e.g. for partner_id
        :type studyName: str

        :rtype: DerivativeSamples
        """

        get = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        samp = get.get_by_os_attr(prop_name, prop_value, study_name, value_type, start,
                                  count, studies)

        return samp, retcode

    def download_derivative_samples_by_study(self, study_name,
                                             start=None, count=None,
                                             studies=None, user=None, auths=None):
        """
        fetches derivativeSamples for a study

        :param studyName: location
        :type studyName: str

        :rtype: DerivativeSamples
        """

        get = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        # print(f'study_name {study_name} start {start} count {count}')
        try:
            samp = get.get_by_study(study_name, start=start, count=count, studies=studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_derivativeSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_derivative_samples_by_study: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode

    def download_derivative_samples_by_taxa(self, taxa_id,
                                            start=None, count=None,
                                            studies=None, user=None, auths=None):
        """
        fetches derivativeSamples for a taxa

        :param taxaId: taxa
        :type taxaId: str

        :rtype: DerivativeSamples
        """

        get = BaseDerivativeSample(self.get_engine(), self.get_session())

        retcode = 200
        samp = None

        try:
            samp = get.get_by_taxa(taxa_id, studies, start, count)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "download_derivative_samples_by_taxa: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("download_derivative_samples_by_taxa: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode

    def update_derivative_sample(self, derivative_sample_id, derivative_sample, studies=None, user=None, auths=None):  # noqa: E501
        """updates an DerivativeSample

         # noqa: E501

        :param derivativeSampleId: ID of DerivativeSample to update
        :type derivativeSampleId: str
        :param derivativeSample:
        :type derivativeSample: dict | bytes

        :rtype: DerivativeSample
        """

        retcode = 200
        samp = None

        try:
            put = BaseDerivativeSample(self.get_engine(), self.get_session())

            study_name = None
            samp = put.put(derivative_sample_id, derivative_sample, study_name, studies, user)
        except DuplicateKeyException as dke:
            logging.getLogger(__name__).debug(
                "update_derivativeSample: %s", repr(dke))
            retcode = 422
            samp = str(dke)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug(
                "update_derivativeSample: %s", repr(dme))
            retcode = 404
            samp = str(dme)
        except PermissionException as dke:
            logging.getLogger(__name__).debug("update_derivativeSample: %s", repr(dke))
            retcode = 403
            samp = str(dke)

        return samp, retcode
