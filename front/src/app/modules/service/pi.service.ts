import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { PiComponent } from 'src/app/models/models';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PiService {
  
  constructor(private readonly http: HttpClient) { }
  
  private selectedDevice = new BehaviorSubject<string>("");
  selectedDeviceId$ = this.selectedDevice.asObservable();

  setSelectedPi(name: string) {
    this.selectedDevice.next(name);
  }

  getComponents(piName: string): Observable<PiComponent[]> {
    return this.http.get<PiComponent[]>(environment.apiHost + `/component/${piName}`)
  }

}
