import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Studies } from '../typescript-angular-client/model/studies';

import { asyncData } from '../../testing/index.spec';

import { AllStudiesListComponent } from './all-studies-list.component';
import { StudyService } from '../typescript-angular-client';
import { Component, Input } from '@angular/core';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs/observable/of';

@Component({ selector: 'sims-studies-list', template: '' })
class StudiesListStubComponent {
  @Input() studies: Studies;
}

describe('AllStudiesListComponent', () => {
  let component: AllStudiesListComponent;
  let fixture: ComponentFixture<AllStudiesListComponent>;
  let httpClientSpy: { get: jasmine.Spy };
  let studyService: StudyService;

  beforeEach(async(() => {

    // Create a fake AuthService object 
    const authService = jasmine.createSpyObj('OAuthService', ['getAccessToken', 'getConfiguration']);
    // Make the spy return a synchronous Observable with the test data
    let getAccessToken = authService.getAccessToken.and.returnValue(of(undefined));
    let getConfiguration = authService.getConfiguration.and.returnValue(of(undefined));

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);
    studyService = new StudyService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      declarations: [
        AllStudiesListComponent,
        StudiesListStubComponent
      ],
      providers: [
        { provide: OAuthService, useValue: authService },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: StudyService, useValue: studyService }
      ]
    })
      .compileComponents();

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AllStudiesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });

  it('should have requested all studies', () => {
    expect(httpClientSpy.get.calls.first().args[0]).toBe('http://localhost/v1/studies', 'url');
    expect(httpClientSpy.get.calls.mostRecent().args[0]).toBe('http://localhost/v1/study/9999', 'url');
    expect(httpClientSpy.get.calls.count()).toBe(4, 'one call');
  });
});
