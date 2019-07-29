import { TestBed, inject } from '@angular/core/testing';

import { OriginalSamplesService } from './original-samples.service';
import { OriginalSampleService } from './typescript-angular-client';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HttpClientModule } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { OsListComponent } from './os-list/os-list.component';

describe('OriginalSamplesService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule
      ],
      providers: [
        OriginalSamplesService,
        OriginalSampleService
      ],
      declarations: [
        MockComponent(OsListComponent)
      ]
    });
  });

  it('should be created', inject([OriginalSamplesService], (service: OriginalSamplesService) => {
    expect(service).toBeTruthy();
  }));
});
