import logging

from sqlalchemy.sql import text
from backbone_server.model.scope import session_scope
from backbone_server.report.base import BaseReport


class MissingTaxon(BaseReport):

    def get(self, studies):

        with session_scope(self.session) as db:
            stmt = text('''select distinct name from partner_species_identifier
            LEFT JOIN taxonomy_identifier ON taxonomy_identifier.partner_species_identifier_id = partner_species_identifier.id
            JOIN study ON study.id=study_id
            WHERE taxonomy_id IS NULL ORDER BY name''')

            result = self.engine.execute(stmt)

            report_studies = []

            for (study_name,) in result:
                report_studies.append(study_name)

        return self.return_studies(report_studies, studies)
