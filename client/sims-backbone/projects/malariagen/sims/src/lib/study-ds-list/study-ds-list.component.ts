import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-study-ds-list',
  templateUrl: './study-ds-list.component.html',
  styleUrls: ['./study-ds-list.component.scss']
})
export class StudyDsListComponent implements OnInit {

  studyName: string;
  
  filter: string;

  downloadFileName: string;

  jsonDownloadFileName: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.studyName = pmap.get('studyName');
    });
    this.filter = 'studyId:' + this.studyName;
    this.downloadFileName = 'derivative_samples_study_' + this.studyName + '.csv';
    this.jsonDownloadFileName = 'derivative_samples_study_' + this.studyName + '.json';
  }

}
