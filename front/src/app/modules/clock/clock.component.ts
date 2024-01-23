import { Component, OnInit } from '@angular/core';
import { PiService } from '../service/pi.service';

@Component({
  selector: 'app-clock',
  templateUrl: './clock.component.html',
  styleUrls: ['./clock.component.css']
})
export class ClockComponent implements OnInit {

  constructor(private readonly piService: PiService ) { }

  hour = '-1'
  minute = '1'
  inputHour: number = -1
  inputMinute: number = -1

  setResult = ""
  offResult = ""

  ngOnInit(): void {
    this.piService.getClock().subscribe((res: any) => {
      console.log(res)
      if (res['data']['hour'] != -1) {
        this.hour = this.pad(res['data']['hour'])
        this.minute = this.pad(res['data']['minute'])
      } 
    })
  }

  timeChangeHandler(event: any) {
    this.inputHour = event.getHours();
    this.inputMinute = event.getMinutes();
  }

  turnOff() {
    let currentDate = new Date()
    let reason =  (currentDate.getHours() === parseInt(this.hour) && currentDate.getMinutes() === parseInt(this.minute) )? "off" : "cancel"
    this.piService.setClockOff(reason).subscribe((res: any) => {
      console.log(res)
      this.offResult = res['data']
    })
  }

  setClock() {
    if (this.inputHour != -1 && this.inputMinute != -1) {
      this.piService.setClock(this.inputHour, this.inputMinute).subscribe((res: any) => {
        console.log(res)
        this.setResult = res['data']
      })
    }
  }

  pad(num: number) {
    if (num < 10) {
      return "0" + num.toString()
    } else {
      return num.toString()
    }
  }

}
