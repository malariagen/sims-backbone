import { Injectable } from '@angular/core';
import { SamplingEvents, SamplingEventService } from './typescript-angular-client';
import { Observable } from 'rxjs/Observable';

@Injectable({
  providedIn: 'root'
})
export class SamplingEventsService {

  constructor(private sampleService: SamplingEventService) { }

  findEvents(filter = '', sortOrder = 'asc',
    pageNumber = 0, pageSize = 3): Observable<SamplingEvents> {

    return this.sampleService.downloadSamplingEvents(filter, pageNumber * pageSize, pageSize);

  }
}
