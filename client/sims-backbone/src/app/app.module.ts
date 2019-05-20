import { BrowserModule } from '@angular/platform-browser';
import { NgModule, InjectionToken } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { MatFormFieldModule, MatSelectModule, MatPaginatorModule } from '@angular/material';
import { MatInputModule } from '@angular/material';
import { MatTableModule } from '@angular/material';
import { MatToolbarModule } from '@angular/material';
import { MatButtonModule } from '@angular/material';
import { MatAutocompleteModule } from '@angular/material';
import { MatDialogModule } from '@angular/material';
import { MatIconRegistry, MatIconModule } from '@angular/material';
import { MatMenuModule } from '@angular/material';

import { FlexLayoutModule } from '@angular/flex-layout';

import { AppRoutingModule } from './app-routing.module';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'hammerjs';

import { LeafletModule } from '@asymmetrik/ngx-leaflet';

import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { LocationsMapComponent } from './locations-map/locations-map.component';
import { LocationEditComponent } from './location-edit/location-edit.component';
import { EventListComponent } from './event-list/event-list.component';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';
import { LocationEventListComponent } from './location-event-list/location-event-list.component';

import { AuthService } from './auth.service';
import { OAuthModule } from 'angular-oauth2-oidc';

import { Configuration } from './typescript-angular-client/configuration';
import { StudiesListComponent } from './studies-list/studies-list.component';
import { StudyEditComponent } from './study-edit/study-edit.component';
import { TaxonomyEditComponent } from './taxonomy-edit/taxonomy-edit.component';
import { TaxaListComponent } from './taxa-list/taxa-list.component';
import { TaxaEventListComponent } from './taxa-event-list/taxa-event-list.component';
import { EventSetEventListComponent } from './event-set-event-list/event-set-event-list.component';
import { EventSetListComponent } from './event-set-list/event-set-list.component';
import { EventSetEditComponent } from './event-set-edit/event-set-edit.component';
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';
import { EventSetEditDialogComponent } from './event-set-edit-dialog/event-set-edit-dialog.component';
import { EventSetAddDialogComponent } from './event-set-add-dialog/event-set-add-dialog.component';

import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

import { EventSearchComponent } from './event-search/event-search.component';
import { EventDetailComponent } from './event-detail/event-detail.component';
import { LocationViewComponent } from './location-view/location-view.component';
import { AllStudiesListComponent } from './all-studies-list/all-studies-list.component';
import { ReportsComponent } from './reports/reports.component';
import { ReportMissingLocationsComponent } from './report-missing-locations/report-missing-locations.component';
import { ReportMissingDetailedLocationsComponent } from './report-missing-detailed-locations/report-missing-detailed-locations.component';
import { ReportUncuratedLocationsComponent } from './report-uncurated-locations/report-uncurated-locations.component';
import { ReportMissingTaxaComponent } from './report-missing-taxa/report-missing-taxa.component';
import { ReportMultipleLocationGpsComponent } from './report-multiple-location-gps/report-multiple-location-gps.component';
import { ReportMultipleLocationNamesComponent } from './report-multiple-location-names/report-multiple-location-names.component';
import { AttrTableComponent } from './attr-table/attr-table.component';
import { SamplingEventDisplayPipe } from './sampling-event-display.pipe';
import { DownloaderJsonComponent } from './downloader-json/downloader-json.component';
import { DownloaderCsvComponent } from './downloader-csv/downloader-csv.component';
import { SampleOverviewComponent } from './sample-overview/sample-overview.component';
import { OsListComponent } from './os-list/os-list.component';
import { OriginalSampleDisplayPipe } from './original-sample-display.pipe';
import { TaxaOsListComponent } from './taxa-os-list/taxa-os-list.component';
import { DownloaderOsCsvComponent } from './downloader-os-csv/downloader-os-csv.component';
import { DownloaderOsJsonComponent } from './downloader-os-json/downloader-os-json.component';
import { DsListComponent } from './ds-list/ds-list.component';
import { TaxaDsListComponent } from './taxa-ds-list/taxa-ds-list.component';
import { DownloaderDsCsvComponent } from './downloader-ds-csv/downloader-ds-csv.component';
import { DownloaderDsJsonComponent } from './downloader-ds-json/downloader-ds-json.component';
import { DerivativeSampleDisplayPipe } from './derivative-sample-display.pipe';
import { OsDetailComponent } from './os-detail/os-detail.component';
import { DsDetailComponent } from './ds-detail/ds-detail.component';
import { AdDetailComponent } from './ad-detail/ad-detail.component';
import { EventSetOsListComponent } from './event-set-os-list/event-set-os-list.component';
import { EventSetDsListComponent } from './event-set-ds-list/event-set-ds-list.component';
import { StudyOsListComponent } from './study-os-list/study-os-list.component';
import { StudyDsListComponent } from './study-ds-list/study-ds-list.component';
import { ResponseInterceptor } from './auth/response.interceptor';
import { IndividualViewComponent } from './individual-view/individual-view.component';

export function getConfiguration(authService: AuthService) {
  return authService.getConfiguration();
}

@NgModule({
  declarations: [
    AppComponent,
    AttrTableComponent,
    AllLocationsMapComponent,
    LocationsMapComponent,
    LocationEditComponent,
    EventListComponent,
    StudyEventListComponent,
    LocationEventListComponent,
    StudiesListComponent,
    StudyEditComponent,
    TaxonomyEditComponent,
    TaxaListComponent,
    TaxaEventListComponent,
    EventSetEventListComponent,
    EventSetListComponent,
    EventSetEditComponent,
    ErrorDialogComponent,
    EventSetEditDialogComponent,
    EventSetAddDialogComponent,
    EventSearchComponent,
    EventDetailComponent,
    LocationViewComponent,
    AllStudiesListComponent,
    ReportsComponent,
    ReportMissingLocationsComponent,
    ReportMissingDetailedLocationsComponent,
    ReportUncuratedLocationsComponent,
    ReportMissingTaxaComponent,
    ReportMultipleLocationGpsComponent,
    ReportMultipleLocationNamesComponent,
    SamplingEventDisplayPipe,
    DownloaderJsonComponent,
    DownloaderCsvComponent,
    SampleOverviewComponent,
    OsListComponent,
    OriginalSampleDisplayPipe,
    TaxaOsListComponent,
    DownloaderOsCsvComponent,
    DownloaderOsJsonComponent,
    DsListComponent,
    TaxaDsListComponent,
    DownloaderDsCsvComponent,
    DownloaderDsJsonComponent,
    DerivativeSampleDisplayPipe,
    OsDetailComponent,
    DsDetailComponent,
    AdDetailComponent,
    EventSetOsListComponent,
    EventSetDsListComponent,
    StudyOsListComponent,
    StudyDsListComponent,
    IndividualViewComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
    MatButtonModule,
    MatAutocompleteModule,
    MatDialogModule,
    MatIconModule,
    MatMenuModule,
    MatPaginatorModule,
    MatSelectModule,
    FlexLayoutModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LeafletModule,
    AgmCoreModule.forRoot({
      apiKey: process.env.GOOGLE_API_KEY,
      libraries: ["places"]
    }),
    OAuthModule.forRoot()
  ],
  providers: [
    AuthService,
    {
      provide: Configuration,
      useFactory: getConfiguration,
      deps: [AuthService],
      multi: false
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ResponseInterceptor,
      multi: true
    }
  ],
  entryComponents: [
    ErrorDialogComponent,
    EventSetEditDialogComponent,
    EventSetAddDialogComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
