import { TestBed, async } from '@angular/core/testing';

import { AppComponent } from './app.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule, MAT_MENU_DEFAULT_OPTIONS, MAT_MENU_SCROLL_STRATEGY } from '@angular/material/menu';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { Component } from '@angular/core';
import { of } from 'rxjs/observable/of';
import { MatIconRegistry } from '@angular/material/icon';

@Component({ selector: 'router-outlet', template: '' })
class RouterOutletStubComponent { }

describe('AppComponent', () => {
  let dialog: MatDialog;

  beforeEach(async(() => {

    // Create a fake AuthService object
    const authService = jasmine.createSpyObj('OAuthService', ['configure', 'setupAutomaticSilentRefresh', 'tryLogin']);
    // Make the spy return a synchronous Observable with the test data
    const configure = authService.configure.and.returnValue(of(undefined));
    const setupAutomaticSilentRefresh = authService.setupAutomaticSilentRefresh.and.returnValue(of(undefined));
    const tryLogin = authService.tryLogin.and.returnValue(of(undefined));

    TestBed.configureTestingModule({
      imports: [
        MatMenuModule,
        MatIconModule,
        MatToolbarModule,
        MatDialogModule
      ],
      declarations: [
        AppComponent,
        RouterOutletStubComponent
      ],
      providers: [
        MatIconRegistry,
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
/* Disabled until work out how to test translation
  it(`should have as title 'SIMS Backbone'`, async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    console.log(app);
    expect(app.title).toEqual('SIMS Backbone');
  }));
*/
});
