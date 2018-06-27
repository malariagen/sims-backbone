import { Component, OnInit } from '@angular/core';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';

import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';

@Component({
  selector: 'app-event-search',
  providers: [SamplingEventService, MetadataService],
  templateUrl: './event-search.component.html',
  styleUrls: ['./event-search.component.scss']
})
export class EventSearchComponent implements OnInit {

  samplingEvents: SamplingEvents;

  attr_type: string;
  attr_value: string;

  options: string[];

  constructor(private sampleService: SamplingEventService, private metadataService: MetadataService) { }

  ngOnInit() {

    this.metadataService.getAttrTypes().subscribe(attr_types => {
      this.options = attr_types;
    });
    
    this.attr_type = 'oxford_id';
    //this.attr_value = 'QS0167-C';
    this.search();
  }

  search() {
    if (this.attr_type && this.attr_value) {
      this.sampleService.downloadSamplingEventsByOsAttr(this.attr_type, this.attr_value).subscribe(samplingEvents => {
        
          this.samplingEvents = samplingEvents;
        
      });
    }
  }
}
