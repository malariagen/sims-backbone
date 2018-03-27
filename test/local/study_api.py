import six

from swagger_server.models.studies import Studies  # noqa: E501
from swagger_server.models.study import Study  # noqa: E501
from swagger_server import util

from backbone_server.controllers.study_controller import StudyController

from local.base_local_api import BaseLocalApi

class LocalStudyApi(BaseLocalApi):

    def __init__(self, api_client=None):

        super().__init__(api_client)

        self.study_controller = StudyController()

    def download_studies(self, start=None, count=None, user=None, token_info = None):  # noqa: E501
        """fetches studies

         # noqa: E501

        :param start: for pagination start the result set at a record x
        :type start: int
        :param count: for pagination the number of entries to return
        :type count: int

        :rtype: Studies
        """
        (ret, retcode) = self.study_controller.download_studies(start, count, user, token_info)

        return self.create_response(ret, retcode, 'Studies')


    def download_study(self, studyName, user=None, token_info = None):  # noqa: E501
        """fetches a study

         # noqa: E501

        :param studyName: ID of study to fetch
        :type studyName: str

        :rtype: Study
        """
        (ret, retcode) = self.study_controller.download_study(studyName, user, token_info)

        return self.create_response(ret, retcode, 'Study')


    def update_study(self, studyName, study, user=None, token_info = None):
        """updates a study

         # noqa: E501

        :param studyName: ID of study to update
        :type studyName: str
        :param study: 
        :type study: dict | bytes

        :rtype: Study
        """
        (ret, retcode) = self.study_controller.update_study(studyName, study, user,
                                             self.study_controller.token_info(token_info))
        return self.create_response(ret, retcode, 'Study')

