import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaEventListComponent } from './taxa-event-list.component';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { SamplingEvents, SamplingEventService } from '../typescript-angular-client';
import { ActivatedRouteStub, asyncData, createAuthServiceSpy, ActivatedRoute } from '../../testing/index.spec';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-event-list',
  template: ''
})
export class EventListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
}
describe('TaxaEventListComponent', () => {
  let component: TaxaEventListComponent;
  let fixture: ComponentFixture<TaxaEventListComponent>;

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
        TaxaEventListComponent,
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
    fixture = TestBed.createComponent(TaxaEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
