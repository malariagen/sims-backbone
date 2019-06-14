import { Component } from '@angular/core';

import { MatDialog } from '@angular/material';

import { EventSetAddDialogComponent } from '@malariagen/sims';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'SIMS Backbone';

    constructor(public dialog: MatDialog) {

 
    }

    addEventSet(action) {

        let dialogRef = this.dialog.open(EventSetAddDialogComponent, {
            width: '600px'
        });

    }

}
