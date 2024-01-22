import { Component, OnInit } from '@angular/core';
import { PI } from 'src/app/models/models';
import { PiService } from '../service/pi.service';
import { Router } from '@angular/router';
import { io } from "socket.io-client";
import { WebSocketService } from '../service/web-socket.service';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {


  pies: PI[] = [];

  constructor(
    private readonly piService: PiService,
    private router: Router,
    private readonly ngxSocket: Socket
  ) {}

  ngOnInit(): void {
    this.pies = this.loadPies()
    this.ngxSocket.connect();

    // Listen for events from the server
    this.ngxSocket.on('message_from_server', (data: any) => {
      console.log('Received data from server:', data);
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
}
