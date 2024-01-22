import { Component, OnInit, ViewChild } from '@angular/core';
import { PiService } from '../service/pi.service';
import { PiComponent } from 'src/app/models/models';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort, Sort } from '@angular/material/sort';
import {LiveAnnouncer} from '@angular/cdk/a11y';
import { Socket } from 'ngx-socket-io';


@Component({
  selector: 'app-one-pi',
  templateUrl: './one-pi.component.html',
  styleUrls: ['./one-pi.component.css']
})
export class OnePiComponent implements OnInit {
  piName: string = ''
  
  components: PiComponent[] = []
  displayedColumns: string[] = ['code', 'name', 'simulated', 'measurement', 'runsOn'];
  dataSource!: MatTableDataSource<PiComponent>;
  temperature = 22
  hummidity = 18

  constructor(private readonly piService:PiService,
    private sanitizer: DomSanitizer,
    private _liveAnnouncer: LiveAnnouncer,
    private readonly ngxSocket: Socket,) { 
    this.piService.selectedDeviceId$.subscribe((res: string) => {
      this.piName = res;
      console.log(this.piName)
    })
  }
  @ViewChild(MatSort)
  sort!: MatSort;

  

  ngOnInit(): void {
    this.piService.getComponents(this.piName).subscribe((res: any) => {
      console.log("AAAAAAA")
      console.log(res)
      this.components = res;
      this.dataSource = new MatTableDataSource<PiComponent>(this.components);
      this.dataSource.sort = this.sort;
    })

    if (this.piName == "PI2"){
      this.ngxSocket.on('lcd', (data: any) => {
        console.log('Received data from server:', data);
      });
    }
  }

  // ngAfterViewInit() {
  //   this.dataSource.sort = this.sort;
  // }

  getSanitizedUrl(): SafeResourceUrl {
    // const url = 'http://localhost:3000/d/e1deea5f-5dc6-4647-b974-d04ef94fd431/iot?orgId=1&refresh=10s';
    const url = this.piService.panelLinks[this.piName]
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }

  announceSortChange(sortState: Sort) {
    // This example uses English messages. If your application supports
    // multiple language, you would internationalize these strings.
    // Furthermore, you can customize the message to add additional
    // details about the values being sorted.
    if (sortState.direction) {
      this._liveAnnouncer.announce(`Sorted ${sortState.direction}ending`);
    } else {
      this._liveAnnouncer.announce('Sorting cleared');
    }
  }

  getName(code: string): string {
    return this.piService.deviceNames[code]
  }

}
