import { Component, Input } from '@angular/core';
import { MatTableDataSource } from '@angular/material';
import { Attr } from '../typescript-angular-client/model/attr';

import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'sims-attr-table',
  templateUrl: './attr-table.component.html',
  styleUrls: ['./attr-table.component.scss']
})
export class AttrTableComponent {

  attrColumns = ['attr_source', 'attr_type', 'attr_value'];

  dataSource: MatTableDataSource<Attr[]>;

  public studyEvents = '/study/events';

  constructor() { }

  @Input()
  set attrs(attrs) {
    if (attrs) {
      this.dataSource = new MatTableDataSource(attrs);
    }
  }

  @Input()
  set studies(studies) {
    if (studies === 'true') {
      this.attrColumns.push('study_name');
    }
  }
}
