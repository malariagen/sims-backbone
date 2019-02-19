import { Component, OnInit, Input } from '@angular/core';
import { IndividualService, Individual } from '../typescript-angular-client';

@Component({
  selector: 'app-individual-view',
  providers: [IndividualService],
  templateUrl: './individual-view.component.html',
  styleUrls: ['./individual-view.component.scss']
})
export class IndividualViewComponent implements OnInit {

  constructor(private individualService: IndividualService) { }

  individual: Individual;

  ngOnInit() {
  }

  @Input()
  set individualId(_individualId) {
    this.individualService.downloadIndividual(_individualId).subscribe(indiv => {
      this.individual = indiv;
    });
  }
}
