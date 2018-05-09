import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportMultipleLocationNamesComponent } from './report-multiple-location-names.component';
import { Component, Input } from '@angular/core';
import { Studies, ReportService } from '../typescript-angular-client';
import { createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';

@Component({ selector: 'app-studies-list', template: '' })
class StudiesListStubComponent {
  @Input() studies: Studies;
}

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
        ReportMissingTaxaComponent,
        StudiesListStubComponent
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
