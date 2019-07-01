import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { HttpClientModule, HTTP_INTERCEPTORS, HttpClient } from '@angular/common/http';

import { MatToolbarModule, MatDialogModule, MatButtonModule } from '@angular/material';
import { MatIconModule } from '@angular/material';
import { MatMenuModule } from '@angular/material';

import { AppRoutingModule } from './app-routing.module';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import 'hammerjs';

import { AppComponent } from './app.component';

import { environment } from '../environments/environment';

import { ReportsComponent } from './reports/reports.component';

import { SimsModule } from '@malariagen/sims';
import { AlfResponseInterceptor } from './alf-interceptor/response.interceptor';
import { AlfStudyDetailComponent } from './alf-study-detail/alf-study-detail.component';

import { CoreModule, TRANSLATION_PROVIDER } from '@alfresco/adf-core';
import { ContentModule } from '@alfresco/adf-content-services';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';

// AoT requires an exported function for factories
export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http);
}

@NgModule({
  declarations: [
    AppComponent,
    ReportsComponent,
    AlfStudyDetailComponent,
  ],
  imports: [
    BrowserModule,
    MatToolbarModule,
    MatIconModule,
    MatMenuModule,
    MatDialogModule,
    MatButtonModule,
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
        'responseType': 'code',
        'showDebugInformation': environment.showDebugInformation,
        'dummyClientSecret': environment.dummyClientSecret,

      }
    }),
    CoreModule.forRoot(),
    ContentModule.forRoot(),
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AlfResponseInterceptor,
      multi: true
    },
    {
      provide: TRANSLATION_PROVIDER,
      multi: true,
      useValue: {
        name: 'sims-backbone',
        source: 'assets'
      }
    }
  ],
  entryComponents: [
  ],
  bootstrap: [
    AppComponent
  ]
})
export class AppModule { }
