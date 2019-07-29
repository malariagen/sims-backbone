import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationsMapComponent } from './locations-map.component';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { Locations, Location } from '../typescript-angular-client';


describe('LocationsMapComponent', () => {
  let component: LocationsMapComponent;
  let fixture: ComponentFixture<LocationsMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        LeafletModule
      ],
      declarations: [
        LocationsMapComponent
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
