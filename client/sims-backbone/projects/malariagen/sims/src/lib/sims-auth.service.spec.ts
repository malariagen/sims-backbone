import { TestBed, inject } from '@angular/core/testing';

import { SimsAuthService } from './sims-auth.service';
import { OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('SimsAuthService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [
      HttpClientModule,
      HttpClientTestingModule
    ],
    providers: [
      OAuthService,
      UrlHelperService,
      SimsAuthService,
    ]
  }));

  it('should be created', inject([SimsAuthService], (service: SimsAuthService) => {
    expect(service).toBeTruthy();
  }));
});
