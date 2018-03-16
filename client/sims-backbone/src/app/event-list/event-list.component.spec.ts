import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventListComponent } from './event-list.component';
import { Component, Input } from '@angular/core';
import {
  MatProgressBar, MatTable, MatColumnDef, MatHeaderCell, MatCellDef,
  MatHeaderCellDef, MatHeaderRowDef, MatHeaderRow, MatRow, MatRowDef,
  MatCell, MatDialogModule, MatSelect, MatTableModule
} from '@angular/material';
import { OverlayModule } from '@angular/cdk/overlay';


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
});
