import { Component, Input, Output, EventEmitter, Renderer } from '@angular/core';

import { DataSource, CollectionViewer } from '@angular/cdk/collections';
import { Observable } from 'rxjs/Observable';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
  selector: 'app-csv-downloader',
  templateUrl: './csv-downloader.component.html',
  styleUrls: ['./csv-downloader.component.css']
})
export class CsvDownloaderComponent implements CollectionViewer {
  viewChange = new BehaviorSubject<{ start: number, end: number }>({ start: 0, end: Number.MAX_VALUE });

  _fileName: string = 'data.csv';

  @Input() separator: string = '\t';

  @Input() downloaderName: string = 'Download CSV';
  @Input() headers: string[] = [];
  @Input() data: DataSource<any>;
  @Input()
  set fileName(fn: string) {
    this._fileName = fn;
  }
  @Output() onError = new EventEmitter<Error>();

  constructor(private renderer: Renderer) {

  }

  build() {


    let csvString = this.construct();

    this.buildDownloader(csvString);

  }

  private getDocumentBody(): any {
    return document.body;
  }

  private construct(): string {
    let tabText = '';
    let keys = null;
    
    this.data.connect(this).forEach(d => {

      d.forEach(k => {
        if (!keys) {
          keys = Object.keys(k);
          if (!this.headers.length) {
            this.headers = keys;
          }
          this.headers.forEach(h => {
            tabText += '"' + h + '"' + this.separator;
          });

          if (tabText.length > 0) {
            tabText = tabText.slice(0, -1);
            tabText += '\r\n';
          }
        }
        this.headers.forEach(field => {
          if (k.hasOwnProperty(field) && k[field] != null) {
            let text: string = k[field];
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


    });
    return tabText;
  }

  private buildDownloader(data) {

    var blob = new Blob([data], { type: 'text/csv;charset=utf-8' });
    var filename = this._fileName;
    
    if (window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveBlob(blob, filename);
    } else {

      let anchor = this.renderer.createElement(this.getDocumentBody(), 'a');
      this.renderer.setElementStyle(anchor, 'visibility', 'hidden');
      this.renderer.setElementAttribute(anchor, 'href', URL.createObjectURL(blob));
      //'data:text/csv;charset=utf-8,' + encodeURIComponent(data));
      this.renderer.setElementAttribute(anchor, 'target', '_blank');
      this.renderer.setElementAttribute(anchor, 'download', this._fileName);

      setTimeout(() => {
        this.renderer.invokeElementMethod(anchor, 'click');
        this.renderer.invokeElementMethod(anchor, 'remove');
      }, 5);
    }

  }

}
