import { Injectable } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';
import { Configuration } from './typescript-angular-client/configuration';

@Injectable()
export class AuthService {

  accessToken: string;

  constructor(private oauthService: OAuthService) { }

  public getConfiguration() {
    return new Configuration({
      accessToken: this.getAccessToken(),
      withCredentials: false
    });
  }

  public getAccessToken(): string {
      this.accessToken = this.oauthService.getAccessToken();
      if (! this.accessToken) {
        this.oauthService.initImplicitFlow();
    }
    console.log("AuthService getAuthToken:" + this.accessToken);
    return this.accessToken;
  }
}
