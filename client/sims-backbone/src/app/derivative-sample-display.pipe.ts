import { Pipe, PipeTransform } from '@angular/core';
import { DerivativeSample, OriginalSample } from './typescript-angular-client';

@Pipe({
  name: 'derivativeSampleDisplay'
})
export class DerivativeSampleDisplayPipe implements PipeTransform {

  transform(value: DerivativeSample, key: string, studyId: string, originalSamples: any): any {
    let ret = '';
    let originalSample : OriginalSample = originalSamples[value.originalSampleId];

    if (key === 'derivativeSampleId') {
      return value.derivativeSampleId
    } else if (key === 'originalSampleId') {
      return value.originalSampleId
    } else if (key === 'partner_species') {
      ret = originalSample.partnerSpecies;
    } else if (key === 'dna_prep') {
      ret = value.dnaPrep
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
