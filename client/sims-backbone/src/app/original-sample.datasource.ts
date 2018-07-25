import { DataSource } from "@angular/cdk/table";
import { CollectionViewer } from "@angular/cdk/collections";
import { Observable } from "rxjs/Observable";
import { OriginalSample, OriginalSamples, LocationMap } from "./typescript-angular-client";

import { BehaviorSubject } from "rxjs/BehaviorSubject";
import { catchError, finalize } from "rxjs/operators";
import { of } from "rxjs/observable/of";
import { OriginalSamplesService } from "./original-samples.service";

export class OriginalSamplesSource implements DataSource<OriginalSample> {

    locations: LocationMap;
    originalSampleCount: number;
    attrTypes: Array<string>;

    private originalSamplesSubject = new BehaviorSubject<OriginalSample[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    public loading$ = this.loadingSubject.asObservable();

    constructor(private originalSamplesService: OriginalSamplesService) { }

    connect(collectionViewer: CollectionViewer): Observable<OriginalSample[]> {
        return this.originalSamplesSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.originalSamplesSubject.complete();
        this.loadingSubject.complete();
    }

    loadOriginalSamples(filter = '',
        sortDirection = 'asc', pageIndex = 0, pageSize = 3) {

        this.loadingSubject.next(true);
        let ses: OriginalSamples;

        this.originalSamplesService.findOriginalSamples(filter, sortDirection,
            pageIndex, pageSize).pipe(
                catchError(() => of([])),
                finalize(() => this.loadingSubject.next(false))
            )
            .subscribe(result => {
                let originalSamples = <OriginalSamples>result;
                this.originalSampleCount = originalSamples.count;
                this.attrTypes = originalSamples.attr_types;
                
                //this.locations = { ...this.locations, ...originalSamples.locations };

                this.originalSamplesSubject.next(originalSamples.original_samples);
            },
                error => { console.log(error); }
            );
    }
}
