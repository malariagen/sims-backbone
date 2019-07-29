import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMultipleLocationNamesComponent } from './report-multiple-location-names.component';
import { ReportService } from '../typescript-angular-client';
import { createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';
import { MockComponent } from 'ng-mocks';
import { StudiesListComponent } from '../studies-list/studies-list.component';

describe('ReportMultipleLocationNamesComponent', () => {
  let component: ReportMultipleLocationNamesComponent;
  let fixture: ComponentFixture<ReportMultipleLocationNamesComponent>;

  let httpClientSpy: { get: jasmine.Spy };
  let reportService: ReportService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    reportService = new ReportService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        ReportMultipleLocationNamesComponent,
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
    fixture = TestBed.createComponent(ReportMultipleLocationNamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
