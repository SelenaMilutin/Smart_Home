import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AppRoutingModule } from './infrastructure/app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { MaterialModule } from './infrastructure/material/material.module';
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from '@angular/material/form-field';
import { DatePipe } from '@angular/common';
import { LandingComponent } from './modules/landing/landing.component';
import { OnePiComponent } from './modules/one-pi/one-pi.component';
import { SocketIoModule, SocketIoConfig  } from 'ngx-socket-io';
import { ClockComponent } from './modules/clock/clock.component';
import { MatTimepickerModule } from 'mat-timepicker';

const config: SocketIoConfig = { url: 'http://localhost:5000', options: {} };

@NgModule({
  declarations: [
    AppComponent,
    LandingComponent,
    OnePiComponent,
    ClockComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    HttpClientModule,
    SocketIoModule.forRoot(config),
    MatTimepickerModule 
  ],
  providers: [
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: {
        appearance: 'outline'
      }
    },
    
    DatePipe
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
