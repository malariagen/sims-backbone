import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyOsListComponent } from './study-os-list.component';
import { Component, Input } from '@angular/core';
import { ActivatedRouteStub, createOAuthServiceSpy } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';

@Component({
  selector: 'sims-os-list',
  template: ''
})
export class OsListComponentStub {
  @Input() filter: string;
  @Input() studyName: string;
  @Input() downloadFileName: string;
  @Input() jsonDownloadFileName: string;
}
describe('StudyOsListComponent', () => {
  let component: StudyOsListComponent;
  let fixture: ComponentFixture<StudyOsListComponent>;

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
        StudyOsListComponent,
        OsListComponentStub
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyOsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
