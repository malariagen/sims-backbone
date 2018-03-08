import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AllStudiesListComponent } from './all-studies-list.component';

describe('AllStudiesListComponent', () => {
  let component: AllStudiesListComponent;
  let fixture: ComponentFixture<AllStudiesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AllStudiesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllStudiesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
