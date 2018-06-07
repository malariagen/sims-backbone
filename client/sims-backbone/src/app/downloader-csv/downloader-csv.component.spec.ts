import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { DownloaderCsvComponent } from './downloader-csv.component';
import { createOAuthServiceSpy, getTestSamplingEvents } from 'testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { SamplingEventsService } from '../sampling-events.service';
import { SamplingEventService, SamplingEvents } from '../typescript-angular-client';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import * as FileSaver from 'file-saver';

describe('DownloaderCsvComponent', () => {
  let component: DownloaderCsvComponent;
  let fixture: ComponentFixture<DownloaderCsvComponent>;
  let test_entries = getTestSamplingEvents();

  let httpClientSpy: { get: jasmine.Spy };

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [DownloaderCsvComponent],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: SamplingEventsService },
        { provide: SamplingEventService },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(DownloaderCsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      expect(component).toBeTruthy();
    })
  )
  );


  it('should return csv', inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      component.filter = 'studyId:0001';
      component.pageSize = 2;
      component.headers = [
        "study_id",
        "partner_id",
        "roma_id",
        "doc",
        "partner_species",
        "taxa",
        "partner_location_name",
        "location_curated_name",
        "location"
      ]

      spyOn(component, 'build').and.callThrough();

      spyOn(FileSaver, 'saveAs').and.callFake(function (blob: Blob, fileName) {

        //toHaveBeenCalledWith isn't clever enough to compare Blobs so doing
        //in fake function
        //Also fake function stops the actual saveAs being called and generating a download

        expect(fileName).toBe(component.fileName);
        let resultString = '"study_id"	"partner_id"	"roma_id"	"doc"	"partner_species"	"taxa"	"partner_location_name"	"location_curated_name"	"location"\r\n'
          + '"9999"	"9999_1"	"9999_1R"	"2003-06-01"	"An. dirus A"	"7168"	"Cambodia"	""	"12.565679, 104.990963"\r\n'
          + '"9999"	"9999_2"	"9999_2R"	"2003-06-01"	"An. dirus A"	"7168"	"Cambodia"	""	"12.565679, 104.990963"\r\n';

        //        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('text/csv;charset=utf-8');
        var reader = new FileReader();
        reader.addEventListener("loadend", function () {
          
          let cells = reader.result.split(/\t|\r\n/);
          let i = 0;

          component.headers.forEach(header => {
            expect(cells[i++]).toBe('"' + header + '"');
          });
          expect(reader.result).toEqual(resultString);
        });
        reader.readAsText(blob);

      });

      let button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/samplingEvents?filter=' + component.filter + '&start=0&count=' + component.pageSize,
        method: 'GET'
      };
      let req = backend.expectOne(result);

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

    })
  );

});
