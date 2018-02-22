import { Component, OnInit } from '@angular/core';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';

@Component({
  selector: 'app-event-search',
  providers: [SamplingEventService],
  templateUrl: './event-search.component.html',
  styleUrls: ['./event-search.component.scss']
})
export class EventSearchComponent implements OnInit {

  samplingEvents: SamplingEvents;

  identifier_type: string;
  identifier_value: string;

  constructor(private sampleService: SamplingEventService) { }

  ngOnInit() {
    this.identifier_type = 'oxford_id';
    //this.identifier_value = 'QS0167-C';
    this.search();
  }

  search() {
    if (this.identifier_type && this.identifier_value) {
      this.sampleService.downloadSamplingEventByIdentifier(this.identifier_type, this.identifier_value).subscribe(samplingEvents => {
        
          this.samplingEvents = samplingEvents;
        
      });
    }
  }
}
