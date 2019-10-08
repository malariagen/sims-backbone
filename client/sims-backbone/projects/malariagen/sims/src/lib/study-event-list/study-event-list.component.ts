import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-study-event-list',
  templateUrl: './study-event-list.component.html',
  styleUrls: ['./study-event-list.component.css']
})
export class StudyEventListComponent implements OnInit {

  studyName: string;

  filter: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.studyName = pmap.get('studyName');
    });
    this.filter = 'studyId:' + this.studyName;
  }

}
