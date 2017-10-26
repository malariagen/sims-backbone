import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CsvDownloaderComponent } from './csv-downloader.component';

describe('CsvDownloaderComponent', () => {
  let component: CsvDownloaderComponent;
  let fixture: ComponentFixture<CsvDownloaderComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CsvDownloaderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CsvDownloaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
