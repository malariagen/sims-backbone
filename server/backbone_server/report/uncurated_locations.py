
import logging

from sqlalchemy.sql import text
from backbone_server.model.scope import session_scope
from backbone_server.report.base import BaseReport


class UncuratedLocations(BaseReport):

    def get(self, studies):

        with session_scope(self.session) as db:

            # , curated_name, accuracy, country, partner_name
            stmt = text('''select distinct study.name AS study_id FROM location l
            LEFT JOIN sampling_event se ON se.location_id = l.id
            LEFT JOIN original_sample os ON os.sampling_event_id = se.id
            LEFT JOIN study ON study.id = os.study_id
            where curated_name is NULL or accuracy IS NULL OR country IS NULL
                        ORDER BY study.name;''')

            result = self.engine.execute(stmt)

            report_studies = []

            for (study_name,) in result:
                report_studies.append(study_name)

        return self.return_studies(report_studies, studies)
