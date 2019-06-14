import { TestBed, inject } from '@angular/core/testing';

import { DerivativeSamplesService } from './derivative-samples.service';
import { Component, Input } from '@angular/core';
import { DerivativeSampleService } from './typescript-angular-client';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'sims-ds-list',
  template: ''
})
export class DerivativeSampleListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
}
describe('DerivativeSamplesService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({     imports: [
      HttpClientModule,
      HttpClientTestingModule
    ],
    providers: [
      DerivativeSamplesService,
      DerivativeSampleService
    ],
    declarations: [
      DerivativeSampleListComponentStub
    ]
    });
  });

  it('should be created', inject([DerivativeSamplesService], (service: DerivativeSamplesService) => {
    expect(service).toBeTruthy();
  }));
});
