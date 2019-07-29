import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSearchComponent } from './event-search.component';
import { MatInputModule, MatSelectModule } from '@angular/material';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { asyncData } from '../../testing/index.spec';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MockComponent } from 'ng-mocks';
import { SampleOverviewComponent } from '../sample-overview/sample-overview.component';

describe('EventSearchComponent', () => {
  let component: EventSearchComponent;
  let fixture: ComponentFixture<EventSearchComponent>;

  let httpClientSpy: { get: jasmine.Spy };

  beforeEach(async(() => {

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData(['oxford_id']));

    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        MatInputModule,
        MatSelectModule,
        NoopAnimationsModule
      ],
      declarations: [
        EventSearchComponent,
        MockComponent(SampleOverviewComponent)
      ],
      providers: [
        { provide: HttpClient, useValue: httpClientSpy },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
