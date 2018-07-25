import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderOsCsvComponent } from './downloader-os-csv.component';

describe('DownloaderOsCsvComponent', () => {
  let component: DownloaderOsCsvComponent;
  let fixture: ComponentFixture<DownloaderOsCsvComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DownloaderOsCsvComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderOsCsvComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
