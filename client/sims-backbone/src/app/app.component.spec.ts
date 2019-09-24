import { TestBed, async } from '@angular/core/testing';

import { AppComponent } from './app.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule, MAT_MENU_DEFAULT_OPTIONS, MAT_MENU_SCROLL_STRATEGY } from '@angular/material/menu';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

import { Component, Injectable, Pipe, PipeTransform } from '@angular/core';
import { of } from 'rxjs/observable/of';
import { MatIconRegistry } from '@angular/material/icon';
import { TranslateModule, TranslateService, TranslatePipe, TranslateLoader } from '@ngx-translate/core';
import { Observable } from 'rxjs/Observable';

const translations: any = {
};

class FakeLoader implements TranslateLoader {
  getTranslation(lang: string): Observable<any> {
    return of(translations);
  }
}

@Pipe({
  name: 'translate'
})
export class TranslatePipeMock implements PipeTransform {
  public name = 'translate';

  public transform(query: string, ...args: any[]): any {
    return query;
  }
}

@Injectable()
export class TranslateServiceStub {
  public get<T>(key: T): Observable<T> {
    return of(key);
  }
  public setDefaultLang(lang: string) {

  }
}


@Component({ selector: 'router-outlet', template: '' })
class RouterOutletStubComponent { }


describe('AppComponent', () => {
  let dialog: MatDialog;

  beforeEach(async(() => {

    // Create a fake AuthService object 
    const authService = jasmine.createSpyObj('OAuthService', ['configure', 'setupAutomaticSilentRefresh', 'tryLogin']);
    // Make the spy return a synchronous Observable with the test data
    let configure = authService.configure.and.returnValue(of(undefined));
    let setupAutomaticSilentRefresh = authService.setupAutomaticSilentRefresh.and.returnValue(of(undefined));
    let tryLogin = authService.tryLogin.and.returnValue(of(undefined));

    TestBed.configureTestingModule({
      imports: [
        MatMenuModule,
        MatIconModule,
        MatToolbarModule,
        MatDialogModule,
        TranslateModule.forRoot({
          loader: { provide: FakeLoader }
        })
      ],
      declarations: [
        AppComponent,
        RouterOutletStubComponent,
        TranslatePipeMock
      ],
      providers: [
        MatIconRegistry,
        { provide: TranslateService, useClass: TranslateServiceStub },
        { provide: TranslatePipe, useClass: TranslatePipeMock },
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
    expect(app.title).toEqual('sims.menu.title');
  }));

  it('should render title in a span tag', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('#title').textContent).toContain(fixture.componentInstance.title);
  }));
});
