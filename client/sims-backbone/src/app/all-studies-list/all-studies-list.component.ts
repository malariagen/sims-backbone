import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';
import { Study } from '../typescript-angular-client/model/study';
import { StudyService } from '../typescript-angular-client/api/study.service';
import { MetadataService } from '../typescript-angular-client';

@Component({
  selector: 'app-all-studies-list',
  providers: [StudyService, MetadataService],
  templateUrl: './all-studies-list.component.html',
  styleUrls: ['./all-studies-list.component.scss']
})
export class AllStudiesListComponent implements OnInit {

  studies: Studies;

  constructor(private studyService: StudyService, private metadataService: MetadataService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.studyService.downloadStudies().subscribe(
      (studies) => {
        this.studies = studies;
      }
    );
    this.warmUp();
  }

  warmUp() {
    this.metadataService.getAttrTypes().subscribe();
    this.metadataService.getTaxonomyMetadata().subscribe();
    this.studyService.downloadStudy("9999").subscribe();
  }
}
