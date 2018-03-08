import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMissingDetailedLocationsComponent } from './report-missing-detailed-locations.component';

describe('ReportMissingDetailedLocationsComponent', () => {
  let component: ReportMissingDetailedLocationsComponent;
  let fixture: ComponentFixture<ReportMissingDetailedLocationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportMissingDetailedLocationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportMissingDetailedLocationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
