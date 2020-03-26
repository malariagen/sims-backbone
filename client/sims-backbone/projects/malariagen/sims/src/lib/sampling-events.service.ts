import { Injectable } from '@angular/core';
import { SamplingEvents } from './typescript-angular-client';
import { Observable } from 'rxjs/Observable';
import { SamplingEventService } from './typescript-angular-client/api/samplingEvent.service';

@Injectable({
  providedIn: 'root'
})
export class SamplingEventsService {

  constructor(private sampleService: SamplingEventService) { }

  findEvents(filter = '', sortOrder = 'asc',
    pageNumber = 0, pageSize = 3): Observable<SamplingEvents> {

    return this.sampleService.downloadSamplingEvents(filter, 'str', pageNumber * pageSize, pageSize);

  }
}
