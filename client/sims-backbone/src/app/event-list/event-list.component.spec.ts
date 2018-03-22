import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventListComponent } from './event-list.component';
import { Component, Input } from '@angular/core';
import {
  MatProgressBar, MatTable, MatColumnDef, MatHeaderCell, MatCellDef,
  MatHeaderCellDef, MatHeaderRowDef, MatHeaderRow, MatRow, MatRowDef,
  MatCell, MatDialogModule, MatSelect, MatTableModule
} from '@angular/material';
import { OverlayModule } from '@angular/cdk/overlay';
import { SamplingEvents } from '../typescript-angular-client';


@Component({ selector: 'app-csv-downloader', template: '' })
class CsvDownloaderStubComponent {
  @Input() location;
  @Input() data;
  @Input() fileName;
  @Input() headers;
}

describe('EventListComponent', () => {
  let component: EventListComponent;
  let fixture: ComponentFixture<EventListComponent>;

  let test_entries = <SamplingEvents>{
    "count": 2,
    "locations": {
      "ba58650c-f365-41bd-a73d-d8517e9a01e5": {
        "country": "KHM",
        "identifiers": [
          {
            "identifier_source": "test",
            "identifier_type": "partner_name",
            "identifier_value": "Cambodia",
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
        "identifiers": [
          {
            "identifier_source": "vobs_dump",
            "identifier_type": "partner_id",
            "identifier_value": "9999_1"
          },
          {
            "identifier_source": "vobs_dump",
            "identifier_type": "roma_id",
            "identifier_value": "9999_1R"
          }
        ],
        "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "partner_species": "An. dirus A",
        "partner_taxonomies": [
          {
            "taxonomy_id": 7168
          }
        ],
        "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "sampling_event_id": "0b0593ae-c613-42b6-8d3f-2bec2b3bd29c",
        "study_name": "9999"
      },
      {
        "doc": "2003-06-01",
        "identifiers": [
          {
            "identifier_source": "vobs_dump",
            "identifier_type": "partner_id",
            "identifier_value": "9999_2"
          },
          {
            "identifier_source": "vobs_dump",
            "identifier_type": "roma_id",
            "identifier_value": "9999_2R"
          }
        ],
        "location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "partner_species": "An. dirus A",
        "partner_taxonomies": [
          {
            "taxonomy_id": 7168
          }
        ],
        "public_location_id": "ba58650c-f365-41bd-a73d-d8517e9a01e5",
        "sampling_event_id": "6890728f-c5e0-4c16-ac6d-b2505188a72b",
        "study_name": "9999"
      }
    ]
  }

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        MatDialogModule,
        OverlayModule,
        MatTableModule
      ],
      declarations: [
        EventListComponent,
        CsvDownloaderStubComponent,
        MatProgressBar,
        MatSelect
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should create rows', () => {

    component.events = test_entries;

    expect(component._pageNumber).toBe(0);

    component.dataSource.connect().forEach(value => {
      
      for (let i = 0; i < test_entries.count; i++) {
        let row = value[i];
        let sampling_event = test_entries.sampling_events[i];
        
        expect(row.study_id).toBe(sampling_event.study_name);
        sampling_event.identifiers.forEach(ident => {
          if(ident.identifier_type == 'partner_id') {
            expect(row.partner_id).toBe(ident.identifier_value);    
          }
          if(ident.identifier_type == 'roma_id') {
            expect(row.roma_id).toBe(ident.identifier_value);    
          }
        });
        expect(row.doc).toBe(sampling_event.doc);
        expect(row.partner_species).toBe(sampling_event.partner_species);
        expect(row.taxa).toBe((sampling_event.partner_taxonomies[0].taxonomy_id).toString());
        let location = test_entries.locations[test_entries.sampling_events[i].location_id];
        let partner_name : string;
        location.identifiers.forEach(ident => {
          if (ident.study_name == sampling_event.study_name && ident.identifier_type == 'partner_name') {
            partner_name = ident.identifier_value;
          }
        });
        expect(row.partner_location_name).toBe(partner_name);
      }

    });
  });

  it('should set headers', () => {

    component.events = test_entries;
    let expectedHeaders = ["study_id", "partner_id", "roma_id", "doc", "partner_species", "taxa", "partner_location_name", "location_curated_name", "location"];

    expect(component.displayedColumns.length).toBe(expectedHeaders.length);
    
    for(let i=0; i< expectedHeaders.length;i++) {
      expect(component.displayedColumns[i]).toBe(expectedHeaders[i]);
    }
    

  });
});
