import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TaxaListComponent } from './taxa-list.component';
import { RouterModule } from '@angular/router';
import { MetadataService } from '../typescript-angular-client';
import { asyncData, createOAuthServiceSpy, createAuthServiceSpy } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';

describe('TaxaListComponent', () => {
  let component: TaxaListComponent;
  let fixture: ComponentFixture<TaxaListComponent>;

  let metadataHttpClientSpy: { get: jasmine.Spy };

  let metadataService: MetadataService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();

    metadataHttpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    metadataHttpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    metadataService = new MetadataService(<any>metadataHttpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        RouterModule
      ],
      declarations: [ TaxaListComponent ],
      providers: [
       { provide: OAuthService, useValue: createOAuthServiceSpy() },
       { provide: HttpClient, useValue: metadataHttpClientSpy },
       { provide: MetadataService, useValue: metadataService }
      ] 
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TaxaListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
