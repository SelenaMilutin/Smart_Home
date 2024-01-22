import { Component } from '@angular/core';
import { PiService } from './modules/service/pi.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'front';

  constructor(private readonly piService:PiService) {
    
  }

  alarmOff(): void {
    console.log("in app component")
    this.piService.putAlarmOff().subscribe((res: any) => {
        console.log(res)
    })
  }

}
