import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { HttpClientModule, HttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';

import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';

import { AppRoutingModule } from './app-routing.module';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'hammerjs';

import { AngularEditorModule } from '@kolkov/angular-editor';
import { AppComponent } from './app.component';

import { environment } from '../environments/environment';

import { ReportsComponent } from './reports/reports.component';

import { SimsModule } from '@malariagen/sims';
import { OAuthStorage } from 'angular-oauth2-oidc';
import { AlfStudyDetailComponent } from './alf-study-detail/alf-study-detail.component';
import { AlfResponseInterceptor } from './alf-interceptor/response.interceptor';
import { ReactiveFormsModule } from '@angular/forms';

export function storageFactory(): OAuthStorage {
  return localStorage
}

@NgModule({
  declarations: [
    AppComponent,
    ReportsComponent,
    AlfStudyDetailComponent
  ],
  imports: [
    BrowserModule,
    MatToolbarModule,
    MatIconModule,
    MatMenuModule,
    MatDialogModule,
    MatButtonModule,
    ReactiveFormsModule,
    MatInputModule,
    MatSelectModule,
    MatCheckboxModule,
    MatFormFieldModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    SimsModule.forRoot({
      apiLocation: environment.apiLocation,
      mapsApiKey: environment.mapsApiKey,
      OAuthConfig: {
        'clientId': environment.clientId,
        'redirectUri': environment.redirectUri,
        'postLogoutRedirectUri': environment.postLogoutRedirectUri,
        'loginUrl': environment.loginUrl,
        'scope': environment.scope,
        'resource': '',
        'rngUrl': '',
        'oidc': false,
        'requestAccessToken': true,
        'options': null,
        'clearHashAfterLogin': true,
        'tokenEndpoint': environment.tokenEndpoint,
        'responseType': 'token',
        'showDebugInformation': environment.showDebugInformation,
        'dummyClientSecret': environment.dummyClientSecret
      }
    }),
    AngularEditorModule
  ],
  providers: [
    // { provide: OAuthModuleConfig, useValue: authModuleConfig },
    { provide: OAuthStorage, useFactory: storageFactory },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AlfResponseInterceptor,
      multi: true
    },


  ],
  entryComponents: [
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
