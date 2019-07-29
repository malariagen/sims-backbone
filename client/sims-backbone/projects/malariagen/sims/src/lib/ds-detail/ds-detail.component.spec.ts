import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { DsDetailComponent } from './ds-detail.component';
import { MockComponent } from 'ng-mocks';
import { AttrTableComponent } from '../attr-table/attr-table.component';

describe('DsDetailComponent', () => {
  let component: DsDetailComponent;
  let fixture: ComponentFixture<DsDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [
        DsDetailComponent,
        MockComponent(AttrTableComponent)
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DsDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
