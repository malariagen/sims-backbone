import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderOsCsvComponent } from './downloader-os-csv.component';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy } from '../../testing/index.spec';
import { OriginalSamplesService } from '../original-samples.service';
import { OriginalSampleService } from '../typescript-angular-client';

describe('DownloaderOsCsvComponent', () => {
  let component: DownloaderOsCsvComponent;
  let fixture: ComponentFixture<DownloaderOsCsvComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [ DownloaderOsCsvComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: OriginalSamplesService },
        { provide: OriginalSampleService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderOsCsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
