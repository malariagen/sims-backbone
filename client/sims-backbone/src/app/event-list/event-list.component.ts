import { Component, Input, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';

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

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EventListComponent implements OnInit {

  displayedColumns = ['study_id', 'oxford_id', 'partner_id', 'roma_id', 'sanger_lims_id', 'doc', 'partner_species', 'taxa', 'partner_location_name', 'location_curated_name', 'location'];

  _events: Observable<SamplingEvents>;
  _studyName: string;
  _eventSetName: string;
  dataSource: EventDataSource | null;
  eventDatabase: EventDatabase;
  count: number;

  selectedEvents = new Set<string>();

  downloadFileName: string = 'data.csv';

  constructor(private changeDetector: ChangeDetectorRef, public dialog: MatDialog) { }

  ngOnInit() {
  }

  @Input()
  set eventSetName(eventSetName) {
    this._eventSetName = eventSetName;
    this.downloadFileName = eventSetName + '_sampling_events.csv'
  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_sampling_events.csv'
  }

  @Input()
  set events(events: Observable<SamplingEvents>) {
    if (!events) {
      return;
    }
    this._events = events;

    this.loadEvents();
  }

  loadEvents() {
    let eventDatabase = new EventDatabase();
    this._events.subscribe(samples => {
      //console.log(samples);
      this.count = samples.count;
      /*
      This nearly works and might in future...
      samples.samples.forEach(sample => {
        sample.identifiers.forEach(ident => {
          if (this.displayedColumns.indexOf(ident.identifier_type) < 0) {
            //This doesn't work as the table doesn't reload the displayedColumns
            this.displayedColumns.push(ident.identifier_type);
            console.log("Unexpected identifier:" + ident.identifier_type);
          }
        });
      });
      // Hacky column change detection
      // https://stackoverflow.com/questions/40829951/angular2-ngfor-onpush-change-detection-with-array-mutations
      //this.displayedColumns = this.displayedColumns.slice(); 
      //https://stackoverflow.com/questions/42067346/angular2-onpush-change-detection-and-ngfor     
      this.changeDetector.markForCheck();
      */
      samples.sampling_events.forEach((sample: SamplingEvent) => {
        let event = {};
        event['doc'] = sample.doc;
        event['partner_species'] = sample.partner_species;
        event['study_id'] = sample.study_id;
        sample.identifiers.forEach(ident => {
          if (ident.identifier_type in event) {
            let ids : Array<String> = event[ident.identifier_type].split(';');
            //Avoid duplicates from different sources
            if (!ids.includes(ident.identifier_value)) {
              event[ident.identifier_type] = [ event[ident.identifier_type], ident.identifier_value].join(';');
            }
            
          } else {
            event[ident.identifier_type] = ident.identifier_value;
          }

        });
        if (sample.location) {
          event['partner_location_name'] = '';
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
          event['location_curated_name'] = sample.location.curated_name;
          event['location'] = '<a href="location/' + sample.location.latitude + '/' + sample.location.longitude + '">' + sample.location.latitude + ', ' + sample.location.longitude + '</a>';
        }
        if (sample.partner_taxonomies) {
          let taxas = [];
          sample.partner_taxonomies.forEach((taxa: Taxonomy) => {
            taxas.push(taxa.taxonomy_id);
          })
          event['taxa'] = taxas.join(';');
        }
        event['id'] = sample.samplingEvent_id;
        eventDatabase.addEvent(event);
      });
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
