import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AdDetailComponent } from './ad-detail.component';
import { Component, Input } from '@angular/core';

@Component({ selector: 'app-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
}
describe('AdDetailComponent', () => {
  let component: AdDetailComponent;
  let fixture: ComponentFixture<AdDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [ AdDetailComponent, AttrsTableStubComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
