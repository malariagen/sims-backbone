import { AuthConfig } from 'angular-oauth2-oidc';

export const casAuthConfig: AuthConfig = {
  'clientId': '',
  'redirectUri': 'http://localhost/full-map',
  'postLogoutRedirectUri': '',
  'loginUrl': 'https://sso-dev.cggh.org/sso/oauth2.0/authorize',
  'scope': 'openid profile email',
  'resource': '',
  'rngUrl': '',
  'oidc': false,
  'requestAccessToken': true,
  'options': null,
  'clearHashAfterLogin': true,
  'tokenEndpoint': 'https://sso-dev.cggh.org/sso/oauth2.0/accessToken',
  'responseType': 'code',
  'showDebugInformation': true,
  'dummyClientSecret': '',

}
