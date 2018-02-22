import { Component, Input } from '@angular/core';
import { MatTableDataSource } from '@angular/material';
import { Identifier } from '../typescript-angular-client/model/identifier';

import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-identifier-table',
  templateUrl: './identifier-table.component.html',
  styleUrls: ['./identifier-table.component.scss']
})
export class IdentifierTableComponent {

  identifierColumns = ['identifier_source', 'identifier_type', 'identifier_value'];

  dataSource: MatTableDataSource<Identifier[]>;

  public studyEvents: string = '/study/events';

  constructor() { }

  @Input()
  set identifiers(identifiers) {
    if (identifiers) {
      this.dataSource = new MatTableDataSource(identifiers);
    }
  }

  @Input()
  set studies(studies) {
    if (studies == 'true') {
      this.identifierColumns.push('study_name');
    }
  }
}
