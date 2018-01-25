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

  events: SamplingEvents;

  _pageSize: number;
  
  studyName: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.studyName = this.route.snapshot.params['studyName'];
  }

  pageNumber(pageNum: number) {
    let start = pageNum * this._pageSize;
    //console.log('Page number:' + start + "," + this._pageSize);
    this.sampleService.downloadSamplingEventsByStudy(this.studyName, start, this._pageSize).subscribe(samples => {
      this.events = samples;
    });
  }

  pageSize(pageSize: number) {
    this._pageSize = pageSize;
  }
}
