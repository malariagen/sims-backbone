import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxonomyEditComponent } from './taxonomy-edit.component';

describe('TaxonomyEditComponent', () => {
  let component: TaxonomyEditComponent;
  let fixture: ComponentFixture<TaxonomyEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TaxonomyEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxonomyEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
