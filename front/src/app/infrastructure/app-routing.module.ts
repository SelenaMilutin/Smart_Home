import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OnePiComponent } from '../modules/one-pi/one-pi.component';
import { LandingComponent } from '../modules/landing/landing.component';

const routes: Routes = [
  {path: "one-pi", component: OnePiComponent},
  {path: "**", component: LandingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
