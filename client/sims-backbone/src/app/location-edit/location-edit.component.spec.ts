import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { LocationEditComponent } from './location-edit.component';
import { Component, Input } from '@angular/core';
import { Location, Locations, LocationService } from '../typescript-angular-client';
import { FormsModule, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { createAuthServiceSpy, asyncData, createOAuthServiceSpy, ActivatedRouteStub } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatFormField } from '@angular/material';
import { HttpTestingController } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { MapsAPILoader } from '@agm/core';

import { HttpBackend, HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';


@Component({ selector: 'app-locations-map', template: '' })
class LocationsMapStubComponent {
  @Input() locations: Locations;
  @Input() polygon: any;
  @Input() zoom: number;
}

@Component({ selector: 'app-identifier-table', template: '' })
class IdentifiersTableStubComponent {
  @Input() identifiers;
}

@Component({ selector: 'agm-map', template: '' })
class AgmMapStubComponent {
  @Input() latitude: number;
  @Input() longitude: number;
  @Input() zoom: number;
}

@Component({ selector: 'agm-marker', template: '' })
class AgmMarkerStubComponent {
  @Input() latitude: number;
  @Input() longitude: number;
}

@Component({ selector: 'agm-polygon', template: '' })
class AgmPolygonStubComponent {
  @Input() paths;
}


describe('LocationEditComponent', () => {
  let component: LocationEditComponent;
  let fixture: ComponentFixture<LocationEditComponent>;

  let activatedRoute: ActivatedRouteStub;

  let httpClientSpy: { get: jasmine.Spy };

  let locationService: LocationService;

  let authService;

  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      latitude: 0,
      longitude: 0
    });

    authService = createAuthServiceSpy();


    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule
      ],
      declarations: [
        LocationEditComponent,
        LocationsMapStubComponent,
        IdentifiersTableStubComponent,
        AgmMapStubComponent,
        AgmMarkerStubComponent,
        AgmPolygonStubComponent,
        MatFormField
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: LocationService },
        { provide: ActivatedRoute, useValue: activatedRoute },
        MapsAPILoader,

      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(LocationEditComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      let req = backend.expectOne({
        url: 'http://localhost/v1/location/gps/0/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();
      expect(component).toBeTruthy();

    })
  )
  );

});
