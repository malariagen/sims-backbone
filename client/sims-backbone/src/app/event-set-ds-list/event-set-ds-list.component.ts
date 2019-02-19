import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-event-set-ds-list',
  templateUrl: './event-set-ds-list.component.html',
  styleUrls: ['./event-set-ds-list.component.scss']
})
export class EventSetDsListComponent implements OnInit {

  eventSetId: string;
  
  filter: string;

  downloadFileName: string;

  jsonDownloadFileName: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.eventSetId = pmap.get('eventSetId');
    });
    this.filter = 'eventSet:' + this.eventSetId;
    this.downloadFileName = 'derivativeSamples_eventSet_' + this.eventSetId + '.csv';
    this.jsonDownloadFileName = 'derivativeSamples_eventSet_' + this.eventSetId + '.json';
  }
}
