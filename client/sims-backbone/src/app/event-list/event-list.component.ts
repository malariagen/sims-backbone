import { Component, Input, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, SimpleChanges, ViewChild } from '@angular/core';

import { MatPaginator, MatSort, MatTableDataSource, MatTable } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';

import { EventSetEditDialogComponent } from '../event-set-edit-dialog/event-set-edit-dialog.component';

import { AfterViewChecked, AfterViewInit } from '@angular/core/src/metadata/lifecycle_hooks';
import { SamplingEventsSource } from '../sampling-event.datasource';
import { SamplingEventsService } from '../sampling-events.service';
import { tap } from 'rxjs/operators';
import { SamplingEventService, SamplingEvent } from '../typescript-angular-client';

@Component({
  selector: 'app-event-list',
  providers: [SamplingEventsService, SamplingEventService],
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EventListComponent implements OnInit, AfterViewInit {

  _dataSource: SamplingEventsSource;

  displayedColumns = [];

  _studyName: string;
  _eventSetName: string;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatTable) table;

  selectedEvents = new Set<string>();

  downloadFileName: string = 'data.csv';

  jsonDownloadFileName: string = 'data.json';

  constructor(private changeDetector: ChangeDetectorRef, public dialog: MatDialog, private samplingEventsService: SamplingEventsService) { }

  ngOnInit(): void {

    this._dataSource = new SamplingEventsSource(this.samplingEventsService);

    //Recalcuate the column headers when the data changes
    //this is not ideal because it may mean that columns are left out
    //if the columns used change over the result set
    //Also impacts when a csv download occurs - uses the same column definitions
    //
    let obs: Observable<SamplingEvent[]> = this._dataSource.connect(this.table);

    obs.subscribe({
      next: sevents => this.defineColumnHeaders(sevents),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });

    this._dataSource.loadEvents(this.filter, 'asc', 0, 50);

  }

  ngAfterViewInit() {

    if (this.paginator) {
      this.paginator.page
        .pipe(
          tap(() => this.loadEventsPage())
        )
        .subscribe();
    }
      
  }

  @Input()
  filter: string;

  @Input()
  set eventSetName(eventSetName) {
    this._eventSetName = eventSetName;
    this.downloadFileName = eventSetName + '_sampling_events.csv';
    this.jsonDownloadFileName = eventSetName + '_sampling_events.json';
  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_sampling_events.csv';
    this.jsonDownloadFileName = studyName + '_sampling_events.json';
  }

  loadEventsPage() {
    this._dataSource.loadEvents(this.filter,
      'asc',
      this.paginator.pageIndex,
      this.paginator.pageSize
    );
    
  }

  defineColumnHeaders(sampling_events) {

    if(sampling_events == undefined) {
      return;
    }
    this.displayedColumns = ['study_id'];
    sampling_events.forEach(data => {
      data.attrs.forEach(ident => {
        if (this.displayedColumns.indexOf(ident.attr_type) < 0) {
          this.displayedColumns.push(ident.attr_type);
        }
      });
    });
    this.displayedColumns = this.displayedColumns.concat(['doc', 'partner_species', 'taxa', 'partner_location_name', 'location_curated_name', 'location']);
    this.changeDetector.markForCheck();
  }


  select(row) {
    if (this.selectedEvents.has(row.sampling_event_id)) {
      this.selectedEvents.delete(row.sampling_event_id);
    } else {
      this.selectedEvents.add(row.sampling_event_id);
    }
  }

  selectAll() {

    this.table._data.forEach(data => {
      if (!this.selectedEvents.has(data.sampling_event_id)) {
        this.selectedEvents.add(data.sampling_event_id);
      }
    });
  }

  selectNone() {
    this.selectedEvents = new Set<string>();
  }

  editEventSet(action) {
    let dialogData = {
      action: action,
      items: this.selectedEvents,
      eventSet: this._eventSetName
    };

    let dialogRef = this.dialog.open(EventSetEditDialogComponent, {
      width: '400px',
      data: dialogData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (action == 'Remove') {
        this.loadEventsPage();
        this.changeDetector.markForCheck();
      }
    });
  }
}
