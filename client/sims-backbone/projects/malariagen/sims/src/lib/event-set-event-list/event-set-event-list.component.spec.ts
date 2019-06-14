import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEventListComponent } from './event-set-event-list.component';
import { SamplingEvents, SamplingEventService } from '../typescript-angular-client';
import { EventEmitter, Output, Input, Component } from '@angular/core';
import { ActivatedRouteStub, createAuthServiceSpy, ActivatedRoute } from 'testing/index.spec';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'sims-event-list',
  template: ''
})
export class EventListComponentStub {
  @Input() eventSetName: string;
  @Input() filter: string;
}

describe('EventSetEventListComponent', () => {
  let component: EventSetEventListComponent;
  let fixture: ComponentFixture<EventSetEventListComponent>;

  let activatedRoute: ActivatedRouteStub;

  let httpClientSpy: { get: jasmine.Spec };

  let samplingEventService: SamplingEventService;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({ eventSetId: 'evsid' });

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    samplingEventService = new SamplingEventService(<any>httpClientSpy,
      '',
      createAuthServiceSpy().getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        EventSetEventListComponent,
        EventListComponentStub
      ],
      providers: [
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: SamplingEventService, useValue: samplingEventService },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
