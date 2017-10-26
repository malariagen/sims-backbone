import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { Sample } from '../typescript-angular2-client/model/Sample';
import { Samples } from '../typescript-angular2-client/model/Samples';
import { SampleApi } from '../typescript-angular2-client/api/SampleApi';

@Component({
  selector: 'app-study-event-list',
  providers: [SampleApi],
  templateUrl: './study-event-list.component.html',
  styleUrls: ['./study-event-list.component.css']
})
export class StudyEventListComponent implements OnInit {

  events: Observable<Samples>;

  studyName: string;

  constructor(private route: ActivatedRoute, private sampleApi: SampleApi) { }

  ngOnInit() {
    this.studyName = this.route.snapshot.params['studyName'];
    
    this.events = this.sampleApi.downloadSamplesByStudy(this.studyName);
  }

}
