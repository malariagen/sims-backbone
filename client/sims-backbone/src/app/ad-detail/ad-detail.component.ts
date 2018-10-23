import { Component, OnInit, Input } from '@angular/core';
import { AssayData } from '../typescript-angular-client';

@Component({
  selector: 'app-ad-detail',
  templateUrl: './ad-detail.component.html',
  styleUrls: ['./ad-detail.component.scss']
})
export class AdDetailComponent implements OnInit {

  @Input()
  assayData: AssayData;
  
  constructor() { }

  ngOnInit() {
  }

}
