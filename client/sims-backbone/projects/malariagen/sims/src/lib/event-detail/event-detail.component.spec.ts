import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MockComponent } from 'ng-mocks';

import { EventDetailComponent } from './event-detail.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { LocationViewComponent } from '../location-view/location-view.component';
import { IndividualViewComponent } from '../individual-view/individual-view.component';
import { AttrTableComponent } from '../attr-table/attr-table.component';

describe('EventDetailComponent', () => {
  let component: EventDetailComponent;
  let fixture: ComponentFixture<EventDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FlexLayoutModule],
      declarations: [
        EventDetailComponent,
        MockComponent(AttrTableComponent),
        MockComponent(LocationViewComponent),
        MockComponent(IndividualViewComponent)
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
