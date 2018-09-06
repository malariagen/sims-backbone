
import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { EventListComponent } from './event-list.component';
import { Component, Input } from '@angular/core';
import {
  MatProgressBar, MatTable, MatColumnDef, MatHeaderCell, MatCellDef,
  MatHeaderCellDef, MatHeaderRowDef, MatHeaderRow, MatRow, MatRowDef,
  MatCell, MatDialogModule, MatSelect, MatTableModule, MatPaginator, MatOptionModule, MatFormFieldModule, MatTooltipModule, MatPaginatorModule
} from '@angular/material';
import { OverlayModule } from '@angular/cdk/overlay';
import { SamplingEvents, SamplingEventService, SamplingEvent } from '../typescript-angular-client';
import { SamplingEventDisplayPipe } from '../sampling-event-display.pipe';
import { SamplingEventsService } from '../sampling-events.service';
import { HttpBackend, HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';

import { createAuthServiceSpy, ActivatedRouteStub, asyncData, createOAuthServiceSpy, getTestSamplingEvents } from '../../testing/index.spec';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { HttpResponse } from 'selenium-webdriver/http';


@Component({ selector: 'app-downloader-csv', template: '' })
class DownloaderCsvStubComponent {
  @Input() filter;
  @Input() fileName;
  @Input() headers;
}

@Component({ selector: 'app-downloader-json', template: '' })
class DownloaderJsonStubComponent {
  @Input() filter;
  @Input() fileName;
}

describe('EventListComponent', () => {
  let component: EventListComponent;
  let fixture: ComponentFixture<EventListComponent>;

  let test_entries = getTestSamplingEvents();

  let httpClientSpy: { get: jasmine.Spy };

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    TestBed.configureTestingModule({
      imports: [
        MatDialogModule,
        OverlayModule,
        MatTableModule,
        MatOptionModule,
        MatPaginatorModule,
        MatFormFieldModule,
        MatTooltipModule,
        HttpClientModule,
        HttpClientTestingModule,
        NoopAnimationsModule
      ],
      declarations: [
        EventListComponent,
        DownloaderCsvStubComponent,
        DownloaderJsonStubComponent,
        MatProgressBar,
        SamplingEventDisplayPipe,

      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: SamplingEventService },
        { provide: SamplingEventsService },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(EventListComponent);
    component = fixture.componentInstance;

    component.filter = 'studyId:0001';

    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/samplingEvents?search_filter=' + component.filter + '&start=0&count=50',
        method: 'GET'
      });

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component).toBeTruthy();
    })
  )
  );

  it('should create rows', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/samplingEvents?search_filter=' + component.filter + '&start=0&count=50',
        method: 'GET'
      });

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.table._data.length).toBe(test_entries.sampling_events.length);

      expect(component.table._data).toBe(test_entries.sampling_events);

    })));

  it('should set headers', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/samplingEvents?search_filter=' + component.filter + '&start=0&count=50',
        method: 'GET'
      });

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      let expectedHeaders = ["sampling_event_id", "study_id", "partner_id", "roma_id", "doc", "partner_species", "taxa", "partner_location_name", "location_curated_name", "location"];

      expect(component.displayedColumns.length).toBe(expectedHeaders.length);

      for (let i = 0; i < expectedHeaders.length; i++) {
        expect(component.displayedColumns).toContain(expectedHeaders[i]);
      }


    })));

});
