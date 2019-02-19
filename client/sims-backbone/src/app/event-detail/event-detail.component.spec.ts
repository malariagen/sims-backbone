import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventDetailComponent } from './event-detail.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { Component, Input } from '@angular/core';

@Component({ selector: 'app-attr-table', template: '' })
class AttrsTableStubComponent {
  @Input() attrs;
}

@Component({ selector: 'app-location-view', template: '' })
class LocationViewStubComponent {
  @Input() location;
}
@Component({ selector: 'app-individual-view', template: '' })
class IndividualViewStubComponent {
  @Input() individualId;
}

describe('EventDetailComponent', () => {
  let component: EventDetailComponent;
  let fixture: ComponentFixture<EventDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [
        EventDetailComponent,
        AttrsTableStubComponent,
        LocationViewStubComponent,
        IndividualViewStubComponent
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
