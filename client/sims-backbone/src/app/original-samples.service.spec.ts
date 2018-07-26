import { TestBed, inject } from '@angular/core/testing';

import { OriginalSamplesService } from './original-samples.service';
import { OriginalSampleService } from './typescript-angular-client';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HttpClientModule } from '@angular/common/http';
import { Input, Component } from '@angular/core';

@Component({
  selector: 'app-os-list',
  template: ''
})
export class OriginalSampleListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
}

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
        OriginalSampleListComponentStub
      ]
    });
  });

  it('should be created', inject([OriginalSamplesService], (service: OriginalSamplesService) => {
    expect(service).toBeTruthy();
  }));
});
