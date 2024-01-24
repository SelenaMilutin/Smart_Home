import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OnePiComponent } from '../modules/one-pi/one-pi.component';
import { LandingComponent } from '../modules/landing/landing.component';
import { ClockComponent } from '../modules/clock/clock.component';

const routes: Routes = [
  {path: "one-pi", component: OnePiComponent},
  {path: "clock", component: ClockComponent},
  {path: "**", component: LandingComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
