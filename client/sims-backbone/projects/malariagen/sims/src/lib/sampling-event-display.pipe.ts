import { Pipe, PipeTransform } from '@angular/core';
import { SamplingEvent, Location } from './typescript-angular-client';

@Pipe({
  name: 'samplingEventDisplay'
})
export class SamplingEventDisplayPipe implements PipeTransform {


  transform(value: SamplingEvent, key: string, studyId: string, locations: any): any {
    let ret = '';

    if (key === 'sampling_event_id') {
      return value.sampling_event_id
    } else if (key === 'doc') {
      ret = value.doc;
    } else if (key === 'location') {
      if (value.location_id) {
        const loc: Location = locations[value.location_id];
        if (loc && loc.latitude) {
          ret = '<a href="location/' + loc.location_id + '">' + loc.latitude + ', ' + loc.longitude + '</a>';
        }
      }
    } else if (key === 'location_curated_name') {
      if (value.location_id) {
        const loc: Location = locations[value.location_id];
        ret = loc.curated_name;
      }
    } else if (key === 'partner_location_name') {
      if (value.location_id) {
        const location: Location = locations[value.location_id];
        if (location.attrs) {
          location.attrs.forEach(ident => {
            const ident_value = String(ident.attr_value);
            if (studyId) {
              if ((studyId && (ident.study_name === studyId))) {
                ret = ident_value;
              }
            } else {
              ret = ret + ident_value + '(' + ident.study_name + ');';
            }
          });
        }
      }
    } else {

      value.attrs.forEach(ident => {
        if (ident.attr_type === key) {
          if (ret === '') {
            ret = String(ident.attr_value);
          } else {
            const ids: Array<String> = ret.split(';');
            // Avoid duplicates from different sources
            if (!ids.includes(String(ident.attr_value))) {
              ret = [ret, String(ident.attr_value)].join(';');
            }
          }
        }

      });
    }

    return ret;

  }

}
