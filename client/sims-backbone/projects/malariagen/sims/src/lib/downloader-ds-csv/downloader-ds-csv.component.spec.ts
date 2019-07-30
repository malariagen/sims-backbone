import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { DownloaderDsCsvComponent } from './downloader-ds-csv.component';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSampleService } from '../typescript-angular-client';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { getTestDerivativeSamples } from '../../testing/index.spec';

import * as FileSaver from 'file-saver';

describe('DownloaderDsCsvComponent', () => {
  let component: DownloaderDsCsvComponent;
  let fixture: ComponentFixture<DownloaderDsCsvComponent>;

  const test_entries = getTestDerivativeSamples();

  const resultString = '"derivative_sample_id"	"dna_prep"	"plate_name"	"plate_position"	"original_sample_id"\r\n'
  + '"0f1aaffe-7de2-4adc-b593-c53c37a1ab1c"	""	"PLATE_RCN_00022"	"H10"	"529b4442-c1b8-454b-bb86-76242b1cb7bd"\r\n'
  + '"1334aae7-fdee-4244-a960-396c714886c4"	""	"PLATE_RCN_00023"	"G04"	"58932826-5adf-4cfc-9f3b-238de4a52f6d"\r\n';

  let httpClientSpy: { get: jasmine.Spy };

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [DownloaderDsCsvComponent],
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

    fixture = TestBed.createComponent(DownloaderDsCsvComponent);
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
        'derivative_sample_id',
        'dna_prep',
        'plate_name',
        'plate_position',
        'original_sample_id'
      ]

      spyOn(component, 'build').and.callThrough();

      spyOn(FileSaver, 'saveAs').and.callFake(function (blob: Blob, fileName) {

        // toHaveBeenCalledWith isn't clever enough to compare Blobs so doing
        // in fake function
        // Also fake function stops the actual saveAs being called and generating a download

        expect(fileName).toBe(component.fileName);
        
        expect(blob.type).toBe('text/csv;charset=utf-8');
        const reader = new FileReader();
        reader.readAsText(blob);
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {
            const content: string = reader.result;
            const cells = content.split(/\t|\r\n/);
            let i = 0;

            component.headers.forEach(header => {
              expect(cells[i++]).toBe('"' + header + '"');
            });
          }
          expect(reader.result).toEqual(resultString);
        });

        
      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + component.filter + '&start=0&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);
      req.flush(test_entries);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

    })
  );

  it('should return csv paged', inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      component.filter = 'studyId:0001';
      component.pageSize = 1;
      component.headers = [
        'derivative_sample_id',
        'dna_prep',
        'plate_name',
        'plate_position',
        'original_sample_id'
      ]

      spyOn(component, 'build').and.callThrough();

      spyOn(FileSaver, 'saveAs').and.callFake(function (blob: Blob, fileName) {

        // toHaveBeenCalledWith isn't clever enough to compare Blobs so doing
        // in fake function
        // Also fake function stops the actual saveAs being called and generating a download

        expect(fileName).toBe(component.fileName);

        //        expect(blob.size).toBe(resultString.length);
        expect(blob.type).toBe('text/csv;charset=utf-8');
        const reader = new FileReader();
        reader.addEventListener('loadend', function () {
          if (typeof reader.result === 'string') {

            const content: string = reader.result;
            const cells = content.split(/\t|\r\n/);
            let i = 0;

            component.headers.forEach(header => {
              expect(cells[i++]).toBe('"' + header + '"');
            });
            expect(reader.result).toEqual(resultString);
          }
        });
        reader.readAsText(blob);

      });

      const button = fixture.debugElement.nativeElement.querySelector('button');
      button.click();
      expect(component.build).toHaveBeenCalled();

      fixture.detectChanges();

      const result = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + component.filter + '&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);

      const firstEntry = getTestDerivativeSamples();
      firstEntry.derivative_samples.pop();
      req.flush(firstEntry);

      //expect(component.pageNumber).toBe(1);

      const result1 = {
        url: 'http://localhost/v1/derivativeSamples?search_filter=' + component.filter + '&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
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
