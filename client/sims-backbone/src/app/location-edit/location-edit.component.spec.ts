import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationEditComponent } from './location-edit.component';
import { Component, Input } from '@angular/core';
import { Locations, LocationService } from '../typescript-angular-client';
import { FormsModule, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { createAuthServiceSpy, asyncData, createOAuthServiceSpy, ActivatedRouteStub } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatFormField } from '@angular/material';
import { HttpClient, HttpHandler } from '@angular/common/http';
import { OAuthService } from 'angular-oauth2-oidc';
import { MapsAPILoader } from '@agm/core';

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

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({ 
      latitude: 0,
      longitude: 0
     });

    let authService = createAuthServiceSpy();
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    locationService = new LocationService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule
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
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: LocationService, useValue: locationService },
        HttpHandler,
        { provide: ActivatedRoute, useValue: activatedRoute },
        MapsAPILoader
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocationEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
