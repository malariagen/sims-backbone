import logging

from backbone_server.errors.missing_key_exception import MissingKeyException
from backbone_server.errors.integrity_exception import IntegrityException
from backbone_server.errors.permission_exception import PermissionException
from backbone_server.model.study import BaseStudy

from backbone_server.controllers.base_controller import BaseController

from backbone_server.controllers.decorators import apply_decorators


@apply_decorators
class StudyController(BaseController):

    def download_studies(self, studies=None, start=None, count=None, user=None, auths=None):
        """
        fetches studies

        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """

        get = BaseStudy(self.get_engine(), self.get_session())

        studies = get.gets(studies, start, count)

        return studies, 200

    def download_study(self, study_name, studies=None, user=None, auths=None):
        """
        fetches a study

        :param study_name: ID of study to fetch
        :type study_name: str

        :rtype: Study
        """

        get = BaseStudy(self.get_engine(), self.get_session())

        study = None
        retcode = 200
        try:
            study = get.get(study_name, studies)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_study: %s", repr(dme))
            retcode = 404
            study = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("download_study: %s, %s", repr(pme), user)
            retcode = 403
            study = str(pme)

        # print(f'returning {study}')

        return study, retcode

    def update_study(self, study_name, study, studies=None, user=None, auths=None):
        """
        updates a study

        :param study_name: ID of study to update
        :type study_name: str
        :param study:
        :type study: dict | bytes

        :rtype: Study
        """

        retcode = 200
        updated_study = None

        try:
            put = BaseStudy(self.get_engine(), self.get_session())

            updated_study = put.put(study_name, study, study_name, studies, user)
        except IntegrityException as dme:
            logging.getLogger(__name__).debug("update_study: %s", repr(dme))
            retcode = 422
            updated_study = str(dme)
        except MissingKeyException as dme:
            logging.getLogger(__name__).debug("update_study: %s", repr(dme))
            retcode = 404
            updated_study = str(dme)
        except PermissionException as pme:
            logging.getLogger(__name__).debug("update_study: %s, %s", repr(pme), user)
            retcode = 403
            updated_study = str(pme)

        return updated_study, retcode
