import six

from openapi_server.models.studies import Studies  # noqa: E501
from openapi_server.models.study import Study  # noqa: E501
from openapi_server import util

from backbone_server.controllers.study_controller import StudyController

from local.base_local_api import BaseLocalApi


class LocalStudyApi(BaseLocalApi):

    def __init__(self, api_client, user, auths, method):

        super().__init__(api_client, user, auths, method)

        self.study_controller = StudyController()

    def download_studies(self, start=None, count=None):  # noqa: E501
        """fetches studies

         # noqa: E501

        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """
        (ret, retcode) = self.study_controller.download_studies(
            start, count, self._user, self.auth_tokens())

        return self.create_response(ret, retcode, 'Studies')

    def download_study(self, study_name):  # noqa: E501
        """fetches a study

         # noqa: E501

        :param study_name: ID of study to fetch
        :type study_name: str

        :rtype: Study
        """
        (ret, retcode) = self.study_controller.download_study(
            study_name, self._user, self.auth_tokens())

        return self.create_response(ret, retcode, 'Study')

    def update_study(self, study_name, study):
        """updates a study

         # noqa: E501

        :param study_name: ID of study to update
        :type study_name: str
        :param study:
        :type study: dict | bytes

        :rtype: Study
        """
        (ret, retcode) = self.study_controller.update_study(study_name, study, self._user,
                                                            self.auth_tokens())
        return self.create_response(ret, retcode, 'Study')
