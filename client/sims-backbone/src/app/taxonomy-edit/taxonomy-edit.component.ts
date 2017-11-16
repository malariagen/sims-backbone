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

  taxonomies: Taxonomy[];

  constructor(private fb: FormBuilder, private metadataService: MetadataService) { }

  ngOnInit(): void {
    this.metadataService.getTaxonomyMetadata().subscribe(
      (taxas: Taxonomies) => {
        this.taxonomies = taxas.taxonomies;
        console.log('OnInit' + this);
      }
    );
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
    console.log(taxonomy_id);
    console.log(this);
    
    if (this.taxonomies) {
      console.log(this.taxonomies);
      this.taxonomies.forEach(taxa => {
        console.log(taxa.taxonomy_id + taxonomy_id);
        if (taxa.taxonomy_id == taxonomy_id) {
          return taxa.taxonomy_id + " " + taxa.rank + " " + taxa.name;
        }
      });
    }
    if (taxonomy_id) {
      return String(taxonomy_id);
    } else {
      return '';
    }
  }
}
