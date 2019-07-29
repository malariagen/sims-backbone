import { TestBed, inject } from '@angular/core/testing';

import { SamplingEventsService } from './sampling-events.service';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';
import { SamplingEventService } from './typescript-angular-client';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MockComponent } from 'ng-mocks';
import { EventListComponent } from './event-list/event-list.component';

describe('SamplingEventsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule
      ],
      providers: [SamplingEventsService, SamplingEventService],
      declarations: [
        StudyEventListComponent,
        MockComponent(EventListComponent)
      ]
    });
  });

  it('should be created', inject([SamplingEventsService], (service: SamplingEventsService) => {
    expect(service).toBeTruthy();
  }));
});
