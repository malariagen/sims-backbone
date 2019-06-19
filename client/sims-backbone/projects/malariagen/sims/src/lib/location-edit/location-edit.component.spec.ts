import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { LocationEditComponent } from './location-edit.component';
import { Component, Input } from '@angular/core';
import { Location, Locations, LocationService, Attr } from '../typescript-angular-client';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { createAuthServiceSpy, createOAuthServiceSpy, ActivatedRouteStub } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { MatFormField } from '@angular/material';
import { HttpTestingController } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { MapsAPILoader } from '@agm/core';
import {ObserversModule} from '@angular/cdk/observers';

import { HttpClient, HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { SimsModuleConfig } from '../sims.module.config';


@Component({ selector: 'sims-locations-map', template: '' })
class LocationsMapStubComponent {
  @Input() locations: Locations;
  @Input() polygon: any;
  @Input() zoom: number;
}

@Component({ selector: 'sims-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
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

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      locationId: 0
    });



    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
        ObserversModule
      ],
      declarations: [
        LocationEditComponent,
        LocationsMapStubComponent,
        AttrsTableStubComponent,
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
        SimsModuleConfig,
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {


    fixture = TestBed.createComponent(LocationEditComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should be created', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
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

  it('should populate edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '1234',
        curated_name: 'UK',
        curation_method: 'by hand',
        notes: 'notes',
        country: 'GBR',
        accuracy: 'region',
        latitude: 1,
        longitude: 2,
        attrs: [<Attr>{
          attr_source: 'test_src',
          attr_type: 'partner_name',
          attr_value: 'test_val',
          study_name: '9999'
        }, <Attr>{
          attr_source: 'test_src',
          attr_type: 'partner_name',
          attr_value: 'test_val',
          study_name: '9998'
        }]
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();
      expect(component.locationForm.controls['location_id'].value).toBe(testData.location_id);
      expect(component.locationForm.controls['curated_name'].value).toBe(testData.curated_name);
      expect(component.locationForm.controls['curation_method'].value).toBe(testData.curation_method);
      expect(component.locationForm.controls['notes'].value).toBe(testData.notes);
      expect(component.locationForm.controls['country'].value).toBe(testData.country);
      expect(component.locationForm.controls['accuracy'].value).toBe(testData.accuracy);
      expect(component.locationForm.controls['latitude'].value).toBe(testData.latitude);
      expect(component.locationForm.controls['longitude'].value).toBe(testData.longitude);
      const arrayControls = component.locationForm.controls['attrs'].value;
      expect(arrayControls[0].attr_source).toBe(testData.attrs[0].attr_source);
      expect(arrayControls[0].attr_type).toBe(testData.attrs[0].attr_type);
      expect(arrayControls[0].attr_value).toBe(testData.attrs[0].attr_value);
      expect(arrayControls[0].study_name).toBe(testData.attrs[0].study_name);
      expect(arrayControls[1].attr_source).toBe(testData.attrs[1].attr_source);
      expect(arrayControls[1].attr_type).toBe(testData.attrs[1].attr_type);
      expect(arrayControls[1].attr_value).toBe(testData.attrs[1].attr_value);
      expect(arrayControls[1].study_name).toBe(testData.attrs[1].study_name);
    })
  )
  );

  it('should save edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '1234',
        curated_name: 'UK',
        curation_method: 'by hand',
        notes: 'notes',
        country: 'GBR',
        accuracy: 'region',
        latitude: 1,
        longitude: 2,
        attrs: [<Attr>{
          attr_source: 'test_src',
          attr_type: 'partner_name',
          attr_value: 'test_val',
          study_name: '9999'
        }, <Attr>{
          attr_source: 'test_src',
          attr_type: 'partner_name',
          attr_value: 'test_val',
          study_name: '9998'
        }]
      };

      req.flush(testData);

      backend.verify();

      testData.curated_name = 'updated name';
      testData.curation_method = 'for test';
      testData.accuracy = 'city';
      testData.country = 'MLI';
      testData.notes = 'updated';
      component.locationForm.controls['curated_name'].setValue(testData.curated_name);
      component.locationForm.controls['curation_method'].setValue(testData.curation_method);
      component.locationForm.controls['notes'].setValue(testData.notes);
      component.locationForm.controls['country'].setValue(testData.country);
      component.locationForm.controls['accuracy'].setValue(testData.accuracy);

      expect(component.locationForm.valid).toBeTruthy();

      component.onSubmit({
        value: component.locationForm.value,
        valid: component.locationForm.valid
      });

      const put = backend.expectOne({
        url: 'http://localhost/v1/location/' + testData.location_id,
        method: 'PUT'
      });

      put.flush(testData);

      expect(put.request.body.location_id).toBe(testData.location_id);
      expect(put.request.body.curated_name).toBe(testData.curated_name);
      expect(put.request.body.curation_method).toBe(testData.curation_method);
      expect(put.request.body.notes).toBe(testData.notes);
      expect(put.request.body.country).toBe(testData.country);
      expect(put.request.body.accuracy).toBe(testData.accuracy);
      expect(put.request.body.latitude).toBe(testData.latitude);
      expect(put.request.body.longitude).toBe(testData.longitude);
      const arrayControls = put.request.body.attrs;
      expect(arrayControls[0].attr_source).toBe(testData.attrs[0].attr_source);
      expect(arrayControls[0].attr_type).toBe(testData.attrs[0].attr_type);
      expect(arrayControls[0].attr_value).toBe(testData.attrs[0].attr_value);
      expect(arrayControls[0].study_name).toBe(testData.attrs[0].study_name);
      expect(arrayControls[1].attr_source).toBe(testData.attrs[1].attr_source);
      expect(arrayControls[1].attr_type).toBe(testData.attrs[1].attr_type);
      expect(arrayControls[1].attr_value).toBe(testData.attrs[1].attr_value);
      expect(arrayControls[1].study_name).toBe(testData.attrs[1].study_name);

      backend.verify();
    })
  )
  );

  it('should set zoom for country accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'country'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('country');
      expect(component.zoom).toBe(4);

    })
  )
  );

  it('should set zoom for region accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'region'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('region');
      expect(component.zoom).toBe(7);

    })
  )
  );

  it('should set zoom for city accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'city'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('city');
      expect(component.zoom).toBe(11);

    })
  )
  );

  it('should set zoom for building accuracy', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const req = backend.expectOne({
        url: 'http://localhost/v1/location/0',
        method: 'GET'
      });

      const testData: Location = <Location>{
        location_id: '',
        latitude: 0,
        longitude: 0,
        accuracy: 'building'
      };

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      backend.verify();

      expect(component.locationForm.controls['accuracy'].value).toBe('building');
      expect(component.zoom).toBe(16);

    })
  )
  );

});
