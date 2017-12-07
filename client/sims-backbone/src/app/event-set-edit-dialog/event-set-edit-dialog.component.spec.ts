import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEditDialogComponent } from './event-set-edit-dialog.component';

describe('EventSetEditDialogComponent', () => {
  let component: EventSetEditDialogComponent;
  let fixture: ComponentFixture<EventSetEditDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EventSetEditDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEditDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
