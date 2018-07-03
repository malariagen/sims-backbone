import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SampleOverviewComponent } from './sample-overview.component';
import { Component, Input } from '@angular/core';
import { SamplingEvents } from '../typescript-angular-client';

@Component({ selector: 'app-event-detail', template: '' })
class EventDetailStubComponent {
  @Input() samplingEvents: SamplingEvents;

}
describe('SampleOverviewComponent', () => {
  let component: SampleOverviewComponent;
  let fixture: ComponentFixture<SampleOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        SampleOverviewComponent,
        EventDetailStubComponent
       ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SampleOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
