import { Component, OnInit } from '@angular/core';
import { PI } from 'src/app/models/models';
import { PiService } from '../service/pi.service';
import { Router } from '@angular/router';
import { io } from "socket.io-client";
import { WebSocketService } from '../service/web-socket.service';
import { Socket } from 'ngx-socket-io';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  peopleNum: number = 0;
  isAlarmOn: boolean = false;
  deviceName: string = '';

  pies: PI[] = [];

  constructor(
    private readonly piService: PiService,
    private router: Router,
    private readonly ngxSocket: Socket,
    private sanitizer: DomSanitizer,
  ) {}

  ngOnInit(): void {
    this.pies = this.loadPies()
    this.ngxSocket.connect();

    // Listen for events from the server
    this.ngxSocket.on('message_from_server', (data: any) => {
      console.log('Received data from server:', data);
    });

    this.ngxSocket.on('updated_data', (data: any) => {
      console.log('Received data from updated_data:', data["data"]["people_num"]);
      this.peopleNum = data["data"]["people_num"]
    });

    this.ngxSocket.on('alarm', (data: any) => {
      console.log('Received data from alarm:', data["data"]);
    });

  
  }

  sendMessage() {
    this.ngxSocket.emit('message_from_client', { message: 'Hello, from angular!' });
    
  }

  loadPies(): PI[] {
    return [
      { name: "PI1" },
      { name: "PI2" },
      { name: "PI3" }
    ];
  }

  navigateToPiDevices(pi: PI) {
    this.piService.setSelectedPi(pi.name);
    this.router.navigate(['/one-pi']);
  }

  getSanitizedUrl(): SafeResourceUrl {
    // const url = 'http://localhost:3000/d/e1deea5f-5dc6-4647-b974-d04ef94fd431/iot?orgId=1&refresh=10s';
    const url = this.piService.panelLinks["property"]
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
