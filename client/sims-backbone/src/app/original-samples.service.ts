import { Injectable, Component } from '@angular/core';
import { OriginalSampleService, OriginalSamples } from './typescript-angular-client';
import { Observable } from 'rxjs';

@Component({
  providers: [OriginalSampleService]
})
@Injectable({
  providedIn: 'root'
})
export class OriginalSamplesService {

  constructor(private sampleService: OriginalSampleService) { }

  findOriginalSamples(filter = '', sortOrder = 'asc',
    pageNumber = 0, pageSize = 3): Observable<OriginalSamples> {

    return this.sampleService.downloadOriginalSamples(filter, pageNumber * pageSize, pageSize);

  }
}
