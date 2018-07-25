import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaOsListComponent } from './taxa-os-list.component';

describe('TaxaOsListComponent', () => {
  let component: TaxaOsListComponent;
  let fixture: ComponentFixture<TaxaOsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxaOsListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxaOsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
