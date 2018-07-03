import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SampleOverviewComponent } from './sample-overview.component';

describe('SampleOverviewComponent', () => {
  let component: SampleOverviewComponent;
  let fixture: ComponentFixture<SampleOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SampleOverviewComponent ]
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
