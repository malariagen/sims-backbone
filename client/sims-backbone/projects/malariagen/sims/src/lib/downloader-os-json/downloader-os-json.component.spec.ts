import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderOsJsonComponent } from './downloader-os-json.component';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OriginalSampleService } from '../typescript-angular-client';
import { OriginalSamplesService } from '../original-samples.service';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy } from '../../testing/index.spec';

describe('DownloaderOsJsonComponent', () => {
  let component: DownloaderOsJsonComponent;
  let fixture: ComponentFixture<DownloaderOsJsonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [ DownloaderOsJsonComponent ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: OriginalSamplesService },
        { provide: OriginalSampleService },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderOsJsonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
