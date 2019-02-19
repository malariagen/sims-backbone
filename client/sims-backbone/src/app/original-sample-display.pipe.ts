import { Pipe, PipeTransform } from '@angular/core';
import { OriginalSample, Taxonomy, SamplingEvent } from './typescript-angular-client';

@Pipe({
  name: 'originalSampleDisplay'
})
export class OriginalSampleDisplayPipe implements PipeTransform {

  transform(value: OriginalSample, key: string, studyId: string, samplingEvents: any): any {
    let ret = '';

    const samplingEvent: SamplingEvent = samplingEvents[value.samplingEventId];

    if (key === 'originalSampleId') {
      return value.originalSampleId
    } else if (key === 'samplingEventId') {
      return value.samplingEventId
    } else if (key === 'partner_species') {
      ret = value.partnerSpecies;
    } else if (key === 'studyId') {
      ret = value.studyName;
    } else if (key === 'taxa') {
      if (value.partnerTaxonomies) {
        const taxas = [];
        value.partnerTaxonomies.forEach((taxa: Taxonomy) => {
          taxas.push(taxa.taxonomyId);
        })
        ret = taxas.join(';');
      }
    } else if (key === 'doc') {
      if (samplingEvent) {
        ret = samplingEvent.doc;
      }
    } else {

      value.attrs.forEach(ident => {
        if (ident.attrType === key) {
          if (ret === '') {
            ret = ident.attrValue;
          } else {
            const ids: Array<String> = ret.split(';');
            // Avoid duplicates from different sources
            if (!ids.includes(ident.attrValue)) {
              ret = [ret, ident.attrValue].join(';');
            }
          }
        }

      });
    }

    return ret;
  }

}
