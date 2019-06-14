import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetEditDialogComponent } from './event-set-edit-dialog.component';
import { FormsModule } from '@angular/forms';
import { MatAutocomplete, MatDialogModule, MatAutocompleteTrigger, MatFormField, MatOption, MatPseudoCheckbox, MatRippleModule, MatDialogRef, MAT_DIALOG_DATA, MAT_AUTOCOMPLETE_SCROLL_STRATEGY, MatSelectModule, MatAutocompleteModule, MatInputModule } from '@angular/material';
import { of } from 'rxjs/observable/of';
import { OAuthService } from 'angular-oauth2-oidc';
import { createAuthServiceSpy, createOAuthServiceSpy, asyncData } from '../../testing/index.spec';
import { HttpClient } from '@angular/common/http';
import { EventSetService } from '../typescript-angular-client';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';

describe('EventSetEditDialogComponent', () => {
  let component: EventSetEditDialogComponent;
  let fixture: ComponentFixture<EventSetEditDialogComponent>;

  let httpClientSpy: { get: jasmine.Spy };

  let eventSetService: EventSetService;

  beforeEach(async(() => {

    let authService = createAuthServiceSpy();
    httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);

    httpClientSpy.get.and.returnValue(asyncData({ count: 0, locations: [] }));

    eventSetService = new EventSetService(<any>httpClientSpy, '', authService.getConfiguration());

    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        MatDialogModule,
        MatRippleModule,
        MatSelectModule,
        MatInputModule,
        NoopAnimationsModule
      ],
      declarations: [
        EventSetEditDialogComponent,
        MatAutocomplete,
        MatAutocompleteTrigger
      ],
      providers: [
        { provide: OAuthService, useValue: createOAuthServiceSpy() },
        { provide: HttpClient, useValue: httpClientSpy },
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: MatDialogRef, useValue: {} },
        { provide: EventSetService, useValue: eventSetService },
        { provide: MAT_AUTOCOMPLETE_SCROLL_STRATEGY, useValue: {} }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetEditDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
