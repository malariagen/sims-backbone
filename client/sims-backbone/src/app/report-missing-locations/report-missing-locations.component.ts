import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';

@Component({
  selector: 'app-report-missing-locations',
  providers: [ReportService],
  templateUrl: './report-missing-locations.component.html',
  styleUrls: ['./report-missing-locations.component.scss']
})

export class ReportMissingLocationsComponent implements OnInit {
  studies: Studies;

  constructor(private reportService: ReportService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.reportService.missingLocations().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
