import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationViewComponent } from './location-view.component';
import { RouterTestingModule } from '@angular/router/testing';

import { Component, Input } from '@angular/core';
import { Location, Locations, LocationService } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy, ActivatedRouteStub, createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { HttpClient } from '@angular/common/http';

@Component({ selector: 'app-locations-map', template: '' })
class LocationsMapStubComponent {
  @Input() locations: Locations;
  @Input() polygon: any;
  @Input() zoom: number;
}

@Component({ selector: 'app-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
}

describe('LocationViewComponent', () => {
  let component: LocationViewComponent;
  let fixture: ComponentFixture<LocationViewComponent>;
  
  beforeEach(async(() => {

    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [ 
        LocationViewComponent,
        LocationsMapStubComponent,
        AttrsTableStubComponent
      ],
      providers: [
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocationViewComponent);
    component = fixture.componentInstance;

    component._location = <Location>{
      accuracy: 'city',
      latitude: 0,
      longitude: 0,
      notes: ''
    };
    component.locations = <Locations> {
      count: 1,
      locations: [ component._location ]
    }
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
