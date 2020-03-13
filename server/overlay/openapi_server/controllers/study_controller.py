import connexion
import six

from openapi_server.models.studies import Studies  # noqa: E501
from openapi_server.models.study import Study  # noqa: E501
from openapi_server import util

from backbone_server.controllers.study_controller import StudyController

study_controller = StudyController()


def download_studies(studies=None, start=None, count=None, user=None, token_info=None):  # noqa: E501
    """fetches studies

     # noqa: E501

    :param start: for pagination start the result set at a record x
    :type start: int
    :param count: for pagination the number of entries to return
    :type count: int

    :rtype: Studies
    """
    return study_controller.download_studies(start=start,
                                             count=count, studies=studies,
                                             user=user,
                                             auths=study_controller.token_info(token_info))


def download_study(study_name, studies=None, user=None, token_info=None):  # noqa: E501
    """fetches a study

     # noqa: E501

    :param studyName: ID of study to fetch
    :type studyName: str

    :rtype: Study
    """
    return study_controller.download_study(study_name, studies=studies, user=user,
                                           auths=study_controller.token_info(token_info))


def update_study(study_name, body, studies=None, user=None, token_info=None):
    """updates a study

     # noqa: E501

    :param studyName: ID of study to update
    :type studyName: str
    :param study:
    :type study: dict | bytes

    :rtype: Study
    """
    if connexion.request.is_json:
        study = Study.from_dict(connexion.request.get_json())
    return study_controller.update_study(study_name, study, studies=studies, user=user,
                                         auths=study_controller.token_info(token_info))
