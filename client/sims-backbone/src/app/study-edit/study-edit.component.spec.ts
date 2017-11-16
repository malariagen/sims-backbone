import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyEditComponent } from './study-edit.component';

describe('StudyEditComponent', () => {
  let component: StudyEditComponent;
  let fixture: ComponentFixture<StudyEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudyEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
