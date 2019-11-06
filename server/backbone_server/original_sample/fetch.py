from openapi_server.models.attr import Attr
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.original_sample import OriginalSample

from backbone_server.sampling_event.fetch import SamplingEventFetch


class OriginalSampleFetch():

    @staticmethod
    def fetch_attrs(cursor, original_sample_id):

        stmt = '''SELECT attr_type, attr_value, attr_source FROM attrs
        JOIN original_sample_attrs ON original_sample_attrs.attr_id = attrs.id
        WHERE original_sample_id = %s
        ORDER BY attr_type, attr_value, attr_source'''

        cursor.execute(stmt, (original_sample_id,))

        attrs = []
        for (name, value, source) in cursor:
            ident = Attr(name, value, source)
            attrs.append(ident)

        if not attrs:
            attrs = None

        return attrs

    @staticmethod
    def fetch(cursor, original_sample_id, sampling_events=None):

        if not original_sample_id:
            return None

        stmt = '''SELECT original_samples.id, studies.study_name AS study_id,
        sampling_event_id, days_in_culture, partner_species, acc_date
        FROM original_samples
        LEFT JOIN partner_species_identifiers psi ON psi.id = original_samples.partner_species_id
        LEFT JOIN studies ON studies.id = original_samples.study_id
        WHERE original_samples.id = %s'''
        cursor.execute(stmt, (original_sample_id,))

        original_sample = None

        for (os_id, study_id,
             sampling_event_id, days_in_culture, partner_species, acc_date) in cursor:
            original_sample = OriginalSample(str(os_id),
                                             study_name=study_id,
                                             days_in_culture=days_in_culture,
                                             partner_species=partner_species,
                                             acc_date=acc_date)
            taxa = OriginalSampleFetch.fetch_taxonomies(cursor, study_id, partner_species)
            original_sample.partner_taxonomies = taxa
            if sampling_event_id:
                original_sample.sampling_event_id = str(sampling_event_id)

        if not original_sample:
            return original_sample

        original_sample.attrs = OriginalSampleFetch.fetch_attrs(
            cursor, original_sample_id)

        return original_sample

    @staticmethod
    def fetch_taxonomies(cursor, study_id, partner_species):

        if not study_id:
            return None

        if not partner_species:
            return None

        stmt = '''select DISTINCT taxonomy_id FROM taxonomy_identifiers ti
        JOIN partner_species_identifiers psi ON ti.partner_species_id=psi.id
        JOIN studies s ON psi.study_id=s.id
        WHERE partner_species = %s AND s.study_code = %s'''

        cursor.execute(stmt, (partner_species, study_id[:4]))

        partner_taxonomies = []
        for (taxa_id,) in cursor:
            taxa = Taxonomy(taxa_id)
            partner_taxonomies.append(taxa)

        if not partner_taxonomies:
            partner_taxonomies = None

        return partner_taxonomies

    @staticmethod
    def load_original_samples(cursor, all_attrs=True):

        original_samples = []
        sampling_event_list = []

        for (original_sample_id, study_id, sampling_event_id,\
             days_in_culture, partner_species) in cursor:
            original_sample = OriginalSample(str(original_sample_id),
                                             study_name=study_id,
                                             days_in_culture=days_in_culture,
                                             partner_species=partner_species)

            if sampling_event_id:
                original_sample.sampling_event_id = str(sampling_event_id)
                if str(sampling_event_id) not in sampling_event_list:
                    sampling_event_list.append(str(sampling_event_id))

            original_samples.append(original_sample)

        for original_sample in original_samples:
            os_id = original_sample.original_sample_id
            original_sample.attrs = OriginalSampleFetch.fetch_attrs(cursor,
                                                                    os_id)
            taxa = OriginalSampleFetch.fetch_taxonomies(cursor,
                                                        original_sample.study_name,
                                                        original_sample.partner_species)
            original_sample.partner_taxonomies = taxa

        sampling_events = {}

        for sampling_event_id in sampling_event_list:
            sampling_event = SamplingEventFetch.fetch(
                cursor, sampling_event_id)
            sampling_events[sampling_event_id] = sampling_event

        return original_samples, sampling_events
