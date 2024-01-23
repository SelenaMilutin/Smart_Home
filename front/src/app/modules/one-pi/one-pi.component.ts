import { Component, OnInit } from '@angular/core';
import { PiService } from '../service/pi.service';
import { PiComponent } from 'src/app/models/models';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-one-pi',
  templateUrl: './one-pi.component.html',
  styleUrls: ['./one-pi.component.css']
})
export class OnePiComponent implements OnInit {
  piName: string = ''
  components: PiComponent[] = []
  rgbResult: string = ''

  colorDict: Record<string, string> = {
    '2': 'green',
    '3': 'blue',
    '4': ' yellow',
    '5': 'purple',
    '6': 'light blue',
    '7': 'white',
    '8': 'red'
  }
  colorList: { key: string, value: string }[] = Object.entries(this.colorDict).map(([key, value]) => ({ key, value }));


  constructor(private readonly piService:PiService,
    private sanitizer: DomSanitizer) { 
    this.piService.selectedDeviceId$.subscribe((res: string) => {
      this.piName = res;
      console.log(this.piName)
    })
  }

  ngOnInit(): void {
    this.piService.getComponents(this.piName).subscribe((res: any) => {
      console.log("AAAAAAA")
      console.log(res)
      this.components = res;
    })
  }

  getSanitizedUrl(): SafeResourceUrl {
    // const url = 'http://localhost:3000/d/e1deea5f-5dc6-4647-b974-d04ef94fd431/iot?orgId=1&refresh=10s';
    const url = this.piService.panelLinks[this.piName]
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  setRGB(val: string) {
    console.log(val)
    this.piService.setRGB(val).subscribe((res: any) => {
      this.rgbResult = res['data'];
      this.fireSwalToast(res['data']);
    })
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
