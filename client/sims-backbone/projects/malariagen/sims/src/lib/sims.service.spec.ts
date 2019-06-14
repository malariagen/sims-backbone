import { TestBed } from '@angular/core/testing';

import { SimsService } from './sims.service';

describe('SimsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SimsService = TestBed.get(SimsService);
    expect(service).toBeTruthy();
  });
});
