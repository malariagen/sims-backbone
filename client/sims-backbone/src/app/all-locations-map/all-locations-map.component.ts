import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Locations } from '../typescript-angular-client/model/locations';
import { Location } from '../typescript-angular-client/model/location';
import { LocationService } from '../typescript-angular-client/api/location.service';

@Component({
  selector: 'app-all-locations-map',
  providers: [LocationService],
  templateUrl: './all-locations-map.component.html',
  styleUrls: ['./all-locations-map.component.css']
})
export class AllLocationsMapComponent implements OnInit {

  locations: Locations;

  constructor(private locationService: LocationService, private oauthService: OAuthService) {
  }

  ngOnInit() {
    this.loadLocations();
  }

  loadLocations(): void {

    this.locationService.downloadLocations().subscribe(
      (locations) => {
        this.locations = locations;
        console.log(this.locations);
      },
      (err) => {
        console.log(err);
        if (err.status == 401) {
          this.oauthService.logOut();
          this.oauthService.initImplicitFlow();
        } else {
          console.error(err);
        }
      },
      () => { console.log("Downloaded locations") }
    )
  }

}
