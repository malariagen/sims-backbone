import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IdentifierTableComponent } from './identifier-table.component';

describe('IdentifierTableComponent', () => {
  let component: IdentifierTableComponent;
  let fixture: ComponentFixture<IdentifierTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IdentifierTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IdentifierTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
