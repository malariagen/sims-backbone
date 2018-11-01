import { Component, OnInit, AfterViewInit, ViewChild, ChangeDetectorRef, Input, ChangeDetectionStrategy } from '@angular/core';
import { MatPaginator, MatTable } from '@angular/material';
import { DerivativeSample, DerivativeSampleService } from '../typescript-angular-client';
import { Observable } from 'rxjs';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSamplesSource } from '../derivative-sample.datasource';
import { tap } from 'rxjs/operators';

@Component({
  selector: 'app-ds-list',
  templateUrl: './ds-list.component.html',
  styleUrls: ['./ds-list.component.scss'],
  providers: [DerivativeSamplesService, DerivativeSampleService],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class DsListComponent implements OnInit, AfterViewInit {

  _dataSource: DerivativeSamplesSource;

  displayedColumns = [];

  _studyName: string;
  _eventSetName: string;

  @Input()
  filter: string;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatTable) table;

  selectedEvents = new Set<string>();

  @Input()
  downloadFileName: string = 'data.csv';

  @Input()
  jsonDownloadFileName: string = 'data.json';

  constructor(private changeDetector: ChangeDetectorRef, private derivativeSamplesService: DerivativeSamplesService) { }

  ngOnInit(): void {

    this._dataSource = new DerivativeSamplesSource(this.derivativeSamplesService);

    //Recalcuate the column headers when the data changes
    let obs: Observable<DerivativeSample[]> = this._dataSource.connect(this.table);

    obs.subscribe({
      next: sevents => this.defineColumnHeaders(sevents),
      error(msg) {
        console.log(msg);
      },
      complete() {
        console.log('complete');
      }
    });

    this._dataSource.loadDerivativeSamples(this.filter, 'asc', 0, 50);

  }

  ngAfterViewInit() {

    if (this.paginator) {
      this.paginator.page
        .pipe(
          tap(() => this.loadOriginalSamplesPage())
        )
        .subscribe();
    }

  }

  @Input()
  set studyName(studyName: string) {
    this._studyName = studyName;
    this.downloadFileName = studyName + '_sampling_events.csv';
    this.jsonDownloadFileName = studyName + '_sampling_events.json';
  }

  loadOriginalSamplesPage() {
    this._dataSource.loadDerivativeSamples(this.filter,
      'asc',
      this.paginator.pageIndex,
      this.paginator.pageSize
    );

  }

  defineColumnHeaders(sampling_events) {

    if (sampling_events == undefined) {
      return;
    }

    let columnsForDisplay = ['derivative_sample_id', 'dna_prep', 'partner_species'];
    columnsForDisplay = columnsForDisplay.concat(this._dataSource.attrTypes);
    columnsForDisplay = columnsForDisplay.concat(['original_sample_id']);

    if (columnsForDisplay != this.displayedColumns) {
      this.displayedColumns = columnsForDisplay;
      this.changeDetector.markForCheck();
    }

  }


}
