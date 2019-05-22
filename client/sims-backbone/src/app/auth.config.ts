import { AuthConfig } from 'angular-oauth2-oidc';
import { environment } from '../environments/environment';

export const casAuthConfig: AuthConfig = {
  'clientId': sprocess.env.CLIENT_ID,
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
  'dummyClientSecret': sprocess.env.CLIENT_SECRET,

}
