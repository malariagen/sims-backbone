
import logging

from sqlalchemy.sql import text
from backbone_server.model.scope import session_scope
from backbone_server.report.base import BaseReport

class MultipleLocationGPS(BaseReport):

    def get(self, studies):

        with session_scope(self.session) as db:

            #, curated_name, accuracy, country, partner_name
            # ST_X(location) as latitude, ST_Y(location) as longitude
            stmt = text('''select code from location l
                join location_attr li ON li.location_id = l.id
                JOIN attr a ON a.id = li.attr_id
                JOIN study s ON a.study_id = s.id
                group by location, code
                having count(location) > 1 ORDER BY code;''')

            result = self.engine.execute(stmt)

            report_studies = []

            for (study_name,) in result:
                report_studies.append(study_name)

        return self.return_studies(report_studies, studies)
