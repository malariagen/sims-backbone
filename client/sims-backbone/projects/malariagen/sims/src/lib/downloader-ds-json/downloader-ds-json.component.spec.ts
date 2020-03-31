import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { DownloaderDsJsonComponent } from './downloader-ds-json.component';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DerivativeSampleService, DerivativeSamples } from '../typescript-angular-client';
import { DerivativeSamplesService } from '../derivative-samples.service';


import * as FileSaver from 'file-saver';
import { getTestDerivativeSamples } from '../../testing/index.spec';

describe('DownloaderDsJsonComponent', () => {
  let component: DownloaderDsJsonComponent;
  let fixture: ComponentFixture<DownloaderDsJsonComponent>;

  const test_entries = getTestDerivativeSamples();

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [DownloaderDsJsonComponent],
      providers: [
        { provide: DerivativeSamplesService },
        { provide: DerivativeSampleService },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(DownloaderDsJsonComponent);
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

        let results = getTestDerivativeSamples();

        delete results.original_samples;
        delete results.attr_types;
        const resultString = JSON.stringify(results);
        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('application/json;charset=utf-8');
        const reader = new FileReader();
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {
            const content: string = reader.result;
            const resultEvents = <DerivativeSamples>JSON.parse(content);
            expect(resultEvents).toEqual(results);
          }
        });
        reader.readAsText(blob);

      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=0&count=' + component.pageSize,
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

        let results = getTestDerivativeSamples();

        delete results.original_samples;
        delete results.attr_types;

        const resultString = JSON.stringify(results);
        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('application/json;charset=utf-8');
        const reader = new FileReader();
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {
            const content: string = reader.result;
            let resultEvents = <DerivativeSamples>JSON.parse(content);
            expect(resultString).toEqual(content);
          }
        });
        reader.readAsText(blob);

      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);

      const firstEntry = getTestDerivativeSamples();
      firstEntry.derivative_samples.pop();
      req.flush(firstEntry);

      expect(component.pageNumber).toBe(1);

      const result1 = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + encodeURIComponent(component.filter) + '&value_type=str&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req1 = backend.expectOne(result1);

      const secondEntry = getTestDerivativeSamples();
      secondEntry.derivative_samples = [secondEntry.derivative_samples[1]];
      req1.flush(secondEntry);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

    })
  );
});
