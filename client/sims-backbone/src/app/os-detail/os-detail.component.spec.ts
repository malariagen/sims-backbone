import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { OsDetailComponent } from './os-detail.component';
import { Component, Input } from '@angular/core';

@Component({ selector: 'app-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
}

describe('OsDetailComponent', () => {
  let component: OsDetailComponent;
  let fixture: ComponentFixture<OsDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [ OsDetailComponent, AttrsTableStubComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OsDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
