import { Component, OnInit } from '@angular/core';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'sims-report-missing-taxa',
  providers: [ReportService],
  templateUrl: './report-missing-taxa.component.html',
  styleUrls: ['./report-missing-taxa.component.scss']
})
export class ReportMissingTaxaComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService) { }

  ngOnInit() {

    this.reportService.missingTaxon().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
