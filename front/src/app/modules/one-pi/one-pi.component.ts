import { Component, OnInit } from '@angular/core';
import { PiService } from '../service/pi.service';
import { PiComponent } from 'src/app/models/models';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-one-pi',
  templateUrl: './one-pi.component.html',
  styleUrls: ['./one-pi.component.css']
})
export class OnePiComponent implements OnInit {
  piName: string = ''
  components: PiComponent[] = []

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

}
