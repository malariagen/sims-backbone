import { Injectable } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';



@Injectable({
    providedIn: 'root'
})
export class TranslationService {
    defaultLang: string;
    userLang: string;

    constructor(public translate: TranslateService) {
        
        this.defaultLang = 'en';
        translate.setDefaultLang(this.defaultLang);
        
    }
}