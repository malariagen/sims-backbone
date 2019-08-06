import { Component, Input, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, SimpleChanges, ViewChild } from '@angular/core';

import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource, MatTable } from '@angular/material/table';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';

import { EventSetEditDialogComponent } from '../event-set-edit-dialog/event-set-edit-dialog.component';

import { AfterViewChecked, AfterViewInit } from '@angular/core';
import { SamplingEventsSource } from '../sampling-event.datasource';
import { SamplingEventsService } from '../sampling-events.service';
import { tap } from 'rxjs/operators';
import { SamplingEvent } from '../typescript-angular-client';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';

@Component({
  selector: 'sims-event-list',
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
  _pageSize: number = 20;
  
  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatTable, { static: true }) table;

  selectedEvents = new Set<string>();

  downloadFileName = 'data.csv';

  jsonDownloadFileName = 'data.json';


  @Input()
  filter: string;

  @Input()
  set eventSetName(eventSetName) {
    this._eventSetName = eventSetName;
    this.downloadFileName = eventSetName + '_samplingEvents.csv';
    this.jsonDownloadFileName = eventSetName + '_samplingEvents.json';
  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_samplingEvents.csv';
    this.jsonDownloadFileName = studyName + '_samplingEvents.json';
  }

  constructor(private changeDetector: ChangeDetectorRef, public dialog: MatDialog, private samplingEventsService: SamplingEventsService) { }

  ngOnInit(): void {

    this._dataSource = new SamplingEventsSource(this.samplingEventsService);

    // Recalcuate the column headers when the data changes
    const obs: Observable<SamplingEvent[]> = this._dataSource.connect(this.table);

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

  loadEventsPage() {
    this._dataSource.loadEvents(this.filter,
      'asc',
      this.paginator.pageIndex,
      this.paginator.pageSize
    );

  }

  defineColumnHeaders(samplingEvents) {

    if (samplingEvents === undefined) {
      return;
    }

    let columnsForDisplay = ['sampling_event_id', 'individual_id'];
    columnsForDisplay = columnsForDisplay.concat(this._dataSource.attrTypes);
    columnsForDisplay = columnsForDisplay.concat(['doc', 'partner_location_name', 'location_curated_name', 'location']);

    if (columnsForDisplay !== this.displayedColumns) {
      this.displayedColumns = columnsForDisplay;
      this.changeDetector.markForCheck();
    }

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
    const dialogData = {
      action: action,
      items: this.selectedEvents,
      eventSet: this._eventSetName
    };

    const dialogRef = this.dialog.open(EventSetEditDialogComponent, {
      width: '400px',
      data: dialogData
    });

    dialogRef.afterClosed().subscribe(result => {
      if (action === 'Remove') {
        this.loadEventsPage();
        this.changeDetector.markForCheck();
      }
    });
  }
}
