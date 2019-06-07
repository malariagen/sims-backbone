import 'rxjs/add/operator/do';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HttpErrorResponse } from '@angular/common/http';
import { AuthService } from 'app/auth.service';
import { Observable } from 'rxjs';
import { OAuthService } from 'angular-oauth2-oidc';
import { Injectable } from '@angular/core';
import { casAuthConfig } from '../auth.config';

@Injectable()
export class ResponseInterceptor implements HttpInterceptor {
    constructor(public auth: AuthService, private oauthService: OAuthService) { }
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

        return next.handle(request).do((event: HttpEvent<any>) => {
            if (event instanceof HttpResponse) {
                // do stuff with response if you want
            }
        }, (err: any) => {
            if (err instanceof HttpErrorResponse) {
                if (err.status === 401) {
                    if (sprocess.env.CLIENT_SECRET == null) {
                        console.log('Please check authentication configuration');
                        console.log(casAuthConfig);
                    } else {
                        this.oauthService.initImplicitFlow();
                    }
                } else {
                    console.error(err);
                }
            } else {
                console.log(err);
            }
        });
    }
}
