
import logging

from sqlalchemy.sql import text
from backbone_server.model.scope import session_scope

from backbone_server.report.base import BaseReport


class MissingLocations(BaseReport):

    def get(self, include_country, studies):

       with session_scope(self.session) as db:

            stmt = text('''select distinct code, accuracy FROM sampling_event se
            LEFT JOIN original_sample os ON os.sampling_event_id = se.id
            LEFT JOIN study ON study.id = os.study_id
            LEFT JOIN location ON location.id = location_id
            WHERE location_id IS NULL OR location.accuracy = 'country';''')

            result = self.engine.execute(stmt)

            report_studies = []

            for (study_name, accuracy) in result:
                if accuracy and accuracy == 'country':
                    if include_country:
                        report_studies.append(study_name)
                else:
                    report_studies.append(study_name)

       return self.return_studies(report_studies, studies)
