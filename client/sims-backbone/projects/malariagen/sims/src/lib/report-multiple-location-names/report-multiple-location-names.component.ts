import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'sims-report-multiple-location-names',
  providers: [ReportService],
  templateUrl: './report-multiple-location-names.component.html',
  styleUrls: ['./report-multiple-location-names.component.scss']
})
export class ReportMultipleLocationNamesComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.multipleLocationNames().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
