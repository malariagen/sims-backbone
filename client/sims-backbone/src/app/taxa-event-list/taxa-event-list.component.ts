import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { SamplingEvent } from '../typescript-angular-client/model/samplingEvent';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';

@Component({
  selector: 'app-taxa-event-list',
  providers: [SamplingEventService],
  templateUrl: './taxa-event-list.component.html',
  styleUrls: ['./taxa-event-list.component.scss']
})
export class TaxaEventListComponent implements OnInit {

  events: SamplingEvents;

  _pageSize: number;

  taxaId: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.taxaId = this.route.snapshot.params['taxaId'];
  }

  pageNumber(pageNum: number) {
    let start = pageNum * this._pageSize;
    //console.log('Page number:' + start + "," + this._pageSize);
    this.sampleService.downloadSamplingEventsByTaxa(this.taxaId, start, this._pageSize).subscribe(samples => {
      this.events = samples;
    });
  }

  pageSize(pageSize: number) {
    this._pageSize = pageSize;
  }
}
