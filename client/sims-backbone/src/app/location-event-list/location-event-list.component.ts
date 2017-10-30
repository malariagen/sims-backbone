import { Component, OnInit } from '@angular/core';

import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { Sample } from '../typescript-angular2-client/model/Sample';
import { Samples } from '../typescript-angular2-client/model/Samples';
import { SampleApi } from '../typescript-angular2-client/api/SampleApi';
import { LocationApi } from '../typescript-angular2-client/api/LocationApi';


@Component({
  selector: 'app-location-event-list',
  providers: [SampleApi, LocationApi],
  templateUrl: './location-event-list.component.html',
  styleUrls: ['./location-event-list.component.css']
})

export class LocationEventListComponent implements OnInit {

  events: Observable<Samples>;

  studyName: string;

  constructor(private route: ActivatedRoute, private sampleApi: SampleApi, private locationApi: LocationApi) { }

  ngOnInit() {
    let latitude = this.route.snapshot.params['latitude'];
    let longitude = this.route.snapshot.params['longitude'];

    this.locationApi.downloadGPSLocation(latitude, longitude).subscribe(
      (location) => {
        console.log("Downloaded location via GPS");
        if (location) {

          this.events = this.sampleApi.downloadSamplesByLocation(location.location_id);
        }
    
      });
  }

}
