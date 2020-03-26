import { Injectable } from '@angular/core';
import { OriginalSamples } from './typescript-angular-client';
import { Observable } from 'rxjs';
import { OriginalSampleService } from './typescript-angular-client/api/originalSample.service';

@Injectable({
  providedIn: 'root'
})
export class OriginalSamplesService {

  constructor(private sampleService: OriginalSampleService) { }

  findOriginalSamples(filter = '', sortOrder = 'asc',
    pageNumber = 0, pageSize = 3): Observable<OriginalSamples> {

    return this.sampleService.downloadOriginalSamples(filter, 'str', pageNumber * pageSize, pageSize);

  }
}
