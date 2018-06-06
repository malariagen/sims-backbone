
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

import { createAuthServiceSpy, ActivatedRouteStub, asyncData, createOAuthServiceSpy } from '../../testing/index.spec';
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

  let test_entries = <SamplingEvents>{
    "count": 2,
    "locations": {
      "ba58650c-f365-41bd-a73d-d8517e9a01e5": {
        "country": "KHM",
        "attrs": [
          {
            "attr_source": "test",
            "attr_type": "partner_name",
            "attr_value": "Cambodia",
            "study_name": "9999"
          }
        ],
        "latitude": 12.565679,
        "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "longitude": 104.990963,
        "notes": "test"
      }
    },
    "sampling_events": [
      {
        "doc": "2003-06-01",
        "attrs": [
          {
            "attr_source": "vobs_dump",
            "attr_type": "partner_id",
            "attr_value": "9999_1"
          },
          {
            "attr_source": "vobs_dump",
            "attr_type": "roma_id",
            "attr_value": "9999_1R"
          }
        ],
        "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "partner_species": "An. dirus A",
        "partner_taxonomies": [
          {
            "taxonomy_id": 7168
          }
        ],
        "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "sampling_event_id": "0b0593ae-c613-42b6-8d3f-2bec2b3bd29c",
        "study_name": "9999"
      },
      {
        "doc": "2003-06-01",
        "attrs": [
          {
            "attr_source": "vobs_dump",
            "attr_type": "partner_id",
            "attr_value": "9999_2"
          },
          {
            "attr_source": "vobs_dump",
            "attr_type": "roma_id",
            "attr_value": "9999_2R"
          }
        ],
        "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "partner_species": "An. dirus A",
        "partner_taxonomies": [
          {
            "taxonomy_id": 7168
          }
        ],
        "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "sampling_event_id": "6890728f-c5e0-4c16-ac6d-b2505188a72b",
        "study_name": "9999"
      }
    ]
  }
  let httpClientSpy: { get: jasmine.Spy };

  let authService;

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
        url: 'http://localhost/v1/samplingEvents?filter=' + component.filter + '&start=0&count=50',
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
        url: 'http://localhost/v1/samplingEvents?filter=' + component.filter + '&start=0&count=50',
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
        url: 'http://localhost/v1/samplingEvents?filter=' + component.filter + '&start=0&count=50',
        method: 'GET'
      });

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      let expectedHeaders = ["study_id", "partner_id", "roma_id", "doc", "partner_species", "taxa", "partner_location_name", "location_curated_name", "location"];

      expect(component.displayedColumns.length).toBe(expectedHeaders.length);

      for (let i = 0; i < expectedHeaders.length; i++) {
        expect(component.displayedColumns).toContain(expectedHeaders[i]);
      }


    })));

});
