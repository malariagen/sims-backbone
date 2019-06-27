import { Injectable } from '@angular/core';
import { DerivativeSamples } from './typescript-angular-client';
import { Observable } from 'rxjs';
import { DerivativeSampleService } from './typescript-angular-client/api/derivativeSample.service';

@Injectable({
  providedIn: 'root'
})
export class DerivativeSamplesService {

  constructor(private sampleService: DerivativeSampleService) { }

  findDerivativeSamples(filter = '', sortOrder = 'asc',
    pageNumber = 0, pageSize = 3): Observable<DerivativeSamples> {

    return this.sampleService.downloadDerivativeSamples(filter, pageNumber * pageSize, pageSize);

  }
}
