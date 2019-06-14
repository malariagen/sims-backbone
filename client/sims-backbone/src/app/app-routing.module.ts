import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';



import { ReportsComponent } from './reports/reports.component';
import { AllStudiesListComponent } from '@malariagen/sims';
import { AllLocationsMapComponent, EventSetListComponent, EventSearchComponent, TaxaListComponent } from '@malariagen/sims';
import { ReportMissingDetailedLocationsComponent, ReportMissingLocationsComponent, ReportMissingTaxaComponent, ReportUncuratedLocationsComponent, ReportMultipleLocationGpsComponent, ReportMultipleLocationNamesComponent } from '@malariagen/sims';

const routes: Routes = [
  { path: '', redirectTo: '/studies', pathMatch: 'full' },
  { path: 'full-map', component: AllLocationsMapComponent },
  { path: 'studies', component: AllStudiesListComponent },
  {
    path: 'lib-experimental',
    loadChildren: () => import('@malariagen/sims').then(m => m.SimsModule)
  },
  { path: 'taxa', component: TaxaListComponent },
  { path: 'eventSets', component: EventSetListComponent },
  { path: 'search', component: EventSearchComponent },
  {
    path: 'reports', component: ReportsComponent,
    children: [
      { path: 'missingDetailedLocations', component: ReportMissingDetailedLocationsComponent },
      { path: 'missingLocations', component: ReportMissingLocationsComponent },
      { path: 'missingTaxa', component: ReportMissingTaxaComponent },
      { path: 'uncuratedLocations', component: ReportUncuratedLocationsComponent },
      { path: 'multipleLocationGPS', component: ReportMultipleLocationGpsComponent },
      { path: 'multipleLocationNames', component: ReportMultipleLocationNamesComponent }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
