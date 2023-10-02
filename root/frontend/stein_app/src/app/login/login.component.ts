import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginResponse } from './login.interface';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  constructor(private http: HttpClient) {}

  username: string | undefined;
  password: string | undefined;

  async login() {
    this.http
      .post<LoginResponse>('http://localhost:3000/login', {
        username: this.username,
        password: this.password,
      })
      .subscribe({
        next: (response) => {
          console.log(response);
          sessionStorage.setItem('token', response.token);
          sessionStorage.setItem('expiry', response.expiry.toString());
        },
        error: (error) => {
          console.error(error);
          console.log(this.username);
          console.log(this.password);
        },
        complete: () => {
          console.log('complete');
        },
      });
  }
}
