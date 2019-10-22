import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlfStudyDetailComponent } from './alf-study-detail.component';
import { Component, Input } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActivatedRouteStub } from 'testing/activated-route-stub';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { AngularEditorModule } from '@kolkov/angular-editor';
import { MatCheckboxModule } from '@angular/material/checkbox';

@Component({
  selector: 'sims-study-edit',
  template: ''
})
export class StudyEditComponentStub {
}
@Component({
  selector: 'adf-content-metadata-card',
  template: ''
})
export class ContentMetadataComponentStub {
  @Input() preset;
  @Input() node;
  @Input() displayAspect;
}

describe('AlfStudyDetailComponent', () => {
  let component: AlfStudyDetailComponent;
  let fixture: ComponentFixture<AlfStudyDetailComponent>;

  let activatedRoute: ActivatedRouteStub;

  beforeEach(async(() => {

    activatedRoute = new ActivatedRouteStub();

    activatedRoute.setParamMap({
      studyCode: '0000'
    });

    TestBed.configureTestingModule({
      imports: [
        RouterModule,
        HttpClientModule,
        HttpClientTestingModule,
        FormsModule,
        ReactiveFormsModule,
        MatFormFieldModule,
        MatCheckboxModule,
        AngularEditorModule
      ],
      declarations: [
        AlfStudyDetailComponent,
        StudyEditComponentStub,
        ContentMetadataComponentStub
      ],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlfStudyDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
