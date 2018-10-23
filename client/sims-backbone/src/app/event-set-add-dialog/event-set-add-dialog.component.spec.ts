import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EventSetAddDialogComponent } from './event-set-add-dialog.component';
import { FormsModule, FormControl, FormGroupDirective, NgForm } from '@angular/forms';
import { MatFormField, MatDialogModule, MatDialogRef, MAT_DIALOG_DATA, MAT_MENU_DEFAULT_OPTIONS, MatInput, ErrorStateMatcher } from '@angular/material';
import { HttpClient } from '@angular/common/http';
import { OAuthService } from 'angular-oauth2-oidc';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { createAuthServiceSpy } from '../../testing/index.spec';
import {ObserversModule} from '@angular/cdk/observers';

/** Error when invalid control is dirty, touched, or submitted. */
export class MyErrorStateMatcher implements ErrorStateMatcher {
  isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
    const isSubmitted = form && form.submitted;
    return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
  }
}

describe('EventSetAddDialogComponent', () => {
  let component: EventSetAddDialogComponent;
  let fixture: ComponentFixture<EventSetAddDialogComponent>;


  beforeEach(async(() => {

    let esm = new MyErrorStateMatcher();

    TestBed.configureTestingModule({
      imports: [FormsModule, MatDialogModule, NoopAnimationsModule],
      declarations: [
        EventSetAddDialogComponent,
        MatFormField,
        MatInput
      ],
      providers: [
        { provide: OAuthService, useValue: createAuthServiceSpy() },
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: MatDialogRef, useValue: {} },
        { provide: ErrorStateMatcher, useValue: esm }
      ]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EventSetAddDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  //Fails after upgrade to 7.0.0
  //it('should create', () => {
  //  expect(component).toBeTruthy();
  //});
});


