import { Component, OnInit } from '@angular/core';
import { SamplingEventService } from '../typescript-angular-client/api/samplingEvent.service';
import { MetadataService } from '../typescript-angular-client/api/metadata.service';

import { SamplingEvents } from '../typescript-angular-client/model/samplingEvents';
import { DerivativeSampleService, AssayDataService, AssayData, OriginalSampleService, OriginalSamples, DerivativeSamples } from '../typescript-angular-client';


@Component({
  selector: 'app-event-search',
  providers: [
    SamplingEventService, MetadataService,
    OriginalSampleService, DerivativeSampleService, AssayDataService],
  templateUrl: './event-search.component.html',
  styleUrls: ['./event-search.component.scss']
})
export class EventSearchComponent implements OnInit {

  originalSamples: OriginalSamples;
  samplingEvents: SamplingEvents;
  derivativeSamples: DerivativeSamples;
  assayData: AssayData;
  attrType: string;
  attrValue: string;

  options: string[];

  constructor(private sampleService: SamplingEventService, private metadataService: MetadataService,
    private originalSampleService: OriginalSampleService,
    private derivativeSampleService: DerivativeSampleService, private assayDataService: AssayDataService) { }

  ngOnInit() {

    this.metadataService.getAttrTypes().subscribe(attrTypes => {
      this.options = attrTypes;
    });
    this.warmUp();

    this.attrType = 'oxfordId';
    //this.attrValue = 'QS0167-C';
    this.search();
    
  }

  warmUp() {
    this.sampleService.downloadSamplingEventsByOsAttr('', '').subscribe();
    this.originalSampleService.downloadOriginalSamplesByAttr('', '').subscribe();
    this.derivativeSampleService.downloadDerivativeSamplesByOsAttr('', '').subscribe();
    this.assayDataService.downloadAssayDataByOsAttr('', '').subscribe();
  }

  search() {
    if (this.attrType && this.attrValue) {
      this.sampleService.downloadSamplingEventsByOsAttr(this.attrType, this.attrValue).subscribe(samplingEvents => {
        this.samplingEvents = samplingEvents;
      });
      this.originalSampleService.downloadOriginalSamplesByAttr(this.attrType, this.attrValue).subscribe(originalSamples => {
        this.originalSamples = originalSamples;

        this.derivativeSampleService.downloadDerivativeSamplesByOsAttr(this.attrType, this.attrValue).subscribe(derivativeSamples => {
          this.derivativeSamples = derivativeSamples;

          this.assayDataService.downloadAssayDataByOsAttr(this.attrType, this.attrValue).subscribe(assayData => {
            this.assayData = assayData;
          });
        });
      });

    }
  }
}
