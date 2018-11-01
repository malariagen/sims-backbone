import { Pipe, PipeTransform } from '@angular/core';
import { DerivativeSample, OriginalSample } from './typescript-angular-client';

@Pipe({
  name: 'derivativeSampleDisplay'
})
export class DerivativeSampleDisplayPipe implements PipeTransform {

  transform(value: DerivativeSample, key: string, studyId: string, originalSamples: any): any {
    let ret = '';
    let originalSample : OriginalSample = originalSamples[value.original_sample_id];

    if (key == "derivative_sample_id") {
      return value.derivative_sample_id
    } else if (key == "original_sample_id") {
      return value.original_sample_id
    } else if (key == 'partner_species') {
      ret = originalSample.partner_species;
    } else if (key == 'dna_prep') {
      ret = value.dna_prep
    } else {

      value.attrs.forEach(ident => {
        if (ident.attr_type == key) {
          if (ret == '') {
            ret = ident.attr_value;
          } else {
            let ids: Array<String> = ret.split(';');
            //Avoid duplicates from different sources
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
