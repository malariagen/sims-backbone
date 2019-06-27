import { Component, OnInit, Input } from '@angular/core';
import { Individual } from '../typescript-angular-client';
import { IndividualService } from '../typescript-angular-client/api/individual.service';

@Component({
  selector: 'sims-individual-view',
  providers: [IndividualService],
  templateUrl: './individual-view.component.html',
  styleUrls: ['./individual-view.component.scss']
})
export class IndividualViewComponent implements OnInit {

  @Input()
  set individualId(_individualId) {
    this.individualService.downloadIndividual(_individualId).subscribe(indiv => {
      this.individual = indiv;
    });
  }

  individual: Individual;

  constructor(private individualService: IndividualService) { }

  ngOnInit() {
  }
}
