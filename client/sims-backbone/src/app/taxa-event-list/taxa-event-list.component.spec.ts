import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaEventListComponent } from './taxa-event-list.component';

describe('TaxaEventListComponent', () => {
  let component: TaxaEventListComponent;
  let fixture: ComponentFixture<TaxaEventListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxaEventListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxaEventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
