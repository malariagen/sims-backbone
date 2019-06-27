import { Injectable } from '@angular/core';
import { SimsModuleConfig } from './sims.module.config';
import { LazyMapsAPILoaderConfigLiteral } from '@agm/core';

@Injectable({
    providedIn: 'root'
  })
export class CustomMapsConfig implements LazyMapsAPILoaderConfigLiteral {
  apiKey?: string;
  libraries: string[];
  constructor(private moduleConf: SimsModuleConfig) {
    this.apiKey = moduleConf.mapsApiKey;
    this.libraries = ["places"];
    //console.log('Custom Map config');
  }
}
