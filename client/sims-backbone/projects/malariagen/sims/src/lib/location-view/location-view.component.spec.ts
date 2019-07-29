import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationViewComponent } from './location-view.component';
import { RouterTestingModule } from '@angular/router/testing';

import { Component, Input } from '@angular/core';
import { Location, Locations } from '../typescript-angular-client';
import { MockComponent } from 'ng-mocks';
import { AttrTableComponent } from '../attr-table/attr-table.component';
import { LocationsMapComponent } from '../locations-map/locations-map.component';

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
        MockComponent(LocationsMapComponent),
        MockComponent(AttrTableComponent)
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
