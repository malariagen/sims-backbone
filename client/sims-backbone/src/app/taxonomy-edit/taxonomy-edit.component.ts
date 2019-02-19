import { Component, Input, OnInit } from '@angular/core';

import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { StudyEditComponent } from '../study-edit/study-edit.component';
import { Taxonomy } from '../typescript-angular-client/model/taxonomy';
import { Taxonomies } from '../typescript-angular-client/model/taxonomies';

@Component({
  selector: 'app-taxonomy-edit',
  templateUrl: './taxonomy-edit.component.html',
  styleUrls: ['./taxonomy-edit.component.css']
})
export class TaxonomyEditComponent implements OnInit {

  @Input('group') taxaGroup: FormGroup;

  @Input('taxonomies') taxonomies: Taxonomy[];

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {

  }

  addClassification() {
    const taxasControl = <FormArray>this.taxaGroup.controls['taxa'];
    let newTaxaControl = StudyEditComponent.initTaxaControl(null);
    taxasControl.push(newTaxaControl);

  }

  removeClassification(i: number) {
    const taxasControl = <FormArray>this.taxaGroup.controls['taxa'];
    taxasControl.removeAt(i);
  }

  displayFn(taxonomyId: number): string {
    
    let ret = String(taxonomyId);

    if (this.taxonomies) {
      this.taxonomies.forEach(taxa => {
        if (taxa.taxonomyId == taxonomyId) {
          ret = taxa.taxonomyId + " " + taxa.rank + " " + taxa.name;
        }
      });
    }
    if (taxonomyId) {
      return ret;
    } else {
      return '';
    }
  }

  getTaxas() {
    return (<FormArray>(this.taxaGroup.controls['taxa'])).controls;
  }
}
