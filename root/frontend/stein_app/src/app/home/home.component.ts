import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
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
    private http: HttpClient
  ) {}
  ngOnInit() {
    this.geolocation.subscribe((position) => {
      this.getPosts(position.coords.latitude, position.coords.longitude, 0);
    });
  }

  posts!: PostInterface[];
  completed = false;

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer' + sessionStorage.getItem('token'),
    }),
  };

  async getPosts(lat: number, lng: number, page: number) {
    this.http
      .get<PostInterface[]>(
        'http://127.0.0.1:5000/api/posts?page=' +
          page +
          '&location_lat=' +
          lat +
          '&location_lon=' +
          lng,
        this.httpOptions
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
