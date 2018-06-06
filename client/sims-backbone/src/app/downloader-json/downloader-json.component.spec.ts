import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderJsonComponent } from './downloader-json.component';
import { createOAuthServiceSpy } from 'testing/index.spec';
import { SamplingEventsService } from '../sampling-events.service';
import { SamplingEventService } from '../typescript-angular-client';
import { OAuthService } from 'angular-oauth2-oidc';

describe('DownloaderJsonComponent', () => {
  let component: DownloaderJsonComponent;
  let fixture: ComponentFixture<DownloaderJsonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DownloaderJsonComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: SamplingEventsService },
        { provide: SamplingEventService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderJsonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
