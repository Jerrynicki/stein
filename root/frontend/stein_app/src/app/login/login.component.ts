import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoginResponse, LoginStatus } from './login.interface';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  constructor(private http: HttpClient, private router: Router) {}

  hide = true;
  color: ThemePalette = 'warn';
  mode: ProgressSpinnerMode = 'indeterminate';
  value = 50;
  diameter = 50;

  loginstatus: LoginStatus = LoginStatus.Initial;
  attempts: number = 0;

  username: string | undefined;
  password: string | undefined;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer' + sessionStorage.getItem('token'),
    }),
  };

  async login() {
    this.attempts++;
    this.loginstatus = LoginStatus.Loading;
    this.http
      .post<LoginResponse>(
        'http://127.0.0.1:5000/api/login',
        {
          username: this.username,
          password: this.password,
        },
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          if (this.username) {
            sessionStorage.setItem('token', response.token);
            sessionStorage.setItem('expiry', this.expiretime(response.expiry));
            sessionStorage.setItem('loginName', this.username);
          }
        },
        error: (error) => {
          console.error(error);
          if (error.status === 403) {
            this.loginstatus = LoginStatus.Fail;
          } else {
            this.loginstatus = LoginStatus.Error;
          }
        },
        complete: () => {
          console.log('login complete');
          this.loginstatus = LoginStatus.Success;
          this.router.navigate(['/profile', this.username]);
        },
      });
  }

  expiretime(expiry: number) {
    return new Date(Date.now() + expiry * 1000).toString();
  }
}
