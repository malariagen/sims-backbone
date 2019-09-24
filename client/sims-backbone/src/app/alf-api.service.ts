import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AlfrescoApiCompatibility as AlfrescoApi, AlfrescoApiConfig } from '@alfresco/js-api';

import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AlfApiService {
  _alfrescoApi: AlfrescoApi;
  ecmApiLocation: string;

  constructor(protected httpClient: HttpClient) {
    this.ecmApiLocation = environment.alfrescoLocation;
  }

  public alfrescoApi() {
    if (!this._alfrescoApi) {
      return this.login();
    }
    return new Promise((resolve, reject) => {
      resolve(this._alfrescoApi);
    });
  }

  public login() {

    return new Promise((resolve, reject) =>
      this.httpClient.get(this.ecmApiLocation + '/alfresco/s/cas/get-ticket',
        {
          withCredentials: true
        }
      ).toPromise().then(
        (ticket) => {
          let ticketEcm: string = ticket['ticket'];
          let ticketBpm = undefined;
          this._alfrescoApi = new AlfrescoApi({
            ticketEcm: ticketEcm,
            hostEcm: this.ecmApiLocation
          });
          
          this._alfrescoApi.loginTicket(ticketEcm, ticketBpm).then(function (data) {
            // console.log('valid ticket you are logged in');
          }, function (error) {
            console.error(error);
            reject(error);
          });
          resolve(this._alfrescoApi);
        }
      ));
  }
}
