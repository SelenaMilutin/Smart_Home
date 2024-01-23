import { Component, OnInit } from '@angular/core';
import { PiService } from '../service/pi.service';
import Swal from 'sweetalert2';

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
      this.fireSwalToast(res['data'])
    })
  }

  setClock() {
    if (this.inputHour != -1 && this.inputMinute != -1) {
      this.piService.setClock(this.inputHour, this.inputMinute).subscribe((res: any) => {
        console.log(res)
        this.setResult = res['data']
        this.fireSwalToast(res['data'])
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

  private fireSwalToast(title: string): void {
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
      didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
      }
    })
    
    Toast.fire({
      icon: 'success',
      title: title
    })
  }

}
