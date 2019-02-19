import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { ErrorDialogComponent } from '../error-dialog/error-dialog.component';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSets } from '../typescript-angular-client/model/eventSets';

import { EventSetService } from '../typescript-angular-client/api/eventSet.service';

import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-event-set-edit-dialog',
  providers: [EventSetService],
  templateUrl: './event-set-edit-dialog.component.html',
  styleUrls: ['./event-set-edit-dialog.component.scss']
})
export class EventSetEditDialogComponent {


  eventSets: EventSet[];

  constructor(private eventSetService: EventSetService,
    private oauthService: OAuthService,
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<EventSetEditDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {

    this.eventSetService.downloadEventSets().subscribe(
      (eventSets: EventSets) => {
        this.eventSets = eventSets.eventSets;
      }
    );
  }

  close(): void {
    this.dialogRef.close();
  }

  save(): void {
    if (this.data.action == 'Remove') {
      this.data.items.forEach(item => {
        this.eventSetService.deleteEventSetItem(this.data.eventSet, item).subscribe(
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
        );
      });
    } else if (this.data.action == 'Add') {
      this.data.items.forEach(item => {
        this.eventSetService.createEventSetItem(this.data.eventSet, item).subscribe(
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
      });
      this.data.eventSet = null;
    }
    this.dialogRef.close();
  }
}
