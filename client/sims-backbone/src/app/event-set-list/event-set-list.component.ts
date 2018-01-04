import { Component, OnInit, InjectionToken } from '@angular/core';

import { HttpClient }               from '@angular/common/http';

import { OAuthService } from 'angular-oauth2-oidc';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSets } from '../typescript-angular-client/model/eventSets';

import { EventSetService } from '../typescript-angular-client/api/eventSet.service';

import { BASE_PATH } from '../typescript-angular-client/variables';

import { environment } from '../../environments/environment';


@Component({
  selector: 'app-event-set-list',
  providers: [
    {
      provide: BASE_PATH,
      useValue: environment.eventSetApiLocation
      
    },
    {
      provide: EventSetService,
      useFactory: (httpClient, basePath) => new EventSetService(httpClient, basePath, undefined),
      deps: [
        HttpClient,
        BASE_PATH
      ]
    }
  ],
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
