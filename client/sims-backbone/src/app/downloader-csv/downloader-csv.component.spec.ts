import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderCsvComponent } from './downloader-csv.component';
import { createOAuthServiceSpy } from 'testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { SamplingEventsService } from '../sampling-events.service';
import { SamplingEventService } from '../typescript-angular-client';

describe('DownloaderCsvComponent', () => {
  let component: DownloaderCsvComponent;
  let fixture: ComponentFixture<DownloaderCsvComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DownloaderCsvComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: SamplingEventsService },
        { provide: SamplingEventService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderCsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
