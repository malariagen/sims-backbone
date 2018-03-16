import { TestBed, inject } from '@angular/core/testing';
import { Location, LocationStrategy, LocationChangeListener } from '@angular/common';

import { AuthService } from './auth.service';
import { HttpClient } from '@angular/common/http';
import { OAuthService, UrlHelperService } from 'angular-oauth2-oidc';
import { ActivatedRouteStub } from '../testing/index.spec';
import { ActivatedRoute } from '@angular/router';

export class LocationStrategyStub {
  path(includeHash?: boolean): string { return '/'};
  prepareExternalUrl(internal: string): string {return ''};
  pushState(state: any, title: string, url: string, queryParams: string): void {};
  replaceState(state: any, title: string, url: string, queryParams: string): void {};
  forward(): void {};
  back(): void {};
  onPopState(fn: LocationChangeListener): void {};
  getBaseHref(): string { return 'http://localhost' };
}
describe('AuthService', () => {

  let httpClientSpy: { get: jasmine.Spy };
  let activatedRoute: ActivatedRouteStub;
  let locStrategy: LocationStrategyStub;

  beforeEach(() => {

    activatedRoute = new ActivatedRouteStub();
    locStrategy = new LocationStrategyStub();

    TestBed.configureTestingModule({
      providers: [
        AuthService,
        OAuthService,
        UrlHelperService,
        Location,
        { provide: LocationStrategy, useValue: locStrategy },
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: HttpClient, useValue: httpClientSpy }
      ]
    });
    activatedRoute.setParamMap({ });

  });

  it('should be created', inject([AuthService], (service: AuthService) => {
    expect(service).toBeTruthy();
  }));
});
