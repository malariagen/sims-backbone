import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'app-report-uncurated-locations',
  providers: [ReportService],
  templateUrl: './report-uncurated-locations.component.html',
  styleUrls: ['./report-uncurated-locations.component.scss']
})
export class ReportUncuratedLocationsComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.reportService.uncuratedLocations().subscribe(
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
