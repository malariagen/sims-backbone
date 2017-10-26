import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';
import { LocationEditComponent } from './location-edit/location-edit.component';
import { StudyEventListComponent } from './study-event-list/study-event-list.component';

const routes: Routes = [
  { path: '', redirectTo: '/full-map', pathMatch: 'full' },
  { path: 'full-map', component: AllLocationsMapComponent },
  { path: 'location/:latitude/:longitude', component: LocationEditComponent},
  { path: 'study/events/:studyName', component: StudyEventListComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
