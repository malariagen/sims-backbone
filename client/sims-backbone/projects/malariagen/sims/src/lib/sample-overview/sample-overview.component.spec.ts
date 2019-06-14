import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SampleOverviewComponent } from './sample-overview.component';
import { Component, Input } from '@angular/core';
import { SamplingEvents, OriginalSamples, DerivativeSamples, AssayData } from '../typescript-angular-client';

@Component({ selector: 'sims-event-detail', template: '' })
class EventDetailStubComponent {
  @Input() samplingEvents: SamplingEvents;

}
@Component({ selector: 'sims-os-detail', template: '' })
class OriginalSampleStubComponent {
  @Input() originalSamples: OriginalSamples;

}
@Component({ selector: 'sims-ds-detail', template: '' })
class DerivativeStubComponent {
  @Input() derivativeSamples: DerivativeSamples;

}
@Component({ selector: 'sims-ad-detail', template: '' })
class AssayDataStubComponent {
  @Input() assayData: AssayData;

}
describe('SampleOverviewComponent', () => {
  let component: SampleOverviewComponent;
  let fixture: ComponentFixture<SampleOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        SampleOverviewComponent,
        EventDetailStubComponent,
        OriginalSampleStubComponent,
        DerivativeStubComponent,
        AssayDataStubComponent
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
