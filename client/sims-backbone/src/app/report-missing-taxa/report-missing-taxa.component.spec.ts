import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMissingTaxaComponent } from './report-missing-taxa.component';

describe('ReportMissingTaxaComponent', () => {
  let component: ReportMissingTaxaComponent;
  let fixture: ComponentFixture<ReportMissingTaxaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ReportMissingTaxaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportMissingTaxaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
