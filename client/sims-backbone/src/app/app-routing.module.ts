import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AllLocationsMapComponent } from './all-locations-map/all-locations-map.component';

const routes: Routes = [
  { path: '', redirectTo: '/full-map', pathMatch: 'full' },
  { path: 'full-map', component: AllLocationsMapComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
