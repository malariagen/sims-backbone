import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'sims-report-uncurated-locations',
  providers: [ReportService],
  templateUrl: './report-uncurated-locations.component.html',
  styleUrls: ['./report-uncurated-locations.component.scss']
})
export class ReportUncuratedLocationsComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.uncuratedLocations().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
