import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaDsListComponent } from './taxa-ds-list.component';
import { ActivatedRouteStub, createOAuthServiceSpy } from '../../testing/index.spec';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { OAuthService } from 'angular-oauth2-oidc';
import { DsListComponent } from '../ds-list/ds-list.component';
import { MockComponent } from 'ng-mocks';


describe('TaxaDsListComponent', () => {
  let component: TaxaDsListComponent;
  let fixture: ComponentFixture<TaxaDsListComponent>;

  let activatedRoute: ActivatedRouteStub;
  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      taxaId: 5877
    });

    TestBed.configureTestingModule({
      imports: [
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [
        TaxaDsListComponent,
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
    fixture = TestBed.createComponent(TaxaDsListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
