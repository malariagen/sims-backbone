import { DataSource } from "@angular/cdk/table";
import { CollectionViewer } from "@angular/cdk/collections";
import { Observable } from "rxjs/Observable";
import { SamplingEvent, SamplingEvents, LocationMap } from "./typescript-angular-client";

import { SamplingEventsService } from "./sampling-events.service";
import { BehaviorSubject } from "rxjs/BehaviorSubject";
import { catchError, finalize } from "rxjs/operators";
import { of } from "rxjs/observable/of";

export class SamplingEventsSource implements DataSource<SamplingEvent> {

    locations: LocationMap;
    samplingEventCount: number;
    private samplingEventsSubject = new BehaviorSubject<SamplingEvent[]>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    public loading$ = this.loadingSubject.asObservable();

    constructor(private samplingEventsService: SamplingEventsService) { }

    connect(collectionViewer: CollectionViewer): Observable<SamplingEvent[]> {
        return this.samplingEventsSubject.asObservable();
    }

    disconnect(collectionViewer: CollectionViewer): void {
        this.samplingEventsSubject.complete();
        this.loadingSubject.complete();
    }

    loadEvents(filter = '',
        sortDirection = 'asc', pageIndex = 0, pageSize = 3) {

        this.loadingSubject.next(true);
        let ses: SamplingEvents;

        this.samplingEventsService.findEvents(filter, sortDirection,
            pageIndex, pageSize).pipe(
                catchError(() => of([])),
                finalize(() => this.loadingSubject.next(false))
            )
            .subscribe(result => {
                let samplingEvents = <SamplingEvents>result;
                this.samplingEventCount = samplingEvents.count;
                this.locations = { ...this.locations, ...samplingEvents.locations };

                this.samplingEventsSubject.next(samplingEvents.sampling_events);
            },
                error => { console.log(error); }
            );
    }
}
