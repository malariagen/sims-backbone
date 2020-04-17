import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, FormArray, FormControl, FormBuilder, Validators } from '@angular/forms';

import { Study } from '../typescript-angular-client/model/study';
import { Taxonomy } from '../typescript-angular-client/model/taxonomy';
import { Taxonomies } from '../typescript-angular-client/model/taxonomies';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';
import { StudyService } from '../typescript-angular-client/api/study.service';
import { DocumentService } from '../typescript-angular-client/api/document.service';
import { Document } from '../typescript-angular-client/model/document';
import { Documents } from '../typescript-angular-client';
import { Observable } from 'rxjs';
import { HttpResponse } from '@angular/common/http';

@Component({
  selector: 'sims-study-edit',
  providers: [StudyService, MetadataService],
  templateUrl: './study-edit.component.html',
  styleUrls: ['./study-edit.component.css']
})
export class StudyEditComponent implements OnInit {

  public studyEvents = '/study/events';

  taxonomies: Taxonomy[];

  studyCode: string;

  study: Study;

  public studyForm: FormGroup;

  fileForm: FormGroup;
  @ViewChild('content', { static: false }) inputFile;
  uploadFile: File;

  @ViewChild("fileUpload", { static: false }) fileUpload: ElementRef;
  files: Set<File> = new Set();

  public documents: Documents = null;

  static initTaxaControl(taxaId) {
    return new FormGroup({
      taxonomy_id: new FormControl(taxaId, Validators.required)
    });
  }

  constructor(private studyService: StudyService, private metadataService: MetadataService,
    private documentService: DocumentService,
    private route: ActivatedRoute, private _fb: FormBuilder) { }

  ngOnInit() {

    this.metadataService.getTaxonomyMetadata().subscribe(
      (taxas: Taxonomies) => {
        this.taxonomies = taxas.taxonomies;
      }
    );

    this.route.paramMap.subscribe(pmap => {
      this.studyCode = pmap.get('studyCode');
    });

    this.fileForm = this._fb.group({
      'study_name': this.studyCode,
      'doc_type': ''
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
          const identControl = new FormGroup({
            partner_species: new FormControl(ident.partner_species, Validators.required),
            taxa: this._fb.array([])
          });

          const taxasControl = <FormArray>identControl.controls['taxa'];

          ident.taxa.forEach(taxa => {
            const taxaControl = StudyEditComponent.initTaxaControl(taxa.taxonomy_id);
            taxasControl.push(taxaControl);
          });
          formIdents.push(identControl);
        });
      },
      (err) => console.error(err)
    );
    this.getDocuments();
  }

  getDocuments() {
    this.documentService.downloadDocumentsByStudy(this.studyCode).subscribe((docs) => {
      this.documents = docs;
    },
      (err) => console.error(err));
  }

  public onSubmit({ value, valid }: { value: Study, valid: boolean }): void {

    this.studyService.updateStudy(value.code, value)
      .subscribe(
        (x) => {
          console.log('Submitted');
        },
        (e) => { console.log('onError: %o', e); },
        () => {
          console.log('Completed update.');
        }
      );
  }

  public onSubmitFile({ value, valid }: { value: Document, valid: boolean }): void {

    const fileUpload = this.fileUpload.nativeElement;

    let self = this;
    this.files.forEach(function (upload_file) {

      self.documentService.createDocument(self.studyCode, value.doc_type, upload_file)
        .subscribe(
          (x) => {
            this.getDocuments();
          },
          (e) => { console.log('onError: %o', e); },
          () => {
            console.log('Completed update.');
          }
        )
    });
  }


  onFilesAdded() {
    const files: { [key: string]: File } = this.fileUpload.nativeElement.files;
    for (let key in files) {
      if (!isNaN(parseInt(key))) {
        this.files.add(files[key]);
      }
    }
  }

  download(doc: Document) {
    var reader = new FileReader();
    this.documentService.downloadDocumentContent(doc.document_id).subscribe((response) => {
      let filename: string = doc.doc_name;
      let downloadLink = document.createElement('a');
      downloadLink.href = window.URL.createObjectURL(response);
      downloadLink.setAttribute('download', filename);
      document.body.appendChild(downloadLink);
      downloadLink.click();
    }
    );
  }
  getPartnerSpecies() {
    return (<FormArray>(this.studyForm.controls['partner_species'])).controls;
  }
}
