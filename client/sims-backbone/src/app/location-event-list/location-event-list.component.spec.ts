import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationEventListComponent } from './location-event-list.component';
import { HttpClient } from '@angular/common/http';
import { SamplingEventService, SamplingEvents } from '../typescript-angular-client';
import { ActivatedRoute } from '@angular/router';
import { createAuthServiceSpy, ActivatedRouteStub, asyncData } from '../../testing/index.spec';
import { Input, Component, Output, EventEmitter } from '@angular/core';


@Component({
  selector: 'app-event-list',
  template: ''
})
export class EventListComponentStub {
  @Input() events: SamplingEvents;
  @Input() eventSetName: string;
  @Input() studyName: string;
  @Output() pageNumber = new EventEmitter<number>(true);
  @Output() pageSize = new EventEmitter<number>(true);
}

describe('LocationEventListComponent', () => {
  let component: LocationEventListComponent;
  let fixture: ComponentFixture<LocationEventListComponent>;

  let activatedRoute: ActivatedRouteStub;

  let httpClientSpy: { get: jasmine.Spy };

  let samplingEventService: SamplingEventService;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({ 
      latitude: '0',
      longitude: '0'
     });

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));
    
    samplingEventService = new SamplingEventService(<any>httpClientSpy,
      '',
      createAuthServiceSpy().getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        LocationEventListComponent,
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
    fixture = TestBed.createComponent(LocationEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
