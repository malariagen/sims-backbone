import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FlexLayoutModule } from '@angular/flex-layout';

import { IndividualViewComponent } from './individual-view.component';
import { HttpClientModule } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { MockComponent } from 'ng-mocks';
import { AttrTableComponent } from '../attr-table/attr-table.component';

describe('IndividualViewComponent', () => {
  let component: IndividualViewComponent;
  let fixture: ComponentFixture<IndividualViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FlexLayoutModule,
        HttpClientModule,
        HttpClientTestingModule,
      ],
      declarations: [
        IndividualViewComponent,
        MockComponent(AttrTableComponent)
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IndividualViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
