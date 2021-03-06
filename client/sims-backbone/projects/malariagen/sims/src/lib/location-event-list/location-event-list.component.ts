import { Component, OnInit } from '@angular/core';

import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'sims-location-event-list',
  templateUrl: './location-event-list.component.html',
  styleUrls: ['./location-event-list.component.css']
})

export class LocationEventListComponent implements OnInit {

  locationId: string;

  filter: string;

  constructor(private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.paramMap.subscribe(pmap => {
      this.locationId = pmap.get('locationId');
    });
    this.filter = 'location:' + this.locationId;
  }
}
