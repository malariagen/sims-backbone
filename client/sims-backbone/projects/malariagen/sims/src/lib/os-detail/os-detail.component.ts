import { Component, OnInit, Input } from '@angular/core';
import { OriginalSamples } from '../typescript-angular-client';

@Component({
  selector: 'sims-os-detail',
  templateUrl: './os-detail.component.html',
  styleUrls: ['./os-detail.component.scss']
})
export class OsDetailComponent implements OnInit {

  @Input()
  originalSamples: OriginalSamples;
  
  constructor() { }

  ngOnInit() {
  }

}
