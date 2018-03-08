import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';

@Component({
  selector: 'app-report-missing-detailed-locations',
  providers: [ReportService],
  templateUrl: './report-missing-detailed-locations.component.html',
  styleUrls: ['./report-missing-detailed-locations.component.scss']
})

export class ReportMissingDetailedLocationsComponent implements OnInit {
  studies: Studies;

  constructor(private reportService: ReportService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.reportService.missingLocations(true).subscribe(
      (studies) => {
        this.studies = studies;
      },
      (err) => {

        if (err.status == 401) {
          this.oauthService.logOut();
          this.oauthService.initImplicitFlow();
        } else {
          console.error(err);
        }

      }
    )
  }

}
