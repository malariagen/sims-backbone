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

  events: Observable<SamplingEvents>;

  taxaId: string;

  constructor(private route: ActivatedRoute, private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.taxaId = this.route.snapshot.params['taxaId'];

    this.events = this.sampleService.downloadSamplingEventsByTaxa(this.taxaId);
  }

}
