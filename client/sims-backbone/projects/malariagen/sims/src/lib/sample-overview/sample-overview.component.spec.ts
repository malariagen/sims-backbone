import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MockComponent } from 'ng-mocks';
import { SampleOverviewComponent } from './sample-overview.component';
import { EventDetailComponent } from '../event-detail/event-detail.component';
import { DsDetailComponent } from '../ds-detail/ds-detail.component';
import { AdDetailComponent } from '../ad-detail/ad-detail.component';
import { OsDetailComponent } from '../os-detail/os-detail.component';

describe('SampleOverviewComponent', () => {
  let component: SampleOverviewComponent;
  let fixture: ComponentFixture<SampleOverviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ 
        SampleOverviewComponent,
        MockComponent(EventDetailComponent),
        MockComponent(OsDetailComponent),
        MockComponent(DsDetailComponent),
        MockComponent(AdDetailComponent)
       ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SampleOverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
