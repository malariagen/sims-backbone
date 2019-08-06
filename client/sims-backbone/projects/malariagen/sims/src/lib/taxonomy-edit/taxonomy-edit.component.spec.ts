import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxonomyEditComponent } from './taxonomy-edit.component';
import { ReactiveFormsModule, FormGroup, FormControl, Validators, FormBuilder, FormArray } from '@angular/forms';
import { MatAutocompleteTrigger, MatAutocomplete } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Taxonomy } from '../typescript-angular-client';

describe('TaxonomyEditComponent', () => {
  let component: TaxonomyEditComponent;
  let fixture: ComponentFixture<TaxonomyEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        MatSelectModule,
        MatInputModule
      ],
      declarations: [
        TaxonomyEditComponent,
        MatAutocomplete,
        MatAutocompleteTrigger
      ],
      providers: [
        FormBuilder
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxonomyEditComponent);
    component = fixture.componentInstance;

    component.taxaGroup = new FormGroup({
      partner_species: new FormControl('test partner species', Validators.required),
      taxa: new FormArray([])
    });

    component.taxonomies = [ <Taxonomy>{
      taxonomy_id: 1234,
      rank: 'species',
      name: 'Made up'
    }];
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
