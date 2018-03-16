import { Component, OnInit } from '@angular/core';

import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { SamplingEvent } from '../typescript-angular-client/model/samplingEvent';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { LocationService } from '../typescript-angular-client/api/location.service';


@Component({
  selector: 'app-location-event-list',
  providers: [SamplingEventService, LocationService],
  templateUrl: './location-event-list.component.html',
  styleUrls: ['./location-event-list.component.css']
})

export class LocationEventListComponent implements OnInit {

  locationId: string;

  events: SamplingEvents;

  _pageSize: number;

  latitude: string;
  longitude: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService, private locationService: LocationService) { }

  ngOnInit() {
    
    this.route.paramMap.subscribe(pmap => {
      this.latitude = pmap.get('latitude');
      this.longitude = pmap.get('longitude');
    });

    this.locationService.downloadGPSLocation(this.latitude, this.longitude).subscribe(
      (location) => {
        //console.log("Downloaded location via GPS");

        if (location) {
          this.locationId = location.location_id;

        }

      });
  }

  pageNumber(pageNum: number) {
    let start = pageNum * this._pageSize;
   // console.log('Page number:' + start + "," + this._pageSize);
    if (this.locationId) {
      this.sampleService.downloadSamplingEventsByLocation(this.locationId, start, this._pageSize).subscribe(samples => {
        this.events = samples;
      });
    }
  }

  pageSize(pageSize: number) {
    this._pageSize = pageSize;
  }
}
