import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'sims-report-multiple-location-gps',
  providers: [ReportService],
  templateUrl: './report-multiple-location-gps.component.html',
  styleUrls: ['./report-multiple-location-gps.component.scss']
})
export class ReportMultipleLocationGpsComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.multipleLocationGPS().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
