import { Component, Input } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Studies } from '../typescript-angular-client/model/studies';
import { Study } from '../typescript-angular-client/model/study';
import { StudyService } from '../typescript-angular-client/api/study.service';

@Component({
  selector: 'app-studies-list',
  providers: [StudyService],
  templateUrl: './studies-list.component.html',
  styleUrls: ['./studies-list.component.css']
})
export class StudiesListComponent {

  @Input()
  studies: Studies;
  

}
