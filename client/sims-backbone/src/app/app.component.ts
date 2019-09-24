import { Component } from '@angular/core';

import { MatDialog } from '@angular/material/dialog';

import { EventSetAddDialogComponent } from '@malariagen/sims';
import { TranslateService } from '@ngx-translate/core';

import { marker as _ } from '@biesbjerg/ngx-translate-extract-marker';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = _('sims.menu.title');
    addEventSets = _('sims.menu.addEventSets');
    studies = _('sims.menu.studies');
    locations = _('sims.menu.locations');
    taxa = _('sims.menu.taxa');
    eventSets = _('sims.menu.eventSets');
    search = _('sims.menu.search');
    reports = _('sims.menu.reports');

    constructor(public dialog: MatDialog, private translate: TranslateService) {
        translate.setDefaultLang('en');
    }

    addEventSet(action) {

        let dialogRef = this.dialog.open(EventSetAddDialogComponent, {
            width: '600px'
        });

    }

}
