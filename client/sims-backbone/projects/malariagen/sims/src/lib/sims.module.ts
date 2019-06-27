import { NgModule, ModuleWithProviders, Optional, SkipSelf, Injectable, InjectionToken } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';


import { AllStudiesListComponent } from './all-studies-list/all-studies-list.component';

import { BrowserModule } from '@angular/platform-browser';
import { StudiesListComponent } from './studies-list/studies-list.component';
import { StudyEditComponent } from './study-edit/study-edit.component';
import { SimsAuthService, SIMS_AUTH_SERVICE } from './sims-auth.service';

import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { SimsResponseInterceptor, SIMS_AUTH_HTTP_CONFIG } from './auth/response.interceptor';
import { SimsModuleConfig } from './sims.module.config';

import { TaxonomyEditComponent } from './taxonomy-edit/taxonomy-edit.component';
import { MatAutocompleteModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatSelectModule, MatPaginatorModule, MatTableModule } from '@angular/material';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';
import { EventListComponent } from './event-list/event-list.component';
import { TaxaEventListComponent } from './taxa-event-list/taxa-event-list.component';
import { LocationEventListComponent } from './location-event-list/location-event-list.component';
import { EventSetEventListComponent } from './event-set-event-list/event-set-event-list.component';
import { SamplingEventDisplayPipe } from './sampling-event-display.pipe';
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';
import { EventSetEditDialogComponent } from './event-set-edit-dialog/event-set-edit-dialog.component';
import { DownloaderCsvComponent } from './downloader-csv/downloader-csv.component';
import { DownloaderJsonComponent } from './downloader-json/downloader-json.component';
import { EventSetEditComponent } from './event-set-edit/event-set-edit.component';
import { EventSetAddDialogComponent } from './event-set-add-dialog/event-set-add-dialog.component';
import { TaxaOsListComponent } from './taxa-os-list/taxa-os-list.component';
import { EventSetOsListComponent } from './event-set-os-list/event-set-os-list.component';
import { StudyOsListComponent } from './study-os-list/study-os-list.component';
import { OsListComponent } from './os-list/os-list.component';
import { DownloaderOsCsvComponent } from './downloader-os-csv/downloader-os-csv.component';
import { DownloaderOsJsonComponent } from './downloader-os-json/downloader-os-json.component';
import { OriginalSampleDisplayPipe } from './original-sample-display.pipe';
import { EventSetDsListComponent } from './event-set-ds-list/event-set-ds-list.component';
import { StudyDsListComponent } from './study-ds-list/study-ds-list.component';
import { TaxaDsListComponent } from './taxa-ds-list/taxa-ds-list.component';
import { DsListComponent } from './ds-list/ds-list.component';
import { DownloaderDsCsvComponent } from './downloader-ds-csv/downloader-ds-csv.component';
import { DownloaderDsJsonComponent } from './downloader-ds-json/downloader-ds-json.component';
import { DerivativeSampleDisplayPipe } from './derivative-sample-display.pipe';
import { LocationEditComponent } from './location-edit/location-edit.component';
import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { TaxaListComponent } from './taxa-list/taxa-list.component';
import { EventSetListComponent } from './event-set-list/event-set-list.component';
import { EventSearchComponent } from './event-search/event-search.component';
import { LocationsMapComponent } from './locations-map/locations-map.component';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { AgmCoreModule } from '@agm/core';
import { SampleOverviewComponent } from './sample-overview/sample-overview.component';

import { DsDetailComponent } from './ds-detail/ds-detail.component';
import { AttrTableComponent } from './attr-table/attr-table.component';
import { OsDetailComponent } from './os-detail/os-detail.component';
import { AdDetailComponent } from './ad-detail/ad-detail.component';
import { EventDetailComponent } from './event-detail/event-detail.component';
import { LocationViewComponent } from './location-view/location-view.component';
import { IndividualViewComponent } from './individual-view/individual-view.component';
import { ReportMissingLocationsComponent } from './report-missing-locations/report-missing-locations.component';
import { ReportMissingDetailedLocationsComponent } from './report-missing-detailed-locations/report-missing-detailed-locations.component';
import { ReportUncuratedLocationsComponent } from './report-uncurated-locations/report-uncurated-locations.component';
import { ReportMissingTaxaComponent } from './report-missing-taxa/report-missing-taxa.component';
import { ReportMultipleLocationGpsComponent } from './report-multiple-location-gps/report-multiple-location-gps.component';
import { ReportMultipleLocationNamesComponent } from './report-multiple-location-names/report-multiple-location-names.component';
import { OAuthModule } from 'angular-oauth2-oidc';

import { LAZY_MAPS_API_CONFIG } from '@agm/core';
import { CustomMapsConfig } from './CustomMapsConfig';
import { Configuration } from './typescript-angular-client/configuration';

