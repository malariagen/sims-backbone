import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationsMapComponent } from './locations-map.component';
import { Component, Directive, EventEmitter, Input, Output } from '@angular/core';
import { LatLng, LatLngBounds } from '@agm/core';
import { LeafletDirective } from '@asymmetrik/ngx-leaflet';

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
});
