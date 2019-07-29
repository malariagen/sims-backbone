import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyDsListComponent } from './study-ds-list.component';
import { ActivatedRouteStub, createOAuthServiceSpy } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { MockComponent } from 'ng-mocks';
import { DsListComponent } from '../ds-list/ds-list.component';

describe('StudyDsListComponent', () => {
  let component: StudyDsListComponent;
  let fixture: ComponentFixture<StudyDsListComponent>;

  let activatedRoute: ActivatedRouteStub;
  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      studyName: '1234'
    });

    TestBed.configureTestingModule({
      imports: [
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [
        StudyDsListComponent,
        MockComponent(DsListComponent)
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyDsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
