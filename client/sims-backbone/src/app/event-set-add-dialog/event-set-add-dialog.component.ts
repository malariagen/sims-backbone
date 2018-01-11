import { Component } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material';

import { ErrorDialogComponent } from '../error-dialog/error-dialog.component';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSets } from '../typescript-angular-client/model/eventSets';

import { EventSetService } from '../typescript-angular-client/api/eventSet.service';


@Component({
  selector: 'app-event-set-add-dialog',
  templateUrl: './event-set-add-dialog.component.html',
  styleUrls: ['./event-set-add-dialog.component.scss']
})

export class EventSetAddDialogComponent {

  eventSet: string;

  constructor(private eventSetService: EventSetService, public dialog: MatDialog,
    public dialogRef: MatDialogRef<EventSetAddDialogComponent>) {

  }

  close(): void {
    this.dialogRef.close();
  }

  save(): void {


    this.eventSetService.createEventSet(this.eventSet).subscribe(
      (x) => {
        //console.log("Submitted");
      },
      (e) => {
        //console.log(e);
        let dialogRef = this.dialog.open(ErrorDialogComponent, {
          width: '250px',
          data: { name: 'Error on save', message: e.message }
        });

        dialogRef.afterClosed().subscribe(result => {
          //console.log('The dialog was closed');
        });
      },
      () => {
        //console.log('Completed update.');
      }
    );;


    this.dialogRef.close();
  }

}
