import { Component, OnInit } from '@angular/core';
import { RegisterResponse, RegisterStatus } from './register.interface';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss'],
})
export class RegistrationComponent implements OnInit {
  constructor(private http: HttpClient) {}
  ngOnInit(): void {
    this.http.get('http://localhost:3000/teams').subscribe({
      next: (response) => {
        this.teams = response;
      },
      error: (error) => {
        console.error(error);
      },
      complete: () => {
        console.log('complete');
      },
  });
  }

  hide = true;
  color: ThemePalette = 'warn';
  mode: ProgressSpinnerMode = 'indeterminate';
  value = 50;
  diameter = 50;

  registerstatus: RegisterStatus = RegisterStatus.Initial;
  attempts: number = 0;
  teams: any = [];

  team: number | undefined;
  password: string | undefined;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + sessionStorage.getItem('token'),
    }),
  };

  async register() {
    this.attempts++;
    this.registerstatus = RegisterStatus.Loading;
    this.http
      .post<RegisterResponse>(
        'http://localhost:3000/register',
        {
          team: this.team,
          password: this.password,
        },
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          sessionStorage.setItem('token', response.token);
          sessionStorage.setItem('expiry', this.expiretime(response.expiry));
          sessionStorage.setItem('loginName', response.username);
        },
        error: (error) => {
          console.error(error);
          if (error.status === 429) {
            this.registerstatus = RegisterStatus.Fail;
          } else {
            this.registerstatus = RegisterStatus.Error;
          }
        },
        complete: () => {
          console.log('login complete');
          this.registerstatus = RegisterStatus.Success;
        },
      });
  }

  expiretime(expiry: number) {
    return new Date(Date.now() + expiry * 1000).toString();
  }
}
