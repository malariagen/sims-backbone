import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportsComponent } from './reports.component';
import { MatToolbarModule } from '@angular/material';
import { Component } from '@angular/core';

@Component({ selector: 'router-outlet', template: '' })
class RouterOutletStubComponent { }

describe('ReportsComponent', () => {
  let component: ReportsComponent;
  let fixture: ComponentFixture<ReportsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatToolbarModule

      ],
      declarations: [
        ReportsComponent,
        RouterOutletStubComponent
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
