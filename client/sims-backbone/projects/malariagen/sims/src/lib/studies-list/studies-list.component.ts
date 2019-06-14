import { Component, Input } from '@angular/core';
import { Studies } from '../typescript-angular-client';

@Component({
  selector: 'sims-studies-list',
  templateUrl: './studies-list.component.html',
  styleUrls: ['./studies-list.component.scss']
})
export class StudiesListComponent {

  constructor() { }
  @Input()
  studies: Studies;
}
