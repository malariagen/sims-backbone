import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEventListComponent } from './event-set-event-list.component';
import { SamplingEventService } from '../typescript-angular-client';
import { ActivatedRouteStub, createAuthServiceSpy, ActivatedRoute } from '../../testing/index.spec';
import { HttpClient } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { EventListComponent } from '../event-list/event-list.component';


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
        MockComponent(EventListComponent)
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
