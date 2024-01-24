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
    "PI3": "http://localhost:3000/d/c475045d-357c-4b76-bf6e-2497d788bb963/iot-pi3?orgId=1&refresh=5s",
    "property": "http://localhost:3000/d/b5c9cf68-3d15-4b69-bbdd-d00c72f86be8/property?orgId=1&from=now-15m&to=now&refresh=5s"
  }

  public deviceNames: {[key: string]: string} = {
    "DS1": "Door Sensor (Button)",
    "DL": "Door Light (LED diode)",
    "DUS1": "Door Ultrasonic Sensor",
    "DB": "Door Buzzer",
    "DPIR1": "Door Motion Sensor",
    "DMS": "Door Membrane Switch",
    "RPIR1": "Room PIR",
    "RPIR2": "Room PIR",
    "RDHT1": "Room DHT", 
    "RDHT2": "Room DHT",
    "DS2":"Door sensor (Button)",
    "DUS2": "Door Ultrasonic Sensor",
    "DPIR2": "Door Motion Sensor",
    "GDHT": "Garage DHT",
    "GLCD": "Garage LCD",
    "GSG": "Gun Safe Gyro (Gyroscope)",
    "RPIR3": "Room PIR",
    "RDHT3": "Room DHT",
    "RPIR4": "Room PIR",
    "RDHT4": "Room DHT",
    "BB": "Bedroom buzzer",
    "B4SD": "Bedroom 4 Digit 7 Segment Display",
    "BIR": "Bedrom Infrared",
    "BRGB": "Bedroom RGB"
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
