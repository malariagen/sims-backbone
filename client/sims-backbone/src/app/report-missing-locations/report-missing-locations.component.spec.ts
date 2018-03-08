import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMissingLocationsComponent } from './report-missing-locations.component';

describe('ReportMissingLocationsComponent', () => {
  let component: ReportMissingLocationsComponent;
  let fixture: ComponentFixture<ReportMissingLocationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportMissingLocationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportMissingLocationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
