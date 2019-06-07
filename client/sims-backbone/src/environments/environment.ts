// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  redirectUri: 'http://localhost:4200/',
  postLogoutRedirectUri: 'https://www.malariagen.net',
  loginUrl: 'https://www.malariagen.net/sso/oauth2.0/authorize',
  scope: 'editor',
  tokenEndpoint: 'https://www.malariagen.net/sso/oauth2.0/accessToken',
  showDebugInformation: true,
  apiLocation: 'http://localhost:4200/v1'
}
