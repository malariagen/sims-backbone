import { Component, OnInit, Input } from '@angular/core';
import { DerivativeSamples } from '../typescript-angular-client';

@Component({
  selector: 'app-ds-detail',
  templateUrl: './ds-detail.component.html',
  styleUrls: ['./ds-detail.component.scss']
})
export class DsDetailComponent implements OnInit {

  @Input()
  derivativeSamples: DerivativeSamples;
  
  constructor() { }

  ngOnInit() {
  }

}
