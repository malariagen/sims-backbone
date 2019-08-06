import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { StudyEditComponent } from './study-edit.component';
import { ReactiveFormsModule } from '@angular/forms';
import { MatFormField } from '@angular/material/form-field';
import { Taxonomy, Study, PartnerSpecies, Taxonomies } from '../typescript-angular-client';
import { createAuthServiceSpy, ActivatedRouteStub, createOAuthServiceSpy, ActivatedRoute } from '../../testing/index.spec';
import { OAuthService } from 'angular-oauth2-oidc';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';
import {ObserversModule} from '@angular/cdk/observers';
import { MockComponent } from 'ng-mocks';
import { TaxonomyEditComponent } from '../taxonomy-edit/taxonomy-edit.component';

describe('StudyEditComponent', () => {
  let component: StudyEditComponent;
  let fixture: ComponentFixture<StudyEditComponent>;

  let activatedRoute: ActivatedRouteStub;

  let httpClient: HttpClient;

  let httpTestingController: HttpTestingController;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      studyCode: '0000'
    });

    const authService = createAuthServiceSpy();

    TestBed.configureTestingModule({
      imports: [
        ReactiveFormsModule,
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
        ObserversModule
      ],
      declarations: [
        StudyEditComponent,
        MockComponent(TaxonomyEditComponent),
        MatFormField
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: ActivatedRoute, useValue: activatedRoute }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {

    // Inject the http service and test controller for each test
    httpClient = TestBed.get(HttpClient);
    httpTestingController = TestBed.get(HttpTestingController);

    fixture = TestBed.createComponent(StudyEditComponent);
    component = fixture.componentInstance;

    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should populate edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const taxas: Taxonomies = <Taxonomies>{
        'count': 2,
        'taxonomies': [
          {
            'name': 'gambiae species complex',
            'rank': 'None',
            'taxonomy_id': 44542
          },
          {
            'name': 'Anopheles gambiae',
            'rank': 'species',
            'taxonomy_id': 7165
          }
        ]
      };

      const req_taxas = backend.expectOne({
        url: 'http://localhost/v1/metadata/taxonomy',
        method: 'GET'
      });

      req_taxas.flush(taxas);

      const testData: Study = <Study>{
        name: '0000 TestStudy',
        code: '0000',
        partner_species: [<PartnerSpecies>{
          partner_species: 'AG',
          taxa: [<Taxonomy>{
            taxonomy_id: 1234,
            name: 'Anonpheles',
            rank: ''
          }]
        }]
      };

      const req = backend.expectOne({
        url: 'http://localhost/v1/study/' + testData.code,
        method: 'GET'
      });

      req.flush(testData);

      // Finally, assert that there are no outstanding requests.
      // backend.verify();
      expect(component.studyForm.controls['name'].value).toBe(testData.name);
    })
  )
  );

  it('should save edit form', async(inject([HttpClient, HttpTestingController],
    (http: HttpClient, backend: HttpTestingController) => {

      const taxas: Taxonomies = <Taxonomies>{
        'count': 2,
        'taxonomies': [
          {
            'name': 'gambiae species complex',
            'rank': 'None',
            'taxonomy_id': 44542
          },
          {
            'name': 'Anopheles gambiae',
            'rank': 'species',
            'taxonomy_id': 7165
          }
        ]
      };

      const req_taxas = backend.expectOne({
        url: 'http://localhost/v1/metadata/taxonomy',
        method: 'GET'
      });

      req_taxas.flush(taxas);

      const testData: Study = <Study>{
        name: '0000 TestStudy',
        code: '0000',
        partner_species: [<PartnerSpecies>{
          partner_species: 'AG',
          taxa: [<Taxonomy>{
            taxonomy_id: 1234,
            name: 'Anonpheles',
            rank: ''
          }]
        }]
      };

      const req = backend.expectOne({
        url: 'http://localhost/v1/study/' + testData.code,
        method: 'GET'
      });

      req.flush(testData);

      backend.verify();

      testData.name = '0001 updated name';
      testData.code = '0001';

      component.studyForm.controls['name'].setValue(testData.name);
      component.studyForm.controls['code'].setValue(testData.code);


      expect(component.studyForm.valid).toBeTruthy();

      component.onSubmit({
        value: component.studyForm.value,
        valid: component.studyForm.valid
      });

      const put = backend.expectOne({
        url: 'http://localhost/v1/study/' + testData.code,
        method: 'PUT'
      });

      // The response to the put request
      put.flush(testData);

      expect(put.request.body.name).toBe(testData.name);
      expect(put.request.body.code).toBe(testData.code);

      const arrayControls = put.request.body.partner_species[0].taxa;
      expect(arrayControls[0].taxonomy_id).toBe(testData.partner_species[0].taxa[0].taxonomy_id);

      backend.verify();
    })
  )
  );
});
