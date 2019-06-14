import { Injectable } from '@angular/core';


/*
import { AlfrescoApi, NodesApi, NodeEntry, AlfrescoApiConfig } from '@alfresco/js-api';
import { AlfrescoApiService, LogService } from '@alfresco/adf-core';
*/
@Injectable()
export class AuthService {

  accessToken: string;
  alfTicket: string;
//  alfrescoJsApi: AlfrescoApi;

  constructor() {
  }

 
  /*
  public getTicket(): string {
    let headers = new HttpHeaders();
    // to determine the Accept header
    const httpHeaderAccepts: string[] = [
      'text/json'
    ];

    headers = headers.set('Accept', httpHeaderAccepts);

    this.httpClient.get("https://alfresco-dev.malariagen.net/alfresco/s/cas/get-ticket", {
      headers: headers,
      withCredentials: true,
      responseType: "json"
    }).subscribe((response) => {
      console.log(response);

      //this.alfTicket = response.ticket;

      let config: AlfrescoApiConfig =
      {
        provider: 'ECM',
        hostEcm: 'https://alfresco-dev.malariagen.net'
      };
      this.apiService.getInstance().configureJsApi(config);
      //this.alfrescoJsApi = new AlfrescoApi(config);

      this.apiService.getInstance().loginTicket(this.alfTicket, null).then(function (data) {
        console.log('valid ticket you are logged in');
      }, function (error) {
        console.error(error);
      });

      
      console.log(this.alfTicket);
    }, (error) => {
      console.log('error');
      console.log(error);

    });
    return this.alfTicket;
  }

  public getNodeInfo() {
    let nodeId = 'b37beaf1-1902-468e-ac39-f0ffa351c8dc';
    let opts = {};
    let nodesApi = new NodesApi(this.alfrescoJsApi);

    nodesApi.getNode(nodeId, null).then(
      (nodeEntry: NodeEntry) => {
        console.log('This is the name' + nodeEntry.entry.name);
      },
      (error) => {
        console.log('This node does not exist');
      });
  }
  */
}
