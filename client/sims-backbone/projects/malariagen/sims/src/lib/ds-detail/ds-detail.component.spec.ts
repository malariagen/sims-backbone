import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { DsDetailComponent } from './ds-detail.component';
import { Component, Input } from '@angular/core';

@Component({ selector: 'sims-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
}

describe('DsDetailComponent', () => {
  let component: DsDetailComponent;
  let fixture: ComponentFixture<DsDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [ DsDetailComponent, AttrsTableStubComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DsDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
