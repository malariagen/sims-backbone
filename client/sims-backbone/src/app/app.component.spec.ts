import { TestBed, async } from '@angular/core/testing';

import { AppComponent } from './app.component';
import { OAuthService } from 'angular-oauth2-oidc';
import { MatIcon, MatMenu, MatToolbar, MatButton, MatMenuModule, MatRipple, MatDialogModule, MAT_MENU_DEFAULT_OPTIONS, MatMenuTrigger, MAT_MENU_SCROLL_STRATEGY } from '@angular/material';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';

import { Component } from '@angular/core';
import { of } from 'rxjs/observable/of';
import { MatIconRegistry } from '@angular/material/icon';


@Component({ selector: 'router-outlet', template: '' })
class RouterOutletStubComponent { }


describe('AppComponent', () => {
  let oauthService: OAuthService;
  let dialog: MatDialog;

  beforeEach(async(() => {

    // Create a fake AuthService object 
    const authService = jasmine.createSpyObj('OAuthService', ['configure', 'setupAutomaticSilentRefresh', 'tryLogin']);
    // Make the spy return a synchronous Observable with the test data
    let configure = authService.configure.and.returnValue(of(undefined));
    let setupAutomaticSilentRefresh = authService.setupAutomaticSilentRefresh.and.returnValue(of(undefined));
    let tryLogin = authService.tryLogin.and.returnValue(of(undefined));

    TestBed.configureTestingModule({
      imports: [MatDialogModule],
      declarations: [
        AppComponent,
        MatIcon,
        MatMenu,
        MatMenuTrigger,
        MatButton,
        MatToolbar,
        MatRipple,
        RouterOutletStubComponent
      ],
      providers: [
        MatIconRegistry,
        { provide: OAuthService, useValue: authService },
        { provide: MAT_DIALOG_DATA, useValue: {} },
        { provide: MatDialogRef, useValue: {} },
        { provide: MAT_MENU_DEFAULT_OPTIONS, useValue: {} },
        { provide: MAT_MENU_SCROLL_STRATEGY, useValue: {} }
      ]
    }).compileComponents();
  }));

  it('should create the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));

  it(`should have as title 'SIMS Backbone'`, async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('SIMS Backbone');
  }));

  it('should render title in a span tag', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#title').textContent).toContain(fixture.componentInstance.title);
  }));
});
