import { Component, Input, OnInit } from '@angular/core';

import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { StudyEditComponent } from '../study-edit/study-edit.component';
import { Taxonomy } from '../typescript-angular-client/model/taxonomy';
import { Taxonomies } from '../typescript-angular-client/model/taxonomies';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';

@Component({
  selector: 'app-taxonomy-edit',
  providers: [MetadataService],
  templateUrl: './taxonomy-edit.component.html',
  styleUrls: ['./taxonomy-edit.component.css']
})
export class TaxonomyEditComponent implements OnInit {

  @Input('group') taxaGroup: FormGroup;

  @Input('taxonomies') taxonomies: Taxonomy[];

  constructor(private fb: FormBuilder, private metadataService: MetadataService) { }

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

  displayFn(taxonomy_id: number): string {
    
    let ret = String(taxonomy_id);

    if (this.taxonomies) {
      this.taxonomies.forEach(taxa => {
        if (taxa.taxonomy_id == taxonomy_id) {
          ret = taxa.taxonomy_id + " " + taxa.rank + " " + taxa.name;
        }
      });
    }
    if (taxonomy_id) {
      return ret;
    } else {
      return '';
    }
  }

  getTaxas() {
    return (<FormArray>(this.taxaGroup.controls['taxa'])).controls;
  }
}
