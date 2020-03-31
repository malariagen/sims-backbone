import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { DownloaderJsonComponent } from './downloader-json.component';
import { createOAuthServiceSpy, getTestSamplingEvents } from '../../testing/index.spec';
import { SamplingEventsService } from '../sampling-events.service';
import { SamplingEventService, SamplingEvent, SamplingEvents } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import * as FileSaver from 'file-saver';

describe('DownloaderJsonComponent', () => {
  let component: DownloaderJsonComponent;
  let fixture: ComponentFixture<DownloaderJsonComponent>;

  const test_entries = getTestSamplingEvents();

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [DownloaderJsonComponent],
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

    fixture = TestBed.createComponent(DownloaderJsonComponent);
    component = fixture.componentInstance;


    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      expect(component).toBeTruthy();
    })
  )
  );

  it('should return json', inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      component.filter = 'studyId:0001';
      component.pageSize = 2;

      spyOn(component, 'build').and.callThrough();

      spyOn(FileSaver, 'saveAs').and.callFake(function (blob: Blob, fileName) {

        // toHaveBeenCalledWith isn't clever enough to compare Blobs so doing
        // in fake function
        // Also fake function stops the actual saveAs being called and generating a download

        expect(fileName).toBe(component.fileName);
        const resultString = JSON.stringify(test_entries);
        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('application/json;charset=utf-8');
        const reader = new FileReader();
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {
            const content: string = reader.result;
            const resultEvents = <SamplingEvents>JSON.parse(content);
            expect(resultEvents).toEqual(test_entries);
          }
        });
        reader.readAsText(blob);

      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/samplingEvents?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=0&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);

      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

    })
  );

  it('should return json paged', inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      component.filter = 'studyId:0001';
      component.pageSize = 1;

      spyOn(component, 'build').and.callThrough();

      spyOn(FileSaver, 'saveAs').and.callFake(function (blob: Blob, fileName) {

        // toHaveBeenCalledWith isn't clever enough to compare Blobs so doing
        // in fake function
        // Also fake function stops the actual saveAs being called and generating a download

        expect(fileName).toBe(component.fileName);
        const resultString = JSON.stringify(test_entries);
        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('application/json;charset=utf-8');
        const reader = new FileReader();
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {
            const content: string = reader.result;
            const resultEvents = <SamplingEvents>JSON.parse(content);
            expect(resultEvents).toEqual(test_entries);
          }
        });
        reader.readAsText(blob);

      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/samplingEvents?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);

      const firstEntry = getTestSamplingEvents();
      firstEntry.sampling_events.pop();
      req.flush(firstEntry);

      expect(component.pageNumber).toBe(1);

      const result1 = {
        url: 'http://localhost/v1/samplingEvents?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req1 = backend.expectOne(result1);

      const secondEntry = getTestSamplingEvents();
      secondEntry.sampling_events = [secondEntry.sampling_events[1]];
      req1.flush(secondEntry);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

    })
  );
});
