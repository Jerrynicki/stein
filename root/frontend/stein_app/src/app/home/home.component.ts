import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GeolocationService } from '@ng-web-apis/geolocation';
import { PostInterface } from '../post.interface';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  constructor(
    private readonly geolocation: GeolocationService,
    private http: HttpClient,
  ) {}

  ngOnInit() {
    this.geolocation.subscribe((position) => {
      if (this.completed == false) {
        this.getPosts(position.coords.latitude, position.coords.longitude, 0);
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
      }
    });
  }

  ngOnDestroy() {
    this.completed = false;
    this.posts = [];
  }

  posts!: PostInterface[];
  completed = false;
  lat: number = 0;
  lng: number = 0;
  page: number = 0;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + sessionStorage.getItem('token'),
    }),
  };

  pageChange(change: number) {
    this.posts = [];
    console.log(this.page);
    console.log(change);
    this.page += change;
    console.log(this.page);
    this.getPosts(this.lat, this.lng, this.page);
  }

  async getPosts(lat: number, lng: number, page: number) {
    this.http
      .get<PostInterface[]>(
        '/api/posts?page=' +
          page +
          '&location_lat=' +
          lat +
          '&location_lon=' +
          lng,
        this.httpOptions,
      )
      .subscribe({
        next: (response) => {
          if (response != null) {
            this.posts = response;
          }
        },
        error: (error) => {},
        complete: () => {
          this.completed = true;
        },
      });
  }
}
