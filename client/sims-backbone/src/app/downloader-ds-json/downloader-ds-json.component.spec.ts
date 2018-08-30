import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderDsJsonComponent } from './downloader-ds-json.component';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { DerivativeSampleService } from '../typescript-angular-client';
import { DerivativeSamplesService } from '../derivative-samples.service';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy } from '../../testing/index.spec';

describe('DownloaderDsJsonComponent', () => {
  let component: DownloaderDsJsonComponent;
  let fixture: ComponentFixture<DownloaderDsJsonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [ DownloaderDsJsonComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: DerivativeSamplesService },
        { provide: DerivativeSampleService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderDsJsonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
