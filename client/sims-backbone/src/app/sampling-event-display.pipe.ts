import { Pipe, PipeTransform } from '@angular/core';
import { SamplingEvent, Location } from './typescript-angular-client';

@Pipe({
  name: 'samplingEventDisplay'
})
export class SamplingEventDisplayPipe implements PipeTransform {


  transform(value: SamplingEvent, key: string, studyId: string, locations: any): any {
    let ret = '';

    if (key === 'samplingEventId') {
      return value.samplingEventId
    } else if (key === 'doc') {
      ret = value.doc;
    } else if (key === 'location') {
      if (value.locationId) {
        const loc = locations[value.locationId];
        if (loc && loc.latitude) {
          ret = '<a href="location/' + loc.locationId + '">' + loc.latitude + ', ' + loc.longitude + '</a>';
        }
      }
    } else if (key === 'location_curated_name') {
      if (value.locationId) {
        const loc: Location = locations[value.locationId];
        ret = loc.curatedName;
      }
    } else if (key === 'partner_location_name') {
      if (value.locationId) {
        const location: Location = locations[value.locationId];
        if (location.attrs) {
          location.attrs.forEach(ident => {
            const ident_value = ident.attrValue;
            if (studyId) {
              if ((studyId && (ident.studyName === studyId))) {
                ret = ident_value;
              }
            } else {
              ret = ret + ident_value + '(' + ident.studyName + ');';
            }
          });
        }
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
