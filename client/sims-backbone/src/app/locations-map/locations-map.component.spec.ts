import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationsMapComponent } from './locations-map.component';
import { Component, Directive, EventEmitter, Input, Output } from '@angular/core';
import { LatLng, LatLngBounds } from '@agm/core';
import { LeafletDirective } from '@asymmetrik/ngx-leaflet';
import { Locations, Location } from '../typescript-angular-client';

@Directive({
  selector: '[leafletLayersControl]'
})
export class LeafletLayersControlDirectiveStub {
 
  @Input('leafletLayersControl') llc;
  
  @Input('leafletLayersControlOptions') layersControlOptions: any;
}


describe('LocationsMapComponent', () => {
  let component: LocationsMapComponent;
  let fixture: ComponentFixture<LocationsMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        LocationsMapComponent,
        LeafletDirective,
        LeafletLayersControlDirectiveStub
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocationsMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should show buttons', () => {

    component.locations = <Locations> {
      count: 2,
      locations: [
        <Location> {
          latitude: 0,
          longitude: 0
        },
        <Location> {
          latitude: 0,
          longitude: 0
        }
      ]
    };
    fixture.detectChanges();
    expect(component._locations.count).toBe(2);
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#noLayers').textContent).toBe('No layers');
    expect(compiled.querySelector('#allLayers').textContent).toBe('All layers');
    expect(component).toBeTruthy();
  });

  it('should hide buttons', () => {

    component.locations = <Locations> {
      count: 1,
      locations: [
        <Location> {
          latitude: 0,
          longitude: 0
        }
      ]
    };
    fixture.detectChanges();
    expect(component._locations.count).toBe(1);
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#noLayers')).toBeNull();
    expect(compiled.querySelector('#allLayers')).toBeNull();
    expect(component).toBeTruthy();
  });
});
