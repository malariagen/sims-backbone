import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OsListComponent } from './os-list.component';
import { Component, Input } from '@angular/core';
import { OriginalSampleDisplayPipe } from '../original-sample-display.pipe';
import { OriginalSamplesService } from '../original-samples.service';
import { OriginalSampleService } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy } from 'testing/index.spec';
import { OverlayModule } from '@angular/cdk/overlay';
import { MatTableModule, MatOptionModule, MatPaginatorModule, MatFormFieldModule, MatTooltipModule } from '@angular/material';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

@Component({ selector: 'sims-downloader-os-csv', template: '' })
class DownloaderOsCsvStubComponent {
  @Input() filter;
  @Input() fileName;
  @Input() headers;
}

@Component({ selector: 'sims-downloader-os-json', template: '' })
class DownloaderOsJsonStubComponent {
  @Input() filter;
  @Input() fileName;
}

describe('OsListComponent', () => {
  let component: OsListComponent;
  let fixture: ComponentFixture<OsListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        OverlayModule,
        MatTableModule,
        MatOptionModule,
        MatPaginatorModule,
        MatFormFieldModule,
        MatTooltipModule,
        HttpClientModule,
        HttpClientTestingModule,
        NoopAnimationsModule
      ],
      declarations: [ 
        OsListComponent,
        DownloaderOsCsvStubComponent,
        DownloaderOsJsonStubComponent,
        OriginalSampleDisplayPipe, 
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: OriginalSampleService },
        { provide: OriginalSamplesService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
