import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DownloaderOsJsonComponent } from './downloader-os-json.component';

describe('DownloaderOsJsonComponent', () => {
  let component: DownloaderOsJsonComponent;
  let fixture: ComponentFixture<DownloaderOsJsonComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DownloaderOsJsonComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DownloaderOsJsonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
