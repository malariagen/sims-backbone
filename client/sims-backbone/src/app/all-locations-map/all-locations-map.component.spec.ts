import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllLocationsMapComponent } from './all-locations-map.component';

describe('AllLocationsMapComponent', () => {
  let component: AllLocationsMapComponent;
  let fixture: ComponentFixture<AllLocationsMapComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllLocationsMapComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllLocationsMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
