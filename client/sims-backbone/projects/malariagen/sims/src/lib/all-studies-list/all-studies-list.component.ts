import { Component, OnInit } from '@angular/core';
import { StudyService, MetadataService, Studies } from '../typescript-angular-client';


@Component({
  selector: 'sims-all-studies-list',
  providers: [StudyService, MetadataService],
  templateUrl: './all-studies-list.component.html',
  styleUrls: ['./all-studies-list.component.scss']
})
export class AllStudiesListComponent implements OnInit {

  studies: Studies;

  constructor(private studyService: StudyService, private metadataService: MetadataService) { }

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
