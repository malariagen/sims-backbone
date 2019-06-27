import { AuthConfig } from 'angular-oauth2-oidc';
import { InjectionToken } from '@angular/core';

export const SIMS_MODULE_CONFIG = new InjectionToken<SimsModuleConfig>('simsModuleConfig');

export class SimsModuleConfig {
  apiLocation: string;
  mapsApiKey?: string;
  OAuthConfig: AuthConfig;
}
