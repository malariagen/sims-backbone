import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { SamplingEvent } from '../typescript-angular-client/model/samplingEvent';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';

@Component({
  selector: 'app-event-set-event-list',
  providers: [SamplingEventService],
  templateUrl: './event-set-event-list.component.html',
  styleUrls: ['./event-set-event-list.component.scss']
})
export class EventSetEventListComponent implements OnInit {

  events: Observable<SamplingEvents>;

  eventSetId: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.eventSetId = this.route.snapshot.params['eventSetId'];

    this.events = this.sampleService.downloadSamplingEventsByEventSet(this.eventSetId);
  }


}
