import { DebugElement } from '@angular/core';
import { tick, ComponentFixture } from '@angular/core/testing';
import { of } from 'rxjs/observable/of';
import { Configuration, SamplingEvents, OriginalSamples, DerivativeSamples, AssayData } from '../lib/typescript-angular-client';


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

export function getTestOriginalSamples() {
  let test_entries = <OriginalSamples>{
    "original_samples": [
      {
        "attrs": [
          {
            "attr_source": "vivax_20190715",
            "attr_type": "partner_id",
            "attr_value": "0001"
          },
          {
            "attr_source": "vivax_20190715",
            "attr_type": "roma_id",
            "attr_value": "VVX0001"
          }
        ],
        "original_sample_id": "bcb1e089-d1ee-43f0-bc5f-02073380b656",
        "partner_species": "Plasmodium vivax",
        "partner_taxonomies": [
          {
            "taxonomy_id": 5855
          }
        ],
        "sampling_event_id": "e0e73994-b9e5-48d0-af1e-84bc1e6d0cd5",
        "study_name": "0001-PV-MD-UP"
      },
      {
        "attrs": [
          {
            "attr_source": "vivax_20190715",
            "attr_type": "partner_id",
            "attr_value": "00002"
          },
          {
            "attr_source": "vivax_20190715",
            "attr_type": "roma_id",
            "attr_value": "VVX00002"
          }
        ],
        "original_sample_id": "4e7748c2-eed2-4920-8db6-c8df0ab675a3",
        "partner_species": "Plasmodium vivax",
        "partner_taxonomies": [
          {
            "taxonomy_id": 5855
          }
        ],
        "sampling_event_id": "0aff80b8-fd1c-47ba-be3a-c3d123b4e28b",
        "study_name": "0001-PV-MD-UP"
      }
    ],
    "sampling_events": {
      "038f6de5-a0da-46d3-899d-a366aae4cdb3": {
        "attrs": [
          {
            "attr_source": "vivax_20190715",
            "attr_type": "roma_pk_id",
            "attr_value": "vivax_4111"
          }
        ],
        "doc": "2015-04-25",
        "event_sets": [
          "vivax_20190715",
          "vivax_XMF00045"
        ],
        "location": {
          "attrs": [
            {
              "attr_source": "vivax_20190715",
              "attr_type": "partner_name",
              "attr_value": "Site1",
              "study_name": "0001-PV-MD-UP"
            },
            {
              "attr_source": "vivax_20190715",
              "attr_type": "src_location_id",
              "attr_value": "vivax_loc_198",
              "study_name": "0001-PV-MD-UP"
            }
          ],
          "country": "VNM",
          "latitude": 13.3049167,
          "location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
          "longitude": 108.602694,
          "notes": "vivax_20190715"
        },
        "location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
        "public_location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
        "sampling_event_id": "038f6de5-a0da-46d3-899d-a366aae4cdb3"
      },
      "0aff80b8-fd1c-47ba-be3a-c3d123b4e28b": {
        "attrs": [
          {
            "attr_source": "vivax_20190715",
            "attr_type": "roma_pk_id",
            "attr_value": "vivax_4174"
          }
        ],
        "doc": "2015-06-09",
        "event_sets": [
          "vivax_20190715",
          "vivax_XMF00045"
        ],
        "location": {
          "attrs": [
            {
              "attr_source": "vivax_20190715",
              "attr_type": "partner_name",
              "attr_value": "Site1",
              "study_name": "0001-PV-MD-UP"
            },
            {
              "attr_source": "vivax_20190715",
              "attr_type": "src_location_id",
              "attr_value": "vivax_loc_198",
              "study_name": "0001-PV-MD-UP"
            }
          ],
          "country": "VNM",
          "latitude": 13.3049167,
          "location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
          "longitude": 108.602694,
          "notes": "vivax_20190715"
        },
        "location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
        "public_location_id": "96bf851a-1b0c-4f09-82f4-58832d3d7f85",
        "sampling_event_id": "0450cc15-9559-47a3-a794-6d3e5a795af7"
      }
    },
    "attr_types": [
      "roma_id",
      "partner_id"
    ],
    "count": 2
  };

  return test_entries;
}

export function getTestDerivativeSamples() {
  const test_entries = <DerivativeSamples>{
    "derivative_samples": [
      {
        "derivative_sample_id": "0f1aaffe-7de2-4adc-b593-c53c37a1ab1c",
        "original_sample_id": "529b4442-c1b8-454b-bb86-76242b1cb7bd",
        "dna_prep": null,
        "attrs": [
          { "attr_type": "plate_name", "attr_value": "PLATE_RCN_00022", "attr_source": "genre_20190609", "study_name": null },
          { "attr_type": "plate_position", "attr_value": "H10", "attr_source": "genre_20190609", "study_name": null }
        ],
        "assay_data": null
      }, {
        "derivative_sample_id": "1334aae7-fdee-4244-a960-396c714886c4",
        "original_sample_id": "58932826-5adf-4cfc-9f3b-238de4a52f6d",
        "dna_prep": null,
        "attrs": [
          { "attr_type": "plate_name", "attr_value": "PLATE_RCN_00023", "attr_source": "genre_20190609", "study_name": null },
          { "attr_type": "plate_position", "attr_value": "G04", "attr_source": "genre_20190609", "study_name": null }
        ],
        "assay_data": null
      }
    ],
    "count": 2,
    "attr_types": ["plate_name", "plate_position"]
  };

  return test_entries;
}

export function getTestAssayData() {
  let test_entries = <AssayData>{

  };

  return test_entries;
}
