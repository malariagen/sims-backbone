import { Injectable } from '@angular/core';
import { DerivativeSamples, DerivativeSampleService } from './typescript-angular-client';
import { Observable } from 'rxjs';

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
