import { Component, Input } from '@angular/core';

import { Location } from '../typescript-angular-client/model/location';
import { Locations } from '../typescript-angular-client/model/locations';

@Component({
  selector: 'app-location-view',
  templateUrl: './location-view.component.html',
  styleUrls: ['./location-view.component.scss']
})
export class LocationViewComponent {

  zoom: number = 6;

  _location: Location;

  locations: Locations;

  constructor() { }

  @Input()
  set location(location) {
    if (location) {
      this._location = location;
      this.locations = <Locations>{};
      this.locations.count = 1;
      this.locations.locations = [location];
    }
  }

}
