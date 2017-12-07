import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { MatFormFieldModule } from '@angular/material';
import { MatInputModule } from '@angular/material';
import { MatTableModule } from '@angular/material';
import { MatToolbarModule } from '@angular/material';
import { MatButtonModule } from '@angular/material';
import { MatAutocompleteModule } from '@angular/material';
import { MatDialogModule } from '@angular/material';

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
import { CsvDownloaderComponent } from './csv-downloader/csv-downloader.component';
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

export function getConfiguration(authService: AuthService) {
  return authService.getConfiguration();
}


@NgModule({
  declarations: [
    AppComponent,
    AllLocationsMapComponent,
    LocationsMapComponent,
    LocationEditComponent,
    EventListComponent,
    StudyEventListComponent,
    CsvDownloaderComponent,
    LocationEventListComponent,
    StudiesListComponent,
    StudyEditComponent,
    TaxonomyEditComponent,
    TaxaListComponent,
    TaxaEventListComponent,
    EventSetEventListComponent,
    EventSetListComponent,
    EventSetEditComponent,
    ErrorDialogComponent
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
    FlexLayoutModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LeafletModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyAXqsQD-9Gthal2ZU6cHIzNoggzMX3hi4o',
      libraries: ["places"]
    }),
    OAuthModule.forRoot()
  ],
  providers: [AuthService, {
    provide: Configuration,
    useFactory: getConfiguration,
    deps: [AuthService],
    multi: false
  }
  ],
  entryComponents: [
    ErrorDialogComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
