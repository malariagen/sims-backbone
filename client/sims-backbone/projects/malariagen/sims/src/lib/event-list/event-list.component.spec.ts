
import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { EventListComponent } from './event-list.component';
import { MatOptionModule } from '@angular/material/core';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressBar } from '@angular/material/progress-bar';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { OverlayModule } from '@angular/cdk/overlay';
import { SamplingEventService  } from '../typescript-angular-client';
import { SamplingEventDisplayPipe } from '../sampling-event-display.pipe';
import { SamplingEventsService } from '../sampling-events.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';

import { createOAuthServiceSpy, getTestSamplingEvents } from '../../testing/index.spec';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MockComponent } from 'ng-mocks';
import { DownloaderCsvComponent } from '../downloader-csv/downloader-csv.component';
import { DownloaderJsonComponent } from '../downloader-json/downloader-json.component';



describe('EventListComponent', () => {
  let component: EventListComponent;
  let fixture: ComponentFixture<EventListComponent>;

  const test_entries = getTestSamplingEvents();

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
        MatProgressBar,
        SamplingEventDisplayPipe,
        MockComponent(DownloaderCsvComponent),
        MockComponent(DownloaderJsonComponent)

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

      const req = backend.expectOne({
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

      const req = backend.expectOne({
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

      const req = backend.expectOne({
        url: 'http://localhost/v1/samplingEvents?search_filter=' + component.filter + '&start=0&count=50',
        method: 'GET'
      });

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      const expectedHeaders = ['sampling_event_id', 'individual_id', 'partner_id', 'roma_id', 'doc', 'partner_location_name', 'location_curated_name', 'location'];

      expect(component.displayedColumns.length).toBe(expectedHeaders.length);

      for (let i = 0; i < expectedHeaders.length; i++) {
        expect(component.displayedColumns).toContain(expectedHeaders[i]);
      }


    })));

});
