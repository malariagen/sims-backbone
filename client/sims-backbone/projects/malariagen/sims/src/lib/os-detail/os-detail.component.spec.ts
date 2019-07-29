import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { OsDetailComponent } from './os-detail.component';
import { AttrTableComponent } from '../attr-table/attr-table.component';
import { MockComponent } from 'ng-mocks';

describe('OsDetailComponent', () => {
  let component: OsDetailComponent;
  let fixture: ComponentFixture<OsDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [ 
        OsDetailComponent,
        MockComponent(AttrTableComponent) ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OsDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
