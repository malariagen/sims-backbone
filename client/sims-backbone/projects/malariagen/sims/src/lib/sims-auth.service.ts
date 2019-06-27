import { Injectable, Optional, Inject, InjectionToken } from '@angular/core';
import { OAuthService, JwksValidationHandler } from 'angular-oauth2-oidc';
import { Configuration } from './typescript-angular-client';
import { SimsModuleConfig, SIMS_MODULE_CONFIG } from './sims.module.config';

export const SIMS_AUTH_SERVICE = new InjectionToken<SimsAuthService>('simsAuthService');

@Injectable({
  providedIn: 'root'
})
export class SimsAuthService {
  accessToken: string;
  apiLocation: string;

  constructor(private oauthService: OAuthService, 
    @Inject(SIMS_MODULE_CONFIG) moduleConf?: SimsModuleConfig,
    ) {
    if (moduleConf) {
      this.apiLocation = moduleConf.apiLocation;

      //console.log(this.apiLocation);
      this.oauthService.configure(moduleConf.OAuthConfig);

      this.oauthService.tokenValidationHandler = new JwksValidationHandler();

      this.oauthService.silentRefreshRedirectUri = window.location.origin + "/assets/silent-refresh.html";
      this.oauthService.setupAutomaticSilentRefresh();

      this.oauthService.tryLogin({
        onTokenReceived: (info) => {
          console.log('state', info.state);
        }
      });
      /*
          this.oauthService.events.subscribe(e => {
              console.log('oauth/oidc event', e);
          })
          */
    }
  }

  public getConfiguration() {
    // console.log('SimsAuthService getConfiguration');
    // console.log(this.apiLocation);
    return new Configuration({
      accessToken: this.getAccessToken(),
      basePath: this.apiLocation,
      withCredentials: false
    });
  }

  public getAccessToken(): string {
    /*
  this.oauthService.silentRefresh().then(info => console.debug('refresh ok', info))
    .catch(err => {
      console.error('refresh error', err);
      this.accessToken = null;
      this.oauthService.logOut();
    });
    */
    this.accessToken = this.oauthService.getAccessToken();
    // console.log("SimsAuthService getAuthToken:" + this.accessToken);

    return this.accessToken;
  }
}
