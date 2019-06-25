// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  redirectUri: sprocess.env.SIMS_REDIRECT_URI,
  postLogoutRedirectUri: 'https://www.malariagen.net',
  loginUrl: 'https://www.malariagen.net/sso/oauth2.0/authorize',
  scope: 'editor',
  tokenEndpoint: 'https://www.malariagen.net/sso/oauth2.0/accessToken',
  showDebugInformation: true,
  apiLocation: sprocess.env.BACKBONE_API_LOCATION,
  clientId: sprocess.env.CLIENT_ID,
  dummyClientSecret: sprocess.env.CLIENT_SECRET,
  mapsApiKey: sprocess.env.GOOGLE_API_KEY
}
