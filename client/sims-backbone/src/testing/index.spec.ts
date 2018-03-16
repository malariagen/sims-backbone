import { DebugElement } from '@angular/core';
import { tick, ComponentFixture } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';

export * from './async-observable-helpers';
export * from './activated-route-stub';

// Create a fake AuthService object 
export function createOAuthServiceSpy() {
    const authService = jasmine.createSpyObj('OAuthService', ['configure', 'setupAutomaticSilentRefresh', 'tryLogin']);
    // Make the spy return a synchronous Observable with the test data
    let configure = authService.configure.and.returnValue(of(undefined));
    let setupAutomaticSilentRefresh = authService.setupAutomaticSilentRefresh.and.returnValue(of(undefined));
    let tryLogin = authService.tryLogin.and.returnValue(of(undefined));
    return authService;
}

export function createAuthServiceSpy() {
    // Create a fake AuthService object 
    const authService = jasmine.createSpyObj('AuthService', ['getAccessToken', 'getConfiguration']);
    // Make the spy return a synchronous Observable with the test data
    let getAccessToken = authService.getAccessToken.and.returnValue(of(undefined));
    let getConfiguration = authService.getConfiguration.and.returnValue(of(undefined));

    return authService;
}