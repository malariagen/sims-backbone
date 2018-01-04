import { Component, OnInit, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { ErrorDialogComponent } from '../error-dialog/error-dialog.component';

import { EventSet } from '../typescript-angular-client/model/eventSet';
import { EventSets } from '../typescript-angular-client/model/eventSets';

import { EventSetService } from '../typescript-angular-client/api/eventSet.service';


import { HttpClient } from '@angular/common/http';

import { BASE_PATH } from '../typescript-angular-client/variables';

import { environment } from '../../environments/environment';

@Component({
  selector: 'app-event-set-edit-dialog',
  providers: [
    {
      provide: BASE_PATH,
      useValue: environment.eventSetApiLocation
      
    },
    {
      provide: EventSetService,
      useFactory: (httpClient, basePath) => new EventSetService(httpClient, basePath, undefined),
      deps: [
        HttpClient,
        BASE_PATH
      ]
    }
  ],
  templateUrl: './event-set-edit-dialog.component.html',
  styleUrls: ['./event-set-edit-dialog.component.scss']
})
export class EventSetEditDialogComponent implements OnInit {


  eventSets: EventSet[];

  ngOnInit() {
  }

  constructor(private eventSetService: EventSetService, public dialog: MatDialog,
    public dialogRef: MatDialogRef<EventSetEditDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any) {

    this.eventSetService.downloadEventSets().subscribe(
      (eventSets: EventSets) => {
        this.eventSets = eventSets.event_sets;
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
