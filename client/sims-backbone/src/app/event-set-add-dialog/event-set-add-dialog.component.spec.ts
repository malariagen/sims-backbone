import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetAddDialogComponent } from './event-set-add-dialog.component';

describe('EventSetAddDialogComponent', () => {
  let component: EventSetAddDialogComponent;
  let fixture: ComponentFixture<EventSetAddDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventSetAddDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetAddDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
