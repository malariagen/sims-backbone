import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { AllStudiesListComponent } from './all-studies-list/all-studies-list.component';
import { LocationEditComponent } from './location-edit/location-edit.component';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';
import { TaxaEventListComponent } from './taxa-event-list/taxa-event-list.component';
import { EventSetEventListComponent } from './event-set-event-list/event-set-event-list.component';
import { LocationEventListComponent } from './location-event-list/location-event-list.component';
import { TaxaListComponent } from './taxa-list/taxa-list.component';
import { EventSetListComponent } from './event-set-list/event-set-list.component';
import { StudyEditComponent } from './study-edit/study-edit.component';
import { EventSetEditComponent } from './event-set-edit/event-set-edit.component';
import { EventSearchComponent } from './event-search/event-search.component';

import { ReportsComponent } from './reports/reports.component';
import { ReportMissingDetailedLocationsComponent } from './report-missing-detailed-locations/report-missing-detailed-locations.component';
import { ReportMissingLocationsComponent } from './report-missing-locations/report-missing-locations.component';
import { ReportMissingTaxaComponent } from './report-missing-taxa/report-missing-taxa.component';
import { ReportUncuratedLocationsComponent } from './report-uncurated-locations/report-uncurated-locations.component';
import { ReportMultipleLocationGpsComponent } from './report-multiple-location-gps/report-multiple-location-gps.component';
import { ReportMultipleLocationNamesComponent } from './report-multiple-location-names/report-multiple-location-names.component';
import { TaxaOsListComponent } from './taxa-os-list/taxa-os-list.component';

const routes: Routes = [
  { path: '', redirectTo: '/studies', pathMatch: 'full' },
  { path: 'full-map', component: AllLocationsMapComponent },
  { path: 'location/:locationId', component: LocationEditComponent },
  { path: 'study/events/:studyName', component: StudyEventListComponent },
  { path: 'location/events/:locationId', component: LocationEventListComponent },
  { path: 'studies', component: AllStudiesListComponent },
  { path: 'study/:studyCode', component: StudyEditComponent },
  { path: 'taxa', component: TaxaListComponent },
  { path: 'taxa/events/:taxaId', component: TaxaEventListComponent },
  { path: 'taxa/os/:taxaId', component: TaxaOsListComponent },
  { path: 'eventSets', component: EventSetListComponent },
  { path: 'eventSet/events/:eventSetId', component: EventSetEventListComponent },
  { path: 'eventSet/:eventSetId', component: EventSetEditComponent },
  { path: 'search', component: EventSearchComponent },
  {
    path: 'reports', component: ReportsComponent,
    children: [
      { path: 'missingDetailedLocations', component: ReportMissingDetailedLocationsComponent },
      { path: 'missingLocations', component: ReportMissingLocationsComponent },
      { path: 'missingTaxa', component: ReportMissingTaxaComponent },
      { path: 'uncuratedLocations', component: ReportUncuratedLocationsComponent },
      { path: 'multipleLocationGPS', component: ReportMultipleLocationGpsComponent },
      { path: 'multipleLocationNames', component: ReportMultipleLocationNamesComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
