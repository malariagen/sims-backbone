import { Component, OnInit } from '@angular/core';

import { Locations } from '../typescript-angular2-client/model/Locations';
import { Location } from '../typescript-angular2-client/model/Location';
import { LocationApi } from '../typescript-angular2-client/api/LocationApi';

@Component({
  selector: 'app-all-locations-map',
  providers: [ LocationApi ],
  templateUrl: './all-locations-map.component.html',
  styleUrls: ['./all-locations-map.component.css']
})
export class AllLocationsMapComponent implements OnInit {

  locations: Locations;

  constructor(private locationApi: LocationApi) { }

  ngOnInit() {
    this.loadLocations();
  }

  loadLocations(): void {
    this.locationApi.downloadLocations().subscribe(
      (locations) => {
        this.locations = locations;
        console.log(this.locations);
      },
      (err) => console.error(err),
      () => { console.log("Downloaded locations") }
    )
  }

}
