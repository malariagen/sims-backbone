import { Pipe, PipeTransform } from '@angular/core';
import { OriginalSample, Taxonomy, SamplingEvent } from './typescript-angular-client';

@Pipe({
  name: 'originalSampleDisplay'
})
export class OriginalSampleDisplayPipe implements PipeTransform {

  transform(value: OriginalSample, key: string, studyId: string, samplingEvents: any): any {
    let ret = '';

    const samplingEvent: SamplingEvent = samplingEvents[value.sampling_event_id];

    if (key === 'original_sample_id') {
      return value.original_sample_id
    } else if (key === 'sampling_event_id') {
      return value.sampling_event_id
    } else if (key === 'partner_species') {
      ret = value.partner_species;
    } else if (key === 'study_id') {
      ret = value.study_name;
    } else if (key === 'taxa') {
      if (value.partner_taxonomies) {
        const taxas = [];
        value.partner_taxonomies.forEach((taxa: Taxonomy) => {
          taxas.push(taxa.taxonomy_id);
        })
        ret = taxas.join(';');
      }
    } else if (key === 'doc') {
      if (samplingEvent) {
        ret = samplingEvent.doc;
      }
    } else {

      value.attrs.forEach(ident => {
        if (ident.attr_type === key) {
          if (ret === '') {
            ret = ident.attr_value;
          } else {
            const ids: Array<String> = ret.split(';');
            // Avoid duplicates from different sources
            if (!ids.includes(ident.attr_value)) {
              ret = [ret, ident.attr_value].join(';');
            }
          }
        }

      });
    }

    return ret;
  }

}
