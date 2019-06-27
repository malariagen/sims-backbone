import { Component, OnInit } from '@angular/core';
import { StudyService } from '../typescript-angular-client/api/study.service';
import { Studies } from '../typescript-angular-client/model/studies';


@Component({
  selector: 'sims-all-studies-list',
  providers: [StudyService],
  templateUrl: './all-studies-list.component.html',
  styleUrls: ['./all-studies-list.component.scss']
})
export class AllStudiesListComponent implements OnInit {

  studies: Studies;

  constructor(private studyService: StudyService) { }

  ngOnInit() {

    this.studyService.downloadStudies().subscribe(
      (studies) => {
        this.studies = studies;
      }
    );
  }

}
