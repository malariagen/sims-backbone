import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-taxa-os-list',
  templateUrl: './taxa-os-list.component.html',
  styleUrls: ['./taxa-os-list.component.scss']
})
export class TaxaOsListComponent implements OnInit {

  downloadFileName: string;

  jsonDownloadFileName: string;

  taxaId: string;

  filter: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.taxaId = pmap.get('taxaId');
    });
    this.filter = 'taxa:' + this.taxaId;
    this.downloadFileName = 'originalSamples_taxa_' + this.taxaId + '.csv';
    this.jsonDownloadFileName =  'originalSamples_taxa_' + this.taxaId + '.json';
  }
}