const routes: Routes = [
  { path: 'study/:studyCode', component: StudyEditComponent },
  { path: 'study/events/:studyName', component: StudyEventListComponent },
  { path: 'taxa/events/:taxaId', component: TaxaEventListComponent },
  { path: 'location/events/:locationId', component: LocationEventListComponent },
  { path: 'eventSet/events/:eventSetId', component: EventSetEventListComponent },
  { path: 'eventSet/:eventSetId', component: EventSetEditComponent },
  { path: 'taxa/os/:taxaId', component: TaxaOsListComponent },
  { path: 'eventSet/os/:eventSetId', component: EventSetOsListComponent },
  { path: 'study/os/:studyName', component: StudyOsListComponent },
  { path: 'eventSet/ds/:eventSetId', component: EventSetDsListComponent },
  { path: 'study/ds/:studyName', component: StudyDsListComponent },
  { path: 'taxa/ds/:taxaId', component: TaxaDsListComponent },
  { path: 'location/:locationId', component: LocationEditComponent },


];

export const API_CONFIG = new InjectionToken<Configuration>('sims-api-config');

export let configFactory = (authService: SimsAuthService): Configuration => {
  return authService.getConfiguration();
};

export function getConfiguration(authService: SimsAuthService): Configuration {
  return authService.getConfiguration();
}

@NgModule({
  declarations: [
    AllStudiesListComponent,
    StudiesListComponent,
    TaxonomyEditComponent,
    StudyEditComponent,
    SamplingEventDisplayPipe,
    ErrorDialogComponent,
    EventSetEditDialogComponent,
    DownloaderCsvComponent,
    DownloaderJsonComponent,
    EventSetAddDialogComponent,
    EventSetEditComponent,
    EventSetEditDialogComponent,
    EventListComponent,
    StudyEventListComponent,
    TaxaEventListComponent,
    LocationEventListComponent,
    EventSetEventListComponent,
    DownloaderOsCsvComponent,
    DownloaderOsJsonComponent,
    OriginalSampleDisplayPipe,
    OsListComponent,
    EventSetOsListComponent,
    TaxaOsListComponent,
    StudyOsListComponent,
    DownloaderDsCsvComponent,
    DownloaderDsJsonComponent,
    DerivativeSampleDisplayPipe,
    DsListComponent,
    EventSetDsListComponent,
    StudyDsListComponent,
    TaxaDsListComponent,
    LocationsMapComponent,
    AllLocationsMapComponent,
    TaxaListComponent,
    EventSetListComponent,
    AttrTableComponent,
    AdDetailComponent,
    EventDetailComponent,
    OsDetailComponent,
    DsDetailComponent,
    LocationViewComponent,
    IndividualViewComponent,
    SampleOverviewComponent,
    EventSearchComponent,
    LocationEditComponent,
    ReportMissingLocationsComponent,
    ReportMissingDetailedLocationsComponent,
    ReportUncuratedLocationsComponent,
    ReportMissingTaxaComponent,
    ReportMultipleLocationGpsComponent,
    ReportMultipleLocationNamesComponent,
  ],
  imports: [
    RouterModule.forChild(routes),
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatFormFieldModule,
    MatAutocompleteModule,
    MatTableModule,
    MatPaginatorModule,
    FlexLayoutModule,
    LeafletModule,
    OAuthModule.forRoot(),
    AgmCoreModule.forRoot(),
  ],
  providers: [
    SimsAuthService,
    {
      provide: SIMS_AUTH_SERVICE,
      useClass: SimsAuthService
    },
    {
      provide: Configuration,
      useFactory: getConfiguration,
      deps: [SimsAuthService],
      multi: false
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: SimsResponseInterceptor,
      multi: true
    },
    {
      provide: LAZY_MAPS_API_CONFIG,
      useClass: CustomMapsConfig
    },
    {
      provide: SIMS_AUTH_HTTP_CONFIG,
      useClass: SimsModuleConfig
    }
  ],
  exports: [
    AllStudiesListComponent,
    StudiesListComponent,
    EventSetAddDialogComponent,
    AllLocationsMapComponent,
    TaxaListComponent,
    EventSetListComponent,
    EventSearchComponent,
    ReportMissingLocationsComponent,
    ReportMissingDetailedLocationsComponent,
    ReportUncuratedLocationsComponent,
    ReportMissingTaxaComponent,
    ReportMultipleLocationGpsComponent,
    ReportMultipleLocationNamesComponent
  ],
  entryComponents: [
    ErrorDialogComponent,
    EventSetEditDialogComponent,
    EventSetAddDialogComponent,
  ]
})
export class SimsModule {
  constructor(@Optional() @SkipSelf() parentModule: SimsModule) {
    if (parentModule) {
      throw new Error(
        'SimsModule is already loaded. Import it in the AppModule only');
    }
    //console.log('SimsModule Constructed');
  }

  static forRoot(config: SimsModuleConfig): ModuleWithProviders {
    //    console.log('SimsModule config');
    //    console.log(config);
    return {
      ngModule: SimsModule,
      providers: [
        { provide: SimsModuleConfig, useValue: config },
        { provide: SIMS_AUTH_HTTP_CONFIG, useValue: config }
      ]
    };
  }
}
