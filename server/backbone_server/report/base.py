
import logging

from openapi_server.models.studies import Studies
from backbone_server.model.study import BaseStudy


class BaseReport():

    def __init__(self, engine, session):
        self._logger = logging.getLogger(__name__)
        self.engine = engine
        self.session = session


    def return_studies(self, report_studies, studies):
        response = Studies([], 0)
        db_study = BaseStudy(self.engine, self.session)
        for study_id in report_studies:
            study = db_study.get(study_id, studies)
            response.studies.append(study)
            response.count = response.count + 1

        return response
