import { TestBed, inject } from '@angular/core/testing';

import { OriginalSamplesService } from './original-samples.service';

describe('OriginalSamplesService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [OriginalSamplesService]
    });
  });

  it('should be created', inject([OriginalSamplesService], (service: OriginalSamplesService) => {
    expect(service).toBeTruthy();
  }));
});
