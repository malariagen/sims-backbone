import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AlfStudyDetailComponent } from './alf-study-detail.component';
import { Component, Input, Pipe, PipeTransform, Injectable } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ActivatedRouteStub } from 'testing/activated-route-stub';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TranslateLoader, TranslateModule, TranslateService, TranslatePipe } from '@ngx-translate/core';
import { Observable, of } from 'rxjs';
import { MatFormFieldModule } from '@angular/material/form-field';

const translations: any = {
};

class FakeLoader implements TranslateLoader {
  getTranslation(lang: string): Observable<any> {
    return of(translations);
  }
}

@Pipe({
  name: 'translate'
})
export class TranslatePipeMock implements PipeTransform {
  public name = 'translate';

  public transform(query: string, ...args: any[]): any {
    return query;
  }
}

@Injectable()
export class TranslateServiceStub {
  public get<T>(key: T): Observable<T> {
    return of(key);
  }
  public setDefaultLang(lang: string) {

  }
}

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
        TranslateModule.forRoot({
          loader: { provide: FakeLoader }
        })
      ],
      declarations: [ 
        AlfStudyDetailComponent,
        StudyEditComponentStub,
        ContentMetadataComponentStub
      ],
      providers: [
        { provide: ActivatedRoute, useValue: activatedRoute },
        { provide: TranslateService, useClass: TranslateServiceStub },
        { provide: TranslatePipe, useClass: TranslatePipeMock }
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
