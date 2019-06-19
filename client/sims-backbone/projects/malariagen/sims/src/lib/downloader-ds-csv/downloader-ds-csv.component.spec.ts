import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderDsCsvComponent } from './downloader-ds-csv.component';
import { OAuthService } from 'angular-oauth2-oidc';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { DerivativeSampleService } from '../typescript-angular-client';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { createOAuthServiceSpy } from '../../testing/index.spec';

describe('DownloaderDsCsvComponent', () => {
  let component: DownloaderDsCsvComponent;
  let fixture: ComponentFixture<DownloaderDsCsvComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [ DownloaderDsCsvComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: DerivativeSamplesService },
        { provide: DerivativeSampleService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderDsCsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
