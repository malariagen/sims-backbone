import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IdentifierTableComponent } from './identifier-table.component';
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

describe('IdentifierTableComponent', () => {
  let component: IdentifierTableComponent;
  let fixture: ComponentFixture<IdentifierTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatTableModule,
        RouterModule
      ],
      declarations: [ 
        IdentifierTableComponent,
        LocationsMapStubComponent
        
       ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IdentifierTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
