import 'rxjs/add/operator/do';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HttpErrorResponse } from '@angular/common/http';

import { Observable } from 'rxjs';
import { OAuthService } from 'angular-oauth2-oidc';
import { Injectable, Inject, Optional } from '@angular/core';
import { SimsModuleConfig, SIMS_MODULE_CONFIG } from '../sims.module.config';


@Injectable()
export class SimsResponseInterceptor implements HttpInterceptor {

    apiLocation: string;

    constructor(private oauthService: OAuthService,
        @Optional() @Inject(SIMS_MODULE_CONFIG) config?: SimsModuleConfig) {

        this.apiLocation = config.apiLocation;
    }



    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        return next.handle(request).do((event: HttpEvent<any>) => {

            if (event instanceof HttpResponse) {
                // do stuff with response if you want
                //console.log('lib OK');
                //console.log(event);
            }
        }, (err: any) => {
            if (err instanceof HttpErrorResponse) {
                if (err.status === 401) {
                    if (this.oauthService.clientId == null) {
                        console.log('Please check authentication configuration');
                        //console.log(casAuthConfig);
                    } else if (this.oauthService.redirectUri.endsWith('/')) {
                        console.log('redirectUri must not end with a / e.g. https://sims.malariagen.net/studies is OK');
                    } else {
                        //console.log('SimsModule initImplicitFlow');
                        if (err.url.startsWith(this.apiLocation)) {
                            this.oauthService.initImplicitFlow();
                        }
                    }
                } else {
                    console.log('SimsModule err');
                    console.error(err);
                }
            } else {
                console.log('SimsModule Not HttpErrorResponse');
                console.log(err);
            }
        });
    }
}
