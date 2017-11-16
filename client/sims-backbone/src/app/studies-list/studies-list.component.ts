import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';
import { Study } from '../typescript-angular-client/model/study';
import { StudyService } from '../typescript-angular-client/api/study.service';

@Component({
  selector: 'app-studies-list',
  providers: [ StudyService ],
  templateUrl: './studies-list.component.html',
  styleUrls: ['./studies-list.component.css']
})
export class StudiesListComponent implements OnInit {

  studies: Studies;

  constructor(private studyService: StudyService) { }

  ngOnInit() {

    this.studyService.downloadStudies().subscribe(
      (studies) => {
        this.studies = studies;
        console.log(this.studies);
      },
      (err) => {
        
        if (err.status == 401) {
          //Unauth - will be dealt with via auth.service.ts
        } else {
          console.error(err);
        }
      },
      () => { console.log("Downloaded studies") }
    )
  }

}
