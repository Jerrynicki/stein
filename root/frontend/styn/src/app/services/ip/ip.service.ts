import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class IpService {
  constructor(private http: HttpClient) {}

  // returns the IP address of the user in JSON format
  // TODO: add error handling
  // TODO: return the IP address as a string
  getIP(): Observable<any> {
    return this.http.get('https://api.ipify.org?format=json');
  }

  // checks if the IP address is banned
  // TODO: implement
  checkIPban(ip: string): boolean {
    return true;
  }
}
