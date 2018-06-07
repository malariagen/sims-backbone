import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { SamplingEventsService } from '../sampling-events.service';
import { SamplingEventDisplayPipe } from '../sampling-event-display.pipe';
import { CollectionViewer } from '@angular/cdk/collections';
import { SamplingEventsSource } from '../sampling-event.datasource';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { SamplingEvent, SamplingEvents, SamplingEventService } from '../typescript-angular-client';

import * as FileSaver from 'file-saver';

@Component({
  selector: 'app-downloader-json',
  providers: [SamplingEventsService, SamplingEventService],
  templateUrl: './downloader-json.component.html',
  styleUrls: ['./downloader-json.component.scss']
})
export class DownloaderJsonComponent implements CollectionViewer {

  samplingEvents: SamplingEvents;
  pageSize: number = 1000;
  pageNumber: number = 0;

  _dataSource: SamplingEventsSource;
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  @Input()
  fileName: string = 'data.json';
  @Input()
  filter: string;
  @Input()
  downloaderName: string = 'Download JSON';
  @Input()
  headers: string[] = [];

  constructor(private samplingEventsService: SamplingEventsService) {

    this._dataSource = new SamplingEventsSource(this.samplingEventsService);

    let obs: Observable<SamplingEvent[]> = this._dataSource.connect(this);

    obs.subscribe({
      next: sevent => this.extractEvents(sevent),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });
  }

  build() {

    this.pageNumber = 0;

    this._dataSource.loadEvents(this.filter, 'asc', this.pageNumber, this.pageSize);

  }

  extractEvents(d: Array<SamplingEvent>) {

    if (d.length == 0) {
      return;
    }

    if (this.pageNumber == 0) {
      this.samplingEvents = <SamplingEvents>{};
      this.samplingEvents.sampling_events = [];
    }

    this.samplingEvents.sampling_events = this.samplingEvents.sampling_events.concat(d);


    if ((this.pageNumber + 1) * this.pageSize < this._dataSource.samplingEventCount) {
      this.pageNumber++;
      this._dataSource.loadEvents(this.filter, 'asc', this.pageNumber, this.pageSize);
    } else {
      this.samplingEvents.attr_types = this._dataSource.attrTypes;
      this.samplingEvents.count = this._dataSource.samplingEventCount;
      this.samplingEvents.locations = this._dataSource.locations;
      this.buildDownloader(JSON.stringify(this.samplingEvents));
    }

  }
  private buildDownloader(data) {

    var blob = new Blob([data], { type: 'application/json;charset=utf-8' });

    FileSaver.saveAs(blob, this.fileName);

  }
}
