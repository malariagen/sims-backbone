import { Component, OnInit } from '@angular/core';

import { OAuthService } from 'angular-oauth2-oidc';

import { Taxonomy } from '../typescript-angular-client/model/taxonomy';
import { Taxonomies } from '../typescript-angular-client/model/taxonomies';

import { MetadataService } from '../typescript-angular-client/api/metadata.service';

@Component({
  selector: 'app-taxa-list',
  providers: [MetadataService],
  templateUrl: './taxa-list.component.html',
  styleUrls: ['./taxa-list.component.scss']
})
export class TaxaListComponent implements OnInit {

  taxonomies: Taxonomy[];

  constructor(private metadataService: MetadataService, private oauthService: OAuthService) { }

  ngOnInit() {

    this.metadataService.getTaxonomyMetadata().subscribe(
      (taxas: Taxonomies) => {
        this.taxonomies = taxas.taxonomies;
      }
    );
  }

}
