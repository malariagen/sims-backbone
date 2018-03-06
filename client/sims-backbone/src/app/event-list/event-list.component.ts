import { Component, Input, Output, EventEmitter, ChangeDetectionStrategy, ChangeDetectorRef, SimpleChanges, Renderer } from '@angular/core';

import { MatPaginator, MatSort, MatTableDataSource } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import { EventSetEditDialogComponent } from '../event-set-edit-dialog/event-set-edit-dialog.component';

import { Identifier } from '../typescript-angular-client/model/identifier';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { SamplingEvent } from '../typescript-angular-client/model/samplingEvent';
import { Taxonomy } from '../typescript-angular-client/model/taxonomy';

import { Angular2Csv } from 'angular2-csv/Angular2-csv';
import { AfterViewChecked, AfterViewInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EventListComponent implements AfterViewInit {

  displayedColumns = ['study_id', 'oxford_id', 'partner_id', 'roma_id', 'sanger_lims_id', 'doc', 'partner_species', 'taxa', 'partner_location_name', 'location_curated_name', 'location'];

  _events: SamplingEvents;
  _studyName: string;
  _eventSetName: string;
  dataSource: EventDataSource | null;
  eventDatabase: EventDatabase;
  count: number;
  progress: number;

  _pageNumber: number;
  _pageSize: number;

  @Output() pageNumber = new EventEmitter<number>(true);
  @Output() pageSize = new EventEmitter<number>(true);

  selectedEvents = new Set<string>();

  downloadFileName: string = 'data.csv';

  jsonDownloadFileName: string = 'data.json';

  constructor(private changeDetector: ChangeDetectorRef, public dialog: MatDialog, private renderer: Renderer) { }

  ngAfterViewInit() {
    this._pageNumber = 0;
    this._pageSize = 1000;
    this.pageSize.emit(this._pageSize);
    this.pageNumber.emit(this._pageNumber);
  }

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

  @Input()
  set events(events: SamplingEvents) {
    if (!events) {
      return;
    }

    this.count = events.count;

    if (this._pageNumber == 0) {
      this._events = events;
    } else {
      this._events.sampling_events = this._events.sampling_events.concat(events.sampling_events);
    }
    let numLoaded = Math.min((this._pageNumber + 1) * this._pageSize, events.count);

    this.progress = (numLoaded / events.count) * 100;

    if (numLoaded < events.count) {
      this._pageNumber++;
      this.pageNumber.emit(this._pageNumber);
    } else {
      this.loadEvents();
    }

  }

  defineColumnHeaders(sampling_events) {
    this.displayedColumns = ['study_id'];
    sampling_events.forEach(sample => {
      sample.identifiers.forEach(ident => {
        if (this.displayedColumns.indexOf(ident.identifier_type) < 0) {
          this.displayedColumns.push(ident.identifier_type);
        }
      });
    });
    this.displayedColumns = this.displayedColumns.concat(['doc', 'partner_species', 'taxa', 'partner_location_name', 'location_curated_name', 'location']);
    this.changeDetector.markForCheck();
  }

  mapSamplingEventToRow(sample) {
    let event = {};
    event['doc'] = sample.doc;
    event['partner_species'] = sample.partner_species;
    event['study_id'] = sample.study_name;
    sample.identifiers.forEach(ident => {
      if (ident.identifier_type in event) {
        let ids: Array<String> = event[ident.identifier_type].split(';');
        //Avoid duplicates from different sources
        if (!ids.includes(ident.identifier_value)) {
          event[ident.identifier_type] = [event[ident.identifier_type], ident.identifier_value].join(';');
        }

      } else {
        event[ident.identifier_type] = ident.identifier_value;
      }

    });
    if (sample.location) {
      event['partner_location_name'] = '';
      if (sample.location.identifiers) {
        sample.location.identifiers.forEach(ident => {
          let ident_value = ident.identifier_value;
          if (this._studyName || event['study_id']) {
            if ((this._studyName && (ident.study_name == this._studyName)) ||
              event['study_id'] && (ident.study_name == event['study_id'])) {
              event['partner_location_name'] = ident_value;
            }
          } else {
            event['partner_location_name'] = event['partner_location_name'] + ident_value + '(' + ident.study_name + ');';
          }
        });
      }
      event['location_curated_name'] = sample.location.curated_name;
      if (sample.location.latitude) {
        event['location'] = '<a href="location/' + sample.location.latitude + '/' + sample.location.longitude + '">' + sample.location.latitude + ', ' + sample.location.longitude + '</a>';
      }
    }
    if (sample.partner_taxonomies) {
      let taxas = [];
      sample.partner_taxonomies.forEach((taxa: Taxonomy) => {
        taxas.push(taxa.taxonomy_id);
      })
      event['taxa'] = taxas.join(';');
    }
    event['id'] = sample.sampling_event_id;
    return event;
  }

  loadEvents() {
    let eventDatabase = new EventDatabase();
    let samples = this._events;

    //console.log(samples);
    this.count = samples.count;

    this.defineColumnHeaders(samples.sampling_events);

    samples.sampling_events.forEach((sample: SamplingEvent) => {
      let event = this.mapSamplingEventToRow(sample);
      eventDatabase.addEvent(event);
    });

    this.dataSource = new EventDataSource(eventDatabase);
    this.eventDatabase = eventDatabase;
  }

  select(row) {
    if (this.selectedEvents.has(row.id)) {
      this.selectedEvents.delete(row.id);
    } else {
      this.selectedEvents.add(row.id);
    }
  }

  selectAll() {
    this.eventDatabase.data.forEach(data => {
      if (!this.selectedEvents.has(data.id)) {
        this.selectedEvents.add(data.id);
      }
    })
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
        this.loadEvents();
        this.changeDetector.markForCheck();
      }
    });
  }

  downloadJSON() {
    let anchor = this.renderer.createElement(document.body, 'a');
    this.renderer.setElementStyle(anchor, 'visibility', 'hidden');
    this.renderer.setElementAttribute(anchor, 'href', 'data:application/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(this._events.sampling_events)));
    this.renderer.setElementAttribute(anchor, 'target', '_blank');
    this.renderer.setElementAttribute(anchor, 'download', this.jsonDownloadFileName);

    setTimeout(() => {
      this.renderer.invokeElementMethod(anchor, 'click');
      this.renderer.invokeElementMethod(anchor, 'remove');
    }, 5);
  }
}

export class EventDatabase {
  dataChange: BehaviorSubject<any[]> = new BehaviorSubject<any[]>([]);
  get data(): any[] { return this.dataChange.value; }
  constructor() {
  }
  addEvent(sample) {
    const copiedData = this.data.slice();
    copiedData.push(sample);
    this.dataChange.next(copiedData);
  }

}
export class EventDataSource extends DataSource<any> {
  constructor(private _exampleDatabase: EventDatabase) {
    super();
  }
  connect(): Observable<any[]> {
    return this._exampleDatabase.dataChange;
  }
  disconnect() { }
}
