import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { SamplingEvent } from '../typescript-angular-client/model/samplingEvent';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';

@Component({
  selector: 'app-study-event-list',
  providers: [SamplingEventService],
  templateUrl: './study-event-list.component.html',
  styleUrls: ['./study-event-list.component.css']
})
export class StudyEventListComponent implements OnInit {

  events: Observable<SamplingEvents>;

  studyName: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.studyName = this.route.snapshot.params['studyName'];

    this.events = this.sampleService.downloadSamplingEventsByStudy(this.studyName);
  }

}
