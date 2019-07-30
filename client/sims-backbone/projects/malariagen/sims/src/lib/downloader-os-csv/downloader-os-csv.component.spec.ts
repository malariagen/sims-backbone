import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { DownloaderOsCsvComponent } from './downloader-os-csv.component';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { getTestOriginalSamples } from '../../testing/index.spec';
import { OriginalSamplesService } from '../original-samples.service';
import { OriginalSampleService } from '../typescript-angular-client';

import * as FileSaver from 'file-saver';

describe('DownloaderOsCsvComponent', () => {
  let component: DownloaderOsCsvComponent;
  let fixture: ComponentFixture<DownloaderOsCsvComponent>;

  const test_entries = getTestOriginalSamples();

  const resultString = '"original_sample_id"	"study_id"	"partner_species"	"taxa"	"doc"	"partner_id"	"roma_id"	"sampling_event_id"\r\n'
  +'"bcb1e089-d1ee-43f0-bc5f-02073380b656"	"0001-PV-MD-UP"	"Plasmodium vivax"	"5855"	""	"0001"	"VVX0001"	"e0e73994-b9e5-48d0-af1e-84bc1e6d0cd5"\r\n'
  +'"4e7748c2-eed2-4920-8db6-c8df0ab675a3"	"0001-PV-MD-UP"	"Plasmodium vivax"	"5855"	"2015-06-09"	"00002"	"VVX00002"	"0aff80b8-fd1c-47ba-be3a-c3d123b4e28b"\r\n';

  let httpClientSpy: { get: jasmine.Spy };

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [ DownloaderOsCsvComponent ],
      providers: [
        { provide: OriginalSamplesService },
        { provide: OriginalSampleService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {


    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(DownloaderOsCsvComponent);
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
        'original_sample_id',
        'study_id',
        'partner_species',
        'taxa',
        'doc',
        'partner_id',
        'roma_id',
        'sampling_event_id'
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
        url: 'http://localhost/v1/originalSamples?search_filter=' + component.filter + '&start=0&count=' + component.pageSize,
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
        'original_sample_id',
        'study_id',
        'partner_species',
        'taxa',
        'doc',
        'partner_id',
        'roma_id',
        'sampling_event_id'
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
        url: 'http://localhost/v1/originalSamples?search_filter=' + component.filter + '&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req = backend.expectOne(result);

      const firstEntry = getTestOriginalSamples();
      firstEntry.original_samples.pop();
      req.flush(firstEntry);

      //expect(component.pageNumber).toBe(1);

      const result1 = {
        url: 'http://localhost/v1/originalSamples?search_filter=' + component.filter + '&start=' + component.pageNumber * component.pageSize + '&count=' + component.pageSize,
        method: 'GET'
      };
      const req1 = backend.expectOne(result1);

      const secondEntry = getTestOriginalSamples();
      secondEntry.original_samples = [secondEntry.original_samples[1]];
      req1.flush(secondEntry);

      // Finally, assert that there are no outstanding requests.
      backend.verify();


    })
  );
});
