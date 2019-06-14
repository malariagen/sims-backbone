import { DebugElement } from '@angular/core';
import { tick, ComponentFixture } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';
import { Configuration, SamplingEvents } from '../lib/typescript-angular-client';

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
    let getConfiguration = new Configuration({
        accessToken: '',
        basePath: '',
        withCredentials: false
      });

    return authService;
}

export function getTestSamplingEvents() {
    let test_entries = <SamplingEvents>{
        "count": 2,
        "attr_types": [
          "partner_id",
          "roma_id"
        ],
        "locations": {
          "ba58650c-f365-41bd-a73d-d8517e9a01e5": {
            "country": "KHM",
            "attrs": [
              {
                "attr_source": "test",
                "attr_type": "partner_name",
                "attr_value": "Cambodia",
                "study_name": "9999"
              }
            ],
            "latitude": 12.565679,
            "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
            "longitude": 104.990963,
            "notes": "test"
          }
        },
        "sampling_events": [
          {
            "doc": "2003-06-01",
            "attrs": [
              {
                "attr_source": "vobs_dump",
                "attr_type": "partner_id",
                "attr_value": "9999_1"
              },
              {
                "attr_source": "vobs_dump",
                "attr_type": "roma_id",
                "attr_value": "9999_1R"
              }
            ],
            "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
            "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
            "sampling_event_id": "0b0593ae-c613-42b6-8d3f-2bec2b3bd29c"
          },
          {
            "doc": "2003-06-01",
            "attrs": [
              {
                "attr_source": "vobs_dump",
                "attr_type": "partner_id",
                "attr_value": "9999_2"
              },
              {
                "attr_source": "vobs_dump",
                "attr_type": "roma_id",
                "attr_value": "9999_2R"
              }
            ],
            "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
            "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
            "sampling_event_id": "6890728f-c5e0-4c16-ac6d-b2505188a72b"
          }
        ]
      }

      return test_entries;
}