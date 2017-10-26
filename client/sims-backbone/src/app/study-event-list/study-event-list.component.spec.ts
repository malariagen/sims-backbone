import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyEventListComponent } from './study-event-list.component';

describe('StudyEventListComponent', () => {
  let component: StudyEventListComponent;
  let fixture: ComponentFixture<StudyEventListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudyEventListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
