import { Component, OnInit } from '@angular/core';
import { PI } from 'src/app/models/models';
import { PiService } from '../service/pi.service';
import { Router } from '@angular/router';
import * as io from 'socket.io-client';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css']
})
export class LandingComponent implements OnInit {

  private socket: any;

  pies: PI[] = []

  constructor(private readonly piService:PiService,
    private router: Router) { 
      
    }

  ngOnInit(): void {
    this.pies = this.loadPies()
    
  }

  loadPies(): PI[] {
    return [
      {name: "PI1"}, 
      {name: "PI2"}, 
      {name: "PI3"}
    ]
  }

  navigateToPiDevices(pi: PI) {
    this.piService.setSelectedPi(pi.name);
    this.router.navigate(['/one-pi'])
    }

}
