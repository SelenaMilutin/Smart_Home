import { AfterViewInit, Component, OnInit } from '@angular/core';
import { PiService } from './modules/service/pi.service';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, AfterViewInit {
  title = 'Smart Home';
  alarm = false;
  alarmSystem = false;
  
  constructor(private readonly piService:PiService, 
    private readonly ngxSocket: Socket) {
      
  }

  ngOnInit(): void {
    this.ngxSocket.connect();
    
    // Listen for events from the server
    this.ngxSocket.on('alarm-socket', (data: any) => {
      console.log('Received data from server:', data);
      let decoded = JSON.parse(data)
      this.alarm = decoded['data'] == '1' ? true: false;
    });
  }
    
  ngAfterViewInit(): void {
    this.piService.getAlarmState().subscribe((res:any) => {
      this.alarm = res['data'] == '1' ? true: false;
    })
    this.piService.getAlarmSystemState().subscribe((res:any) => {
      console.log(res)
      this.alarmSystem = res['data'] == '1' ? true: false;
    })
  }

  alarmOff(): void {
    console.log("in app component")
    this.piService.putAlarmOff().subscribe((res: any) => {
        console.log(res)
        
    })
  }

}
