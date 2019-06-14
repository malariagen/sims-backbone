import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetListComponent } from './event-set-list.component';
import { RouterLink, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { OAuthService } from 'angular-oauth2-oidc';
import { createOAuthServiceSpy, createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { EventSetService } from '../typescript-angular-client';

describe('EventSetListComponent', () => {
  let component: EventSetListComponent;
  let fixture: ComponentFixture<EventSetListComponent>;

  let httpClientSpy: { get: jasmine.Spy };

  let eventSetService: EventSetService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    eventSetService = new EventSetService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        RouterModule
      ],
      declarations: [
        EventSetListComponent
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: HttpClient, useValue: httpClientSpy },
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
