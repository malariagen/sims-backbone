import { TestBed, inject } from '@angular/core/testing';

import { SimsAuthService } from './sims-auth.service';
import { OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SIMS_AUTH_HTTP_CONFIG } from './auth/response.interceptor';
import { SimsModuleConfig } from './sims.module.config';

describe('SimsAuthService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [
      HttpClientModule,
      HttpClientTestingModule
    ],
    providers: [
      OAuthService,
      UrlHelperService,
      {
        provide: SIMS_AUTH_HTTP_CONFIG,
        useClass: SimsModuleConfig
      }     
    ]
  }));

  it('should be created', inject([SimsAuthService], (service: SimsAuthService) => {
    expect(service).toBeTruthy();
  }));
});
