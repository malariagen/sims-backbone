import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEditComponent } from './event-set-edit.component';

describe('EventSetEditComponent', () => {
  let component: EventSetEditComponent;
  let fixture: ComponentFixture<EventSetEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventSetEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
