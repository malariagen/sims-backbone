import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import {
  asyncData, createAuthServiceSpy
} from '../../testing/index.spec';

import { AllLocationsMapComponent } from './all-locations-map.component';
import { of } from 'rxjs/observable/of';

import { OAuthService } from 'angular-oauth2-oidc';
import { LocationService } from '../typescript-angular-client';
import { HttpClient } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { LocationsMapComponent } from '../locations-map/locations-map.component';

describe('AllLocationsMapComponent', () => {
  let component: AllLocationsMapComponent;
  let fixture: ComponentFixture<AllLocationsMapComponent>;
  let httpClientSpy: { get: jasmine.Spy };
  let locationService: LocationService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);
    locationService = new LocationService(<any>httpClientSpy, '', authService.getConfiguration());


    TestBed.configureTestingModule({
      declarations: [
        AllLocationsMapComponent,
        MockComponent(LocationsMapComponent)
      ],
      providers: [
        { provide: OAuthService, useValue: authService },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: LocationService, useValue: locationService }
      ]
    })
      .compileComponents();

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllLocationsMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });


  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should have requested all locations', () => {
    expect(httpClientSpy.get.calls.mostRecent().args[0]).toBe('http://localhost/v1/locations', 'url');
    expect(httpClientSpy.get.calls.count()).toBe(1, 'one call');
  });
});
