import { Component, OnInit } from '@angular/core';

import { marker as _ } from '@biesbjerg/ngx-translate-extract-marker';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent implements OnInit {

  reportMissingDetailedLocation = _('sims.report.missingDetailedLocation');
  reportMissingLocation = _('sims.report.missingLocation');
  reportMissingTaxa = _('sims.report.missingTaxa');
  reportUncuratedLocations = _('sims.report.uncuratedLocations');
  reportMultipleLocationGPS = _('sims.report.multipleLocationGPS');
  reportMultipleLocationNames = _('sims.report.multipleLocationNames');

  constructor() { }

  ngOnInit() {
  }

}
