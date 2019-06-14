import { Component, OnInit, Input } from '@angular/core';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSampleService, DerivativeSample } from '../typescript-angular-client';
import { DerivativeSampleDisplayPipe } from '../derivative-sample-display.pipe';
import { CollectionViewer } from '@angular/cdk/collections';
import { BehaviorSubject, Observable } from 'rxjs';
import { DerivativeSamplesSource } from '../derivative-sample.datasource';

import * as FileSaver from 'file-saver';

@Component({
  selector: 'sims-downloader-ds-csv',
  templateUrl: './downloader-ds-csv.component.html',
  styleUrls: ['./downloader-ds-csv.component.scss'],
  providers: [DerivativeSamplesService, DerivativeSampleService, DerivativeSampleDisplayPipe],

})
export class DownloaderDsCsvComponent implements CollectionViewer {

  header: boolean = false;
  separator: string = '\t';
  csvString: string = '';
  pageSize: number = 1000;
  pageNumber: number = 0;

  _dataSource: DerivativeSamplesSource;
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  @Input()
  fileName: string = 'data.csv';
  @Input()
  filter: string;
  @Input()
  downloaderName: string = 'Download CSV';
  @Input()
  headers: string[] = [];

  constructor(private displayPipe: DerivativeSampleDisplayPipe, private derivativeSamplesService: DerivativeSamplesService) {

    this._dataSource = new DerivativeSamplesSource(this.derivativeSamplesService);

    let obs: Observable<DerivativeSample[]> = this._dataSource.connect(this);


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

    this._dataSource.loadDerivativeSamples(this.filter, 'asc', this.pageNumber, this.pageSize);


  }

  extractEventsToString(d: Array<DerivativeSample>) {

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

        let text: string = this.displayPipe.transform(k, field, null, this._dataSource.originalSamples);
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
      if ((this.pageNumber + 1) * this.pageSize < this._dataSource.derivativeSampleCount) {
        this.pageNumber++;
        this._dataSource.loadDerivativeSamples(this.filter, 'asc', this.pageNumber, this.pageSize);
      } else {
        this.buildDownloader(this.csvString);
        this.header = false;
        this.csvString = '';
      }
    }
  }
  private buildDownloader(data) {

    const blob = new Blob([data], { type: 'text/csv;charset=utf-8' });

    FileSaver.saveAs(blob, this.fileName);

  }
}
