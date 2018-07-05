import { Component, OnInit } from '@angular/core';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';

import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { DerivedSampleService, AssayDataService, AssayData, OriginalSampleService, OriginalSamples, DerivedSamples } from '../typescript-angular-client';


@Component({
  selector: 'app-event-search',
  providers: [
    SamplingEventService, MetadataService,
    OriginalSampleService, DerivedSampleService, AssayDataService],
  templateUrl: './event-search.component.html',
  styleUrls: ['./event-search.component.scss']
})
export class EventSearchComponent implements OnInit {

  originalSamples: OriginalSamples;
  samplingEvents: SamplingEvents;
  derivedSamples: DerivedSamples;
  assayData: AssayData;
  attr_type: string;
  attr_value: string;

  searches: number = 0;

  options: string[];

  constructor(private sampleService: SamplingEventService, private metadataService: MetadataService,
    private originalSampleService: OriginalSampleService,
    private derivedSampleService: DerivedSampleService, private assayDataService: AssayDataService) { }

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
        this.originalSampleService.downloadOriginalSamplesByAttr(this.attr_type, this.attr_value).subscribe(originalSamples => {
          this.originalSamples = originalSamples;

          this.derivedSampleService.downloadDerivedSamplesByOsAttr(this.attr_type, this.attr_value).subscribe(derivedSamples => {
            this.derivedSamples = derivedSamples;

            this.assayDataService.downloadAssayDataByOsAttr(this.attr_type, this.attr_value).subscribe(assayData => {
              this.assayData = assayData;
              this.searches++;
            });

          });
        });
      });

    }
  }
}
