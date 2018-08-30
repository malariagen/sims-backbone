import { DataSource } from "@angular/cdk/table";
import { CollectionViewer } from "@angular/cdk/collections";
import { Observable } from "rxjs/Observable";
import { DerivativeSample, DerivativeSamples } from "./typescript-angular-client";

import { BehaviorSubject } from "rxjs/BehaviorSubject";
import { catchError, finalize } from "rxjs/operators";
import { of } from "rxjs/observable/of";
import { DerivativeSamplesService } from "./derivative-samples.service";

export class DerivativeSamplesSource implements DataSource<DerivativeSample> {

    derivativeSampleCount: number;
    attrTypes: Array<string>;

    private derivativeSamplesSubject = new BehaviorSubject<DerivativeSample[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    public loading$ = this.loadingSubject.asObservable();

    constructor(private derivativeSamplesService: DerivativeSamplesService) { }

    connect(collectionViewer: CollectionViewer): Observable<DerivativeSample[]> {
        return this.derivativeSamplesSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.derivativeSamplesSubject.complete();
        this.loadingSubject.complete();
    }

    loadDerivativeSamples(filter = '',
        sortDirection = 'asc', pageIndex = 0, pageSize = 3) {

        this.loadingSubject.next(true);
        let ses: DerivativeSamples;

        this.derivativeSamplesService.findDerivativeSamples(filter, sortDirection,
            pageIndex, pageSize).pipe(
                catchError(() => of([])),
                finalize(() => this.loadingSubject.next(false))
            )
            .subscribe(result => {
                let derivativeSamples = <DerivativeSamples>result;
                this.derivativeSampleCount = derivativeSamples.count;
                this.attrTypes = derivativeSamples.attr_types;
                
                //this.locations = { ...this.locations, ...originalSamples.locations };

                this.derivativeSamplesSubject.next(derivativeSamples.derivative_samples);
            },
                error => { console.log(error); }
            );
    }
}
