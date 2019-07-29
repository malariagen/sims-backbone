import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AdDetailComponent } from './ad-detail.component';
import { MockComponent } from 'ng-mocks';
import { AttrTableComponent } from '../attr-table/attr-table.component';

describe('AdDetailComponent', () => {
  let component: AdDetailComponent;
  let fixture: ComponentFixture<AdDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [
        AdDetailComponent,
        MockComponent(AttrTableComponent)
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
