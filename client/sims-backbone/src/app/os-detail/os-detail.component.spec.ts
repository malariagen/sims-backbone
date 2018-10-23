import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { OsDetailComponent } from './os-detail.component';

describe('OsDetailComponent', () => {
  let component: OsDetailComponent;
  let fixture: ComponentFixture<OsDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OsDetailComponent ]
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
