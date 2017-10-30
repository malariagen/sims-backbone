import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationEventListComponent } from './location-event-list.component';

describe('LocationEventListComponent', () => {
  let component: LocationEventListComponent;
  let fixture: ComponentFixture<LocationEventListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LocationEventListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LocationEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
