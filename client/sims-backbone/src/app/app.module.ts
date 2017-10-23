import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppRoutingModule }     from './app-routing.module';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import 'hammerjs';

import { LeafletModule } from '@asymmetrik/ngx-leaflet';


import { AppComponent } from './app.component';
import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { LocationsMapComponent } from './locations-map/locations-map.component';

@NgModule({
  declarations: [
    AppComponent,
    AllLocationsMapComponent,
    LocationsMapComponent
  ],
  imports: [
  BrowserModule,
  FormsModule,
  ReactiveFormsModule,
  HttpModule,
  AppRoutingModule,
  BrowserAnimationsModule,
  LeafletModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
