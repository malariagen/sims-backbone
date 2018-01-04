// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  clientId: 'asdfjasdljfasdkjf',
  redirectUri: 'http://localhost/full-map',
  postLogoutRedirectUri: '',
  loginUrl: 'https://sso-dev.cggh.org/sso/oauth2.0/authorize',
  scope: 'editor',
  tokenEndpoint: 'https://sso-dev.cggh.org/sso/oauth2.0/accessToken',
  showDebugInformation: true,
  dummyClientSecret: '1912308409123890',
  apiLocation: 'http://localhost/v1',
  eventSetApiLocation: 'http://localhost/v1'
};
