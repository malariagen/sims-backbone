import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetListComponent } from './event-set-list.component';

describe('EventSetListComponent', () => {
  let component: EventSetListComponent;
  let fixture: ComponentFixture<EventSetListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventSetListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
