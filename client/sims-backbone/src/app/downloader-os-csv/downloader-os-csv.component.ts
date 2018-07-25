import { Component, OnInit, Input } from '@angular/core';
import { OriginalSamplesService } from '../original-samples.service';
import { OriginalSampleService, OriginalSample } from '../typescript-angular-client';
import { OriginalSampleDisplayPipe } from '../original-sample-display.pipe';

import * as FileSaver from 'file-saver';
import { Observable, BehaviorSubject } from 'rxjs';
import { OriginalSamplesSource } from '../original-sample.datasource';
import { CollectionViewer } from '@angular/cdk/collections';

@Component({
  selector: 'app-downloader-os-csv',
  templateUrl: './downloader-os-csv.component.html',
  styleUrls: ['./downloader-os-csv.component.scss'],
  providers: [OriginalSamplesService, OriginalSampleService, OriginalSampleDisplayPipe],

})
export class DownloaderOsCsvComponent implements CollectionViewer {

  header: boolean = false;
  separator: string = '\t';
  csvString: string = '';
  pageSize: number = 1000;
  pageNumber: number = 0;

  _dataSource: OriginalSamplesSource;
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  @Input()
  fileName: string = 'data.csv';
  @Input()
  filter: string;
  @Input()
  downloaderName: string = 'Download CSV';
  @Input()
  headers: string[] = [];

  constructor(private displayPipe: OriginalSampleDisplayPipe, private originalSamplesService: OriginalSamplesService) {

    this._dataSource = new OriginalSamplesSource(this.originalSamplesService);

    let obs: Observable<OriginalSample[]> = this._dataSource.connect(this);


    obs.subscribe({
      next: sevent => this.extractEventsToString(sevent),
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

    this._dataSource.loadOriginalSamples(this.filter, 'asc', this.pageNumber, this.pageSize);


  }

  extractEventsToString(d: Array<OriginalSample>) {

    if (d.length == 0) {
      return;
    }

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
      if ((this.pageNumber + 1) * this.pageSize < this._dataSource.originalSampleCount) {
        this.pageNumber++;
        this._dataSource.loadOriginalSamples(this.filter, 'asc', this.pageNumber, this.pageSize);
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
