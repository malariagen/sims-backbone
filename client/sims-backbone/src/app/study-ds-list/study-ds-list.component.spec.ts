import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyDsListComponent } from './study-ds-list.component';
import { Component, Input } from '@angular/core';
import { ActivatedRouteStub, createOAuthServiceSpy } from 'testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-ds-list',
  template: ''
})
export class DsListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
  @Input() downloadFileName: string;
  @Input() jsonDownloadFileName: string;
}
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
      declarations: [StudyDsListComponent,
        DsListComponentStub
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
