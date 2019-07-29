import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetOsListComponent } from './event-set-os-list.component';
import { ActivatedRouteStub, createOAuthServiceSpy } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { MockComponent } from 'ng-mocks';
import { OsListComponent } from '../os-list/os-list.component';

describe('EventSetOsListComponent', () => {
  let component: EventSetOsListComponent;
  let fixture: ComponentFixture<EventSetOsListComponent>;

  let activatedRoute: ActivatedRouteStub;
  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      eventSetId: '1234'
    });

    TestBed.configureTestingModule({
      imports: [
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [
        EventSetOsListComponent,
        MockComponent(OsListComponent)
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetOsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
