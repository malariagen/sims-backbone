import { Component, Input, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';

import { DataSource } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import { Samples } from '../typescript-angular2-client/model/Samples';
import { Sample } from '../typescript-angular2-client/model/Sample';

import { Angular2Csv } from 'angular2-csv/Angular2-csv';

@Component({
  selector: 'app-event-list',
  templateUrl: './event-list.component.html',
  styleUrls: ['./event-list.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class EventListComponent implements OnInit {

  displayedColumns = ['oxford_id', 'partner_id', 'roma_id', 'doc', 'partner_location_name', 'location'];

  _events: Observable<Samples>;
  _studyName: string;
  dataSource: EventDataSource | null;
  count: number;

  downloadFileName: string = 'data.csv';

  constructor(private changeDetector: ChangeDetectorRef) { }

  ngOnInit() {
  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_sampling_events.csv'
  }

  @Input()
  set events(events: Observable<Samples>) {
    this._events = events;
    let eventDatabase = new EventDatabase();
    events.subscribe(samples => {
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
      samples.samples.forEach(sample => {
        let event = {};
        sample.identifiers.forEach(ident => {
          event[ident.identifier_type] = ident.identifier_value;
        });
        if (sample.location) {
          event['partner_location_name'] = '';
          sample.location.identifiers.forEach(ident => {
            let ident_value = ident.identifier_value;
            if (this._studyName) {
              if (ident.study_name == this._studyName) {
                event['partner_location_name'] = ident_value;
              }
            } else {
              event['partner_location_name'] = event['partner_location_name'] + ident_value;
            }
          });
          event['location'] = '<a href="location/' + sample.location.latitude + '/' + sample.location.longitude + '">' + sample.location.latitude + ', ' + sample.location.longitude + '</a>';
        }
        event['doc'] = sample.doc;
        eventDatabase.addEvent(event);
      });
    });
    this.dataSource = new EventDataSource(eventDatabase);

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