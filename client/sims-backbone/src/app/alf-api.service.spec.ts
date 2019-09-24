import { TestBed } from '@angular/core/testing';

import { AlfApiService } from './alf-api.service';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('AlfApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [
      HttpClientModule,
      HttpClientTestingModule
    ]
  }));

  it('should be created', () => {
    const service: AlfApiService = TestBed.get(AlfApiService);
    expect(service).toBeTruthy();
  });
});
