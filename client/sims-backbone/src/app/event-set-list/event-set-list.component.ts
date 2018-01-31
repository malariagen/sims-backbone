import { Component, OnInit, InjectionToken } from '@angular/core';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSets } from '../typescript-angular-client/model/eventSets';

import { OAuthService } from 'angular-oauth2-oidc';

import { EventSetService } from '../typescript-angular-client/api/eventSet.service';

@Component({
  selector: 'app-event-set-list',
  providers: [EventSetService],
  templateUrl: './event-set-list.component.html',
  styleUrls: ['./event-set-list.component.scss']
})
export class EventSetListComponent implements OnInit {

  eventSets: EventSet[];

  constructor(private eventSetService: EventSetService, private oauthService: OAuthService) { }

  ngOnInit() {
    this.eventSetService.downloadEventSets().subscribe(
      (eventSets: EventSets) => {
        this.eventSets = eventSets.event_sets;
      }
    );
  }

}
