import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMultipleLocationGpsComponent } from './report-multiple-location-gps.component';
import { ReportService } from '../typescript-angular-client';
import { createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { StudiesListComponent } from '../studies-list/studies-list.component';

describe('ReportMultipleLocationGpsComponent', () => {
  let component: ReportMultipleLocationGpsComponent;
  let fixture: ComponentFixture<ReportMultipleLocationGpsComponent>;

  let httpClientSpy: { get: jasmine.Spy };
  let reportService: ReportService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    reportService = new ReportService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        ReportMultipleLocationGpsComponent,
        MockComponent(StudiesListComponent)
      ],
      providers: [
        { provide: OAuthService, useValue: authService },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: ReportService, useValue: reportService }
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ReportMultipleLocationGpsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
