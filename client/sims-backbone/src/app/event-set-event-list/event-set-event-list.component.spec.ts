import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEventListComponent } from './event-set-event-list.component';

describe('EventSetEventListComponent', () => {
  let component: EventSetEventListComponent;
  let fixture: ComponentFixture<EventSetEventListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventSetEventListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
