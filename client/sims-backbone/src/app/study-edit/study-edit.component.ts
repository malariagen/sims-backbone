import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { Studies } from '../typescript-angular-client/model/studies';
import { Study } from '../typescript-angular-client/model/study';
import { Taxonomy } from '../typescript-angular-client/model/taxonomy';
import { Taxonomies } from '../typescript-angular-client/model/taxonomies';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';
import { StudyService } from '../typescript-angular-client/api/study.service';

@Component({
  selector: 'app-study-edit',
  providers: [StudyService, MetadataService],
  templateUrl: './study-edit.component.html',
  styleUrls: ['./study-edit.component.css']
})
export class StudyEditComponent implements OnInit {

  constructor(private studyService: StudyService, private metadataService: MetadataService, private route: ActivatedRoute, private _fb: FormBuilder) { }

  public studyEvents: string = '/study/events';

  taxonomies: Taxonomy[];

  studyCode: string;

  study: Study;

  public studyForm: FormGroup;

  ngOnInit() {

    this.metadataService.getTaxonomyMetadata().subscribe(
      (taxas: Taxonomies) => {
        this.taxonomies = taxas.taxonomies;
      }
    );

    this.route.paramMap.subscribe(pmap => {
      this.studyCode = pmap.get('studyCode');
    });

    this.studyService.downloadStudy(this.studyCode).subscribe(
      (study) => {

        this.study = study;
        this.studyForm = this._fb.group(
          {
            code: [this.study.code, [Validators.required]],
            name: [this.study.name, [Validators.required]],
            partner_species: this._fb.array([]),
          }
        );
        const formIdents = <FormArray>this.studyForm.controls['partner_species'];

        this.study.partner_species.forEach(ident => {
          let identControl = new FormGroup({
            partner_species: new FormControl(ident.partner_species, Validators.required),
            taxa: this._fb.array([])
          });

          const taxasControl = <FormArray>identControl.controls['taxa'];

          ident.taxa.forEach(taxa => {
            let taxaControl = StudyEditComponent.initTaxaControl(taxa.taxonomy_id);
            taxasControl.push(taxaControl);
          });
          formIdents.push(identControl);
        });
      },
      (err) => console.error(err)
    );

  }

  static initTaxaControl(taxa_id) {
    return new FormGroup({
      taxonomy_id: new FormControl(taxa_id, Validators.required)
    });
  }

  public onSubmit({ value, valid }: { value: Study, valid: boolean }): void {

    this.studyService.updateStudy(value.code, value)
      .subscribe(
        (x) => {
          console.log("Submitted");
        },
        (e) => { console.log('onError: %o', e); },
        () => {
          console.log('Completed update.');
        }
      );
  }

}
