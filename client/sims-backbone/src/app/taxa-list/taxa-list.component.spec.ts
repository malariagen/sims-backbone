import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaListComponent } from './taxa-list.component';

describe('TaxaListComponent', () => {
  let component: TaxaListComponent;
  let fixture: ComponentFixture<TaxaListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxaListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
