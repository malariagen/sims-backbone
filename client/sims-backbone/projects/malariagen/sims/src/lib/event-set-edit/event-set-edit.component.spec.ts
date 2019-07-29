import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEditComponent } from './event-set-edit.component';
import { FormsModule, FormGroup, ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { MatDialogModule, MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ActivatedRouteStub, createOAuthServiceSpy, createAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { ActivatedRoute, RouterLink, RouterModule } from '@angular/router';
import { OAuthService } from 'angular-oauth2-oidc';
import { EventSetService } from '../typescript-angular-client';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import {ObserversModule} from '@angular/cdk/observers';
import { MatFormField } from '@angular/material';


describe('EventSetEditComponent', () => {
  let component: EventSetEditComponent;
  let fixture: ComponentFixture<EventSetEditComponent>;
  let activatedRoute: ActivatedRouteStub;

  let httpClientSpy: { get: jasmine.Spy };

  let eventSetService: EventSetService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({ eventSetId: 'evsid' });

    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: []}));

    eventSetService = new EventSetService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        FormsModule, 
        ReactiveFormsModule, 
        RouterModule,
        MatDialogModule,
        ObserversModule
      ],
      declarations: [
        EventSetEditComponent,
        MatFormField
      ],
      providers: [
        FormBuilder,
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: EventSetService, useValue: eventSetService },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: MAT_DIALOG_DATA, useValue: {} }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
