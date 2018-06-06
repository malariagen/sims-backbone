import { TestBed, inject } from '@angular/core/testing';

import { SamplingEventsService } from './sampling-events.service';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';
import { Component, Input } from '@angular/core';
import { SamplingEventService } from './typescript-angular-client';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';

@Component({
  selector: 'app-event-list',
  template: ''
})
export class EventListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
}

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
        EventListComponentStub
      ]
    });
  });

  it('should be created', inject([SamplingEventsService], (service: SamplingEventsService) => {
    expect(service).toBeTruthy();
  }));
});
