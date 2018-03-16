import { Component } from '@angular/core';

import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { EventSetAddDialogComponent } from './event-set-add-dialog/event-set-add-dialog.component';

import { OAuthService } from 'angular-oauth2-oidc';
import { JwksValidationHandler } from 'angular-oauth2-oidc';

import { casAuthConfig } from './auth.config';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'SIMS Backbone';

    constructor(private oauthService: OAuthService, public dialog: MatDialog) {

        this.oauthService.configure(casAuthConfig);
        this.oauthService.tokenValidationHandler = new JwksValidationHandler();

        this.oauthService.silentRefreshRedirectUri = window.location.origin + "/assets/silent-refresh.html";
        this.oauthService.setupAutomaticSilentRefresh();
/*
        this.oauthService.tryLogin({
            onTokenReceived: (info) => {
                console.log('state', info.state);
            }
        });

        this.oauthService.events.subscribe(e => {
            console.log('oauth/oidc event', e);
        })
        */
    }

    addEventSet(action) {

        let dialogRef = this.dialog.open(EventSetAddDialogComponent, {
            width: '600px'
        });

    }

}
