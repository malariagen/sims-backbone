import { Component } from '@angular/core';

import { MatDialog } from '@angular/material/dialog';

import { EventSetAddDialogComponent } from '@malariagen/sims';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {

    constructor(public dialog: MatDialog) {
        
    }

    addEventSet(action) {

        let dialogRef = this.dialog.open(EventSetAddDialogComponent, {
            width: '600px'
        });

    }

}
