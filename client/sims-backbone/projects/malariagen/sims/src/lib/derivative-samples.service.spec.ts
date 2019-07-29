import { TestBed, inject } from '@angular/core/testing';

import { DerivativeSamplesService } from './derivative-samples.service';
import { DerivativeSampleService } from './typescript-angular-client';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HttpClientModule } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { DsListComponent } from './ds-list/ds-list.component';

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
      MockComponent(DsListComponent)
    ]
    });
  });

  it('should be created', inject([DerivativeSamplesService], (service: DerivativeSamplesService) => {
    expect(service).toBeTruthy();
  }));
});
