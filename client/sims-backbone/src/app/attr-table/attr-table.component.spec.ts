import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttrTableComponent } from './attr-table.component';
import { MatTableModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { Component, Input } from '@angular/core';
import { Locations } from '../typescript-angular-client';

@Component({ selector: 'app-locations-map', template: '' })
class LocationsMapStubComponent {
  @Input() locations: Locations;
  @Input() polygon: any;
  @Input() zoom: number;
}

describe('AttrTableComponent', () => {
  let component: AttrTableComponent;
  let fixture: ComponentFixture<AttrTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatTableModule,
        RouterModule
      ],
      declarations: [ 
        AttrTableComponent,
        LocationsMapStubComponent
        
       ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttrTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
