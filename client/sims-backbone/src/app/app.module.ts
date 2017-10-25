import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { MatFormFieldModule } from '@angular/material';
import { MatInputModule } from '@angular/material';

import { AppRoutingModule }     from './app-routing.module';

import { FlexLayoutModule } from '@angular/flex-layout';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import 'hammerjs';

import { LeafletModule } from '@asymmetrik/ngx-leaflet';

import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { LocationsMapComponent } from './locations-map/locations-map.component';
import { LocationEditComponent } from './location-edit/location-edit.component';

@NgModule({
  declarations: [
    AppComponent,
    AllLocationsMapComponent,
    LocationsMapComponent,
    LocationEditComponent
  ],
  imports: [
  BrowserModule,
  FlexLayoutModule,
  FormsModule,
  MatFormFieldModule,
  MatInputModule,
  ReactiveFormsModule,
  HttpModule,
  AppRoutingModule,
  BrowserAnimationsModule,
  LeafletModule,
  AgmCoreModule.forRoot({
  apiKey: 'AIzaSyAXqsQD-9Gthal2ZU6cHIzNoggzMX3hi4o',
  libraries: [ "places" ]
            })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
