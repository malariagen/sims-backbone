import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Observable } from 'rxjs/Observable';

import { SamplingEventsService } from '../sampling-events.service';

@Component({
  selector: 'app-taxa-event-list',
  templateUrl: './taxa-event-list.component.html',
  styleUrls: ['./taxa-event-list.component.scss']
})
export class TaxaEventListComponent implements OnInit {

  taxaId: string;
  
  filter: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.taxaId = pmap.get('taxaId');
    });
    this.filter = 'taxa:' + this.taxaId;
  }
}
