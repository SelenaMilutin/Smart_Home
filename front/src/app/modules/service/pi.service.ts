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
  public panelLinks: { [key: string]: string } = {
    "PI1": "http://localhost:3000/d/c475045d-357c-4b76-bf6e-2497d788bb961/iot-pi1?orgId=1&refresh=5s",
    "PI2": "http://localhost:3000/d/c475045d-357c-4b76-bf6e-2497d788bb962/iot-pi2?orgId=1&refresh=5s",
    "PI3": "http://localhost:3000/d/c475045d-357c-4b76-bf6e-2497d788bb963/iot-pi3?orgId=1&refresh=5s"
  }

  setSelectedPi(name: string) {
    this.selectedDevice.next(name);
  }

  getComponents(piName: string): Observable<PiComponent[]> {
    return this.http.get<PiComponent[]>(environment.apiHost + `/component/${piName}`)
  }

  putAlarmOff(): Observable<any> {
    return this.http.put<any>(environment.apiHost + '/alarm-off', {})
  }

  getAlarmState(): Observable<any> {
    return this.http.get<any>(environment.apiHost + `/alarm-state`)
  }

  getAlarmSystemState(): Observable<any> {
    return this.http.get<any>(environment.apiHost + `/alarm-system-state`)
  }

  setClock(hour: number, minute: number) {
    return this.http.post<any>(environment.apiHost + '/clock', {'hour': hour, 'minute': minute})
  }

  setClockOff(reason: string) {
    return this.http.put<any>(environment.apiHost + '/clock-off', {'reason': reason})
  }

  getClock() {
    return this.http.get<any>(environment.apiHost + '/last-clock')
  }


  setRGB(val: string) {
    return this.http.put<any>(environment.apiHost + '/rgb', {'val': val})
  }

}
