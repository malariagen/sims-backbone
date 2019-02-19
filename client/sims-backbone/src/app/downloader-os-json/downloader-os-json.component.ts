import { Component, OnInit, Input } from '@angular/core';
import { OriginalSamplesSource } from '../original-sample.datasource';
import { BehaviorSubject, Observable } from 'rxjs';
import { OriginalSampleDisplayPipe } from '../original-sample-display.pipe';
import { OriginalSamplesService } from '../original-samples.service';
import { OriginalSample, OriginalSamples, OriginalSampleService } from '../typescript-angular-client';
import { CollectionViewer } from '@angular/cdk/collections';

import * as FileSaver from 'file-saver';

@Component({
  selector: 'app-downloader-os-json',
  templateUrl: './downloader-os-json.component.html',
  styleUrls: ['./downloader-os-json.component.scss'],
  providers: [OriginalSamplesService, OriginalSampleService, OriginalSampleDisplayPipe],
})
export class DownloaderOsJsonComponent implements CollectionViewer {

  originalSamples: OriginalSamples;
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
  downloaderName: string = 'Download JSON';
  @Input()
  headers: string[] = [];

  constructor(private displayPipe: OriginalSampleDisplayPipe, private originalSamplesService: OriginalSamplesService) {

    this._dataSource = new OriginalSamplesSource(this.originalSamplesService);

    let obs: Observable<OriginalSample[]> = this._dataSource.connect(this);


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

    this._dataSource.loadOriginalSamples(this.filter, 'asc', this.pageNumber, this.pageSize);

  }

  extractEvents(d: Array<OriginalSample>) {

    if (d.length == 0) {
      return;
    }

    if (this.pageNumber == 0) {
      this.originalSamples = <OriginalSamples>{};
      this.originalSamples.originalSamples = [];
    }

    this.originalSamples.originalSamples = this.originalSamples.originalSamples.concat(d);


    if ((this.pageNumber + 1) * this.pageSize < this._dataSource.originalSampleCount) {
      this.pageNumber++;
      this._dataSource.loadOriginalSamples(this.filter, 'asc', this.pageNumber, this.pageSize);
    } else {
      this.originalSamples.attrTypes = this._dataSource.attrTypes;
      this.originalSamples.count = this._dataSource.originalSampleCount;
      this.buildDownloader(JSON.stringify(this.originalSamples));
    }

  }
  private buildDownloader(data) {

    var blob = new Blob([data], { type: 'application/json;charset=utf-8' });

    FileSaver.saveAs(blob, this.fileName);

  }

}
