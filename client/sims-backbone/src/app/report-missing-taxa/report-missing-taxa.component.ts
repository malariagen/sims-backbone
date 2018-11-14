import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';

import { ReportService } from '../typescript-angular-client/api/report.service';


@Component({
  selector: 'app-report-missing-taxa',
  providers: [ReportService],
  templateUrl: './report-missing-taxa.component.html',
  styleUrls: ['./report-missing-taxa.component.scss']
})
export class ReportMissingTaxaComponent implements OnInit {

  studies: Studies;

  constructor(private reportService: ReportService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.reportService.missingTaxon().subscribe(
      (studies) => {
        this.studies = studies;
      }
    )
  }

}
