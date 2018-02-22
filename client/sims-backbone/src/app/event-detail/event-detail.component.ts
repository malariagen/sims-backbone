import { Component, OnInit, Input } from '@angular/core';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';


@Component({
  selector: 'app-event-detail',
  templateUrl: './event-detail.component.html',
  styleUrls: ['./event-detail.component.scss']
})
export class EventDetailComponent implements OnInit {

  _samplingEvents: SamplingEvents;


 

  constructor() { }

  ngOnInit() {
  }

  @Input()
  set samplingEvents(samplingEvents) {
    if (samplingEvents) {
      this._samplingEvents = samplingEvents;
      console.log(samplingEvents);
    }
  }
}
