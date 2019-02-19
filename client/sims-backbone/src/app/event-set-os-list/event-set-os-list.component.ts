import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-event-set-os-list',
  templateUrl: './event-set-os-list.component.html',
  styleUrls: ['./event-set-os-list.component.scss']
})
export class EventSetOsListComponent implements OnInit {

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

    this.downloadFileName = 'originalSamples_eventSet_' + this.eventSetId + '.csv';
    this.jsonDownloadFileName = 'originalSamples_eventSet_' + this.eventSetId + '.json';
  }

}

