import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostInterface } from '../post.interface';
import { CommentInterface } from '../comment.interface';
import { GeolocationService } from '@ng-web-apis/geolocation';

@Component({
  selector: 'app-post-big',
  templateUrl: './post-big.component.html',
  styleUrls: ['./post-big.component.scss'],
})
export class PostBigComponent {
  constructor(
    private readonly geolocation: GeolocationService,
    private route: ActivatedRoute,
    private http: HttpClient
  ) {
    this.route.params.subscribe((params) => (this.id = params['id']));
  }

  id: number = 0;
  post!: PostInterface;
  comments!: CommentInterface[];
  comment: { lng: number; lat: number; comment: string; rating: number } = {
    lng: 0,
    lat: 0,
    comment: '',
    rating: 0,
  };
  emojiRegex = /[^\u{1F600}-\u{1F64F}]+/gu;
  postCompleted: boolean = false;
  commentsCompleted: boolean = false;
  username = sessionStorage.getItem('username');
  api: string = 'http://127.0.0.1:5000';

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer' + sessionStorage.getItem('token'),
    }),
  };

  ngOnInit() {
    this.getPost(this.id);
    this.getComments(this.id);
  }

  async getPost(id: number) {
    this.http
      .get<PostInterface>(
        'http://127.0.0.1:5000/api/post?id=' + id,
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          if (response != null) {
            this.post = response;
          }
        },
        error: (error) => {},
        complete: () => {
          this.postCompleted = true;
        },
      });
  }

  async getComments(id: number) {
    this.http
      .get<CommentInterface[]>(
        'http://127.0.0.1:5000/api/post/comments?id=' + id,
        this.httpOptions
      )
      .subscribe({
        next: (response) => {
          if (response != null) {
            this.comments = response;
          }
        },
        error: (error) => {},
        complete: () => {
          this.commentsCompleted = true;
        },
      });
  }

  async createComment() {
    this.geolocation.subscribe((position) => {
      this.comment.lat = position.coords.latitude;
      this.comment.lng = position.coords.longitude;
    });
    this.http
      .post<any>(
        'http://127.0.0.1:5000/api/post/comments?id=' + this.id,
        {
          location_lon: this.comment.lng,
          location_lat: this.comment.lat,
          rating: this.comment.rating,
          comment: this.comment.comment,
        },
        this.httpOptions
      )
      .subscribe({
        next: (response) => {},
        error: (error) => {
          console.error(error);
          if (error.status === 403) {
          } else {
          }
        },
        complete: () => {},
      });
  }

  distance(meters: number) {
    if (meters < 1000) {
      return meters + 'm';
    } else {
      return (meters / 1000).toFixed(1) + 'km';
    }
  }
}
