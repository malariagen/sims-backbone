import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportUncuratedLocationsComponent } from './report-uncurated-locations.component';

describe('ReportUncuratedLocationsComponent', () => {
  let component: ReportUncuratedLocationsComponent;
  let fixture: ComponentFixture<ReportUncuratedLocationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportUncuratedLocationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportUncuratedLocationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
