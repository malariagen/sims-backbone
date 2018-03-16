import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudyEditComponent } from './study-edit.component';
import { ReactiveFormsModule, FormGroup } from '@angular/forms';
import { MatFormField } from '@angular/material';
import { Input, Component } from '@angular/core';
import { Taxonomy, StudyService, MetadataService } from '../typescript-angular-client';
import { RouterTestingModule } from '@angular/router/testing';
import { createAuthServiceSpy, asyncData, ActivatedRouteStub, createOAuthServiceSpy, ActivatedRoute } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient } from '@angular/common/http';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-taxonomy-edit',
  template: ''
})
export class TaxonomyEditComponentStub {

  @Input('group') group: FormGroup;

  @Input('taxonomies') taxonomies: Taxonomy[];
}

describe('StudyEditComponent', () => {
  let component: StudyEditComponent;
  let fixture: ComponentFixture<StudyEditComponent>;

  let activatedRoute: ActivatedRouteStub;

  let studyHttpClientSpy: { get: jasmine.Spy };

  let studyService: StudyService;
 
  let metadataHttpClientSpy: { get: jasmine.Spy };

  let metadataService: MetadataService;
 
  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub({ 
      studyCode: '0000'
     });

    let authService = createAuthServiceSpy();
    studyHttpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    studyHttpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    studyService = new StudyService(<any>studyHttpClientSpy, '', authService.getConfiguration());

    metadataHttpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    metadataHttpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    metadataService = new MetadataService(<any>metadataHttpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        RouterModule
      ],
      declarations: [ 
        StudyEditComponent,
        TaxonomyEditComponentStub,
        MatFormField
       ],
       providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: HttpClient, useValue: studyHttpClientSpy },
        { provide: StudyService, useValue: studyService },
        { provide: MetadataService, useValue: metadataService },
        { provide: ActivatedRoute, useValue: activatedRoute }
       ] 
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudyEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
