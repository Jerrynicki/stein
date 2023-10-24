import { Component, OnInit } from '@angular/core';
import {
  RegisterResponse,
  RegisterStatus,
  TeamResponse,
} from './register.interface';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ThemePalette } from '@angular/material/core';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Router } from '@angular/router';
import { TeamInterface } from './team.interface';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss'],
})
export class RegistrationComponent implements OnInit {
  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.http.get<TeamInterface[]>('/api/teams').subscribe({
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
  teams!: TeamInterface[];

  team!: number;
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
    console.log(this.team);
    this.http
      .post<RegisterResponse>(
        '/api/register',
        {
          password: this.password,
          team: this.team,
        },
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          sessionStorage.setItem('token', response.token);
          sessionStorage.setItem('expiry', this.expiretime(response.expiry));
          sessionStorage.setItem('username', response.username);
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
          console.log('register complete');
          this.registerstatus = RegisterStatus.Success;
          this.router.navigate([
            '/profile',
            sessionStorage.getItem('username'),
          ]);
        },
      });
  }

  expiretime(expiry: number) {
    return new Date(Date.now() + expiry * 1000).toString();
  }
}
