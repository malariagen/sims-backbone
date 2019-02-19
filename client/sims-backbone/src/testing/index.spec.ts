import { DebugElement } from '@angular/core';
import { tick, ComponentFixture } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';
import { Configuration, SamplingEvents } from '../app/typescript-angular-client';

export * from './async-observable-helpers';
export * from './activated-route-stub';

// Create a fake AuthService object
export function createOAuthServiceSpy() {
    const authService = jasmine.createSpyObj('OAuthService', ['configure', 'setupAutomaticSilentRefresh', 'tryLogin']);
    // Make the spy return a synchronous Observable with the test data
    const configure = authService.configure.and.returnValue(of(undefined));
    const setupAutomaticSilentRefresh = authService.setupAutomaticSilentRefresh.and.returnValue(of(undefined));
    const tryLogin = authService.tryLogin.and.returnValue(of(undefined));
    return authService;
}

export function createAuthServiceSpy() {
    // Create a fake AuthService object
    const authService = jasmine.createSpyObj('AuthService', ['getAccessToken', 'getConfiguration']);
    // Make the spy return a synchronous Observable with the test data
    const getAccessToken = authService.getAccessToken.and.returnValue(of(undefined));
    const getConfiguration = new Configuration({
        accessToken: '',
        basePath: '',
        withCredentials: false
      });

    return authService;
}

export function getTestSamplingEvents() {
    const test_entries = <SamplingEvents>{
        'count': 2,
        'attrTypes': [
          'partner_id',
          'roma_id'
        ],
        'locations': {
          'ba58650c-f365-41bd-a73d-d8517e9a01e5': {
            'country': 'KHM',
            'attrs': [
              {
                'attrSource': 'test',
                'attrType': 'partner_name',
                'attrValue': 'Cambodia',
                'studyName': '9999'
              }
            ],
            'latitude': 12.565679,
            'locationId': 'ba58650c-f365-41bd-a73d-d8517e9a01e5',
            'longitude': 104.990963,
            'notes': 'test'
          }
        },
        'samplingEvents': [
          {
            'doc': '2003-06-01',
            'attrs': [
              {
                'attrSource': 'vobs_dump',
                'attrType': 'partner_id',
                'attrValue': '9999_1'
              },
              {
                'attrSource': 'vobs_dump',
                'attrType': 'roma_id',
                'attrValue': '9999_1R'
              }
            ],
            'locationId': 'ba58650c-f365-41bd-a73d-d8517e9a01e5',
            'publicLocationId': 'ba58650c-f365-41bd-a73d-d8517e9a01e5',
            'samplingEventId': '0b0593ae-c613-42b6-8d3f-2bec2b3bd29c'
          },
          {
            'doc': '2003-06-01',
            'attrs': [
              {
                'attrSource': 'vobs_dump',
                'attrType': 'partner_id',
                'attrValue': '9999_2'
              },
              {
                'attrSource': 'vobs_dump',
                'attrType': 'roma_id',
                'attrValue': '9999_2R'
              }
            ],
            'locationId': 'ba58650c-f365-41bd-a73d-d8517e9a01e5',
            'publicLocationId': 'ba58650c-f365-41bd-a73d-d8517e9a01e5',
            'samplingEventId': '6890728f-c5e0-4c16-ac6d-b2505188a72b'
          }
        ]
      }

      return test_entries;
}
