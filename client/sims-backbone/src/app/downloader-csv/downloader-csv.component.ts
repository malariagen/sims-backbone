import { Component, Input } from '@angular/core';
import { SamplingEventDisplayPipe } from '../sampling-event-display.pipe';
import { SamplingEventsService } from '../sampling-events.service';
import { CollectionViewer } from '@angular/cdk/collections';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

import * as FileSaver from 'file-saver';
import { Observable } from 'rxjs/Observable';
import { SamplingEvent } from '../typescript-angular-client';
import { SamplingEventsSource } from '../sampling-event.datasource';

@Component({
  selector: 'app-downloader-csv',
  providers: [SamplingEventsService, SamplingEventDisplayPipe],
  templateUrl: './downloader-csv.component.html',
  styleUrls: ['./downloader-csv.component.scss']
})
export class DownloaderCsvComponent implements CollectionViewer {

  header: boolean = false;
  separator: string = '\t';
  csvString: string = '';
  pageSize: number = 1000;
  pageNumber: number = 0;

  _dataSource: SamplingEventsSource;
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  @Input()
  fileName: string = 'data.csv';
  @Input()
  filter: string;
  @Input()
  downloaderName: string = 'Download CSV';
  @Input()
  headers: string[] = [];

  constructor(private displayPipe: SamplingEventDisplayPipe, private samplingEventsService: SamplingEventsService) {
  }

  build() {

    this.pageNumber = 0;
    this._dataSource = new SamplingEventsSource(this.samplingEventsService);
    
    let obs: Observable<SamplingEvent[]> = this._dataSource.connect(this);


    obs.subscribe({
      next: sevent => this.extractEventsToString(sevent),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });
    this._dataSource.loadEvents(this.filter, 'asc', this.pageNumber, this.pageSize);


  }

  extractEventsToString(d) {

    let tabText = '';
    d.forEach(k => {

      if (!this.header) {
        this.headers.forEach(h => {
          tabText += '"' + h + '"' + this.separator;
        });

        if (tabText.length > 0) {
          tabText = tabText.slice(0, -1);
          tabText += '\r\n';
        }
        this.header = true;
      }
      this.headers.forEach(field => {

        let text: string = this.displayPipe.transform(k, field, null, this._dataSource.locations);
        if (text) {
          if (text.startsWith('<a href="location/')) {
            let res = text.match(/(>)([0-9,.-\s]*)(<)/);
            if (res) {
              if (res.length > 2) {
                text = res[2];
              }
            } else {
              text = "";
            }
          }
          tabText += '"' + text + '"' + this.separator;
        } else {
          tabText += '""' + this.separator;
        }
      });
      tabText = tabText.slice(0, -1);
      tabText += '\r\n';
    });

    if (tabText != '') {
      this.csvString += tabText;
      if ((this.pageNumber + 1) * this.pageSize < this._dataSource.samplingEventCount) {
        this.pageNumber++;
        this._dataSource.loadEvents(this.filter, 'asc', this.pageNumber, this.pageSize);
      } else {
        this.buildDownloader(this.csvString);
        this.header = false;
        this.csvString = '';
      }
    }
  }
  private buildDownloader(data) {

    var blob = new Blob([data], { type: 'text/csv;charset=utf-8' });

    FileSaver.saveAs(blob, this.fileName);

  }
}
