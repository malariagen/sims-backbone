import { Component, OnInit, Input } from '@angular/core';
import { IndividualService, Individual } from '../typescript-angular-client';

@Component({
  selector: 'app-individual-view',
  providers: [IndividualService]
  templateUrl: './individual-view.component.html',
  styleUrls: ['./individual-view.component.scss']
})
export class IndividualViewComponent implements OnInit {

  constructor(private individualService: IndividualService) { }

  individual: Individual;

  ngOnInit() {
  }

  @Input()
  set individual_id(_individual_id) {
    this.individualService.downloadIndividual(_individual_id).subscribe(indiv => {
      this.individual = indiv;
    });
  }
}
