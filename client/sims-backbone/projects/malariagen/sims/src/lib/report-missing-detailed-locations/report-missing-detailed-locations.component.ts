import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';

@Component({
  selector: 'sims-report-missing-detailed-locations',
  providers: [ReportService],
  templateUrl: './report-missing-detailed-locations.component.html',
  styleUrls: ['./report-missing-detailed-locations.component.scss']
})

export class ReportMissingDetailedLocationsComponent implements OnInit {
  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.missingLocations(true).subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
