import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { MatFormFieldModule } from '@angular/material';
import { MatInputModule } from '@angular/material';
import { MatTableModule } from '@angular/material';
import { MatButtonModule } from '@angular/material';

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
import { HttpModule } from '@angular/http';
import { OAuthModule } from 'angular-oauth2-oidc';

import { Configuration } from './typescript-angular-client/configuration';

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
    LocationEventListComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatTableModule,
    MatButtonModule,
    FlexLayoutModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LeafletModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyAXqsQD-9Gthal2ZU6cHIzNoggzMX3hi4o',
      libraries: ["places"]
    }),
    HttpModule,
    OAuthModule.forRoot()
  ],
  providers: [AuthService, {
    provide: Configuration,
    useFactory: getConfiguration,
    deps: [AuthService],
    multi: false
  }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
