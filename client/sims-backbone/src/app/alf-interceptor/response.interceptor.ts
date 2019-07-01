import 'rxjs/add/operator/do';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HttpErrorResponse } from '@angular/common/http';

import { Observable } from 'rxjs';
import { OAuthService, AuthConfig } from 'angular-oauth2-oidc';
import { Injectable, InjectionToken, Inject, Optional } from '@angular/core';
import { AlfApiService } from 'app/alf-api.service';


@Injectable()
export class AlfResponseInterceptor implements HttpInterceptor {
    
    ecmApiLocation: string;

    constructor(private oauthService: OAuthService, private alfrescoService: AlfApiService) {
        this.ecmApiLocation = alfrescoService.ecmApiLocation;
    }



    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        return next.handle(request).do((event: HttpEvent<any>) => {

            if (event instanceof HttpResponse) {
                // do stuff with response if you want
                //console.log('lib OK');
                //console.log(event);
//                this.alfrescoService.login();
              
            }
        }, (err: any) => {
            if (err instanceof HttpErrorResponse) {
                if (err.status === 401) {
                    if (this.oauthService.clientId == null) {
                        console.log('Please check authentication configuration');
                        //console.log(casAuthConfig);
                    } else {
                        console.log('AlfResponseInterceptor initImplicitFlow');
                        if (err.url.startsWith(this.ecmApiLocation)) {
                            this.oauthService.initImplicitFlow();
                        }
                        this.alfrescoService.login();
                    }
                } else {
                    //console.log('AlfResponseInterceptor err');
                    //console.error(err);
                }
            } else {
                //console.log('AlfResponseInterceptor Not HttpErrorResponse');
                //console.log(err);
            }
        });
    }
}
