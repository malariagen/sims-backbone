import { TestBed, inject } from '@angular/core/testing';

import { SimsAuthService } from './sims-auth.service';
import { OAuthService, UrlHelperService, OAuthLogger } from 'angular-oauth2-oidc';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SimsModuleConfig, SIMS_MODULE_CONFIG } from './sims.module.config';

describe('SimsAuthService', () => {
  beforeEach(() => TestBed.configureTestingModule({
    imports: [
      HttpClientModule,
      HttpClientTestingModule
    ],
    providers: [
      OAuthService,
      OAuthLogger,
      UrlHelperService,
      {
        provide: SIMS_MODULE_CONFIG,
        useClass: SimsModuleConfig
      }     
    ]
  }));

  it('should be created', inject([SimsAuthService], (service: SimsAuthService) => {
    expect(service).toBeTruthy();
  }));
});
