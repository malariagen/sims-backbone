import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';

@Component({
  selector: 'sims-report-missing-locations',
  providers: [ReportService],
  templateUrl: './report-missing-locations.component.html',
  styleUrls: ['./report-missing-locations.component.scss']
})

export class ReportMissingLocationsComponent implements OnInit {
  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.missingLocations().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
