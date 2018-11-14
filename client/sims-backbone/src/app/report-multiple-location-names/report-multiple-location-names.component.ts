import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'app-report-multiple-location-names',
  providers: [ReportService],
  templateUrl: './report-multiple-location-names.component.html',
  styleUrls: ['./report-multiple-location-names.component.scss']
})
export class ReportMultipleLocationNamesComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.reportService.multipleLocationNames().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
