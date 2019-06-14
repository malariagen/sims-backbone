import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-taxa-ds-list',
  templateUrl: './taxa-ds-list.component.html',
  styleUrls: ['./taxa-ds-list.component.scss']
})
export class TaxaDsListComponent implements OnInit {

  taxaId: string;
  
  filter: string;

  downloadFileName: string;

  jsonDownloadFileName: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.taxaId = pmap.get('taxaId');
    });
    this.filter = 'taxa:' + this.taxaId;
    this.downloadFileName = 'derivative_samples_taxa_' + this.taxaId + '.csv';
    this.jsonDownloadFileName = 'derivative_samples_taxa_' + this.taxaId + '.json';
  }
}
