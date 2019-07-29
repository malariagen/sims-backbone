import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MockComponent } from 'ng-mocks';

import { AttrTableComponent } from './attr-table.component';
import { MatTableModule } from '@angular/material';
import { RouterModule } from '@angular/router';
import { LocationsMapComponent } from '../locations-map/locations-map.component';

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
        MockComponent(LocationsMapComponent)
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
