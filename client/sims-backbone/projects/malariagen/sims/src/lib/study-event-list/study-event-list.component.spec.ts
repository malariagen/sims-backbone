import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyEventListComponent } from './study-event-list.component';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRouteStub, asyncData, createAuthServiceSpy, ActivatedRoute } from '../../testing/index.spec';
import { SamplingEventService, SamplingEvents } from '../typescript-angular-client';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'sims-event-list',
  template: ''
})
export class EventListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
}

describe('StudyEventListComponent', () => {
  let component: StudyEventListComponent;
  let fixture: ComponentFixture<StudyEventListComponent>;

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
        StudyEventListComponent,
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
    fixture = TestBed.createComponent(StudyEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
