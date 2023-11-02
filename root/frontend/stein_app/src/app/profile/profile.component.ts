import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostInterface } from '../post.interface';
import { ProfileInterface } from './profile.interface';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
})
export class ProfileComponent {
  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
  ) {
    this.route.params.subscribe(
      (params) => (this.profilename = params['name']),
    );
  }

  posts!: PostInterface[];
  profile!: ProfileInterface;
  profilename!: string;
  profileCompleted: boolean = false;
  postsCompleted: boolean = false;
  username = sessionStorage.getItem('username');
  api: string = '';

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: 'Bearer ' + sessionStorage.getItem('token'),
    }),
  };

  ngOnInit() {
    this.getProfile(this.profilename);
    this.getPosts(this.profilename);
  }

  async getProfile(name: string) {
    this.http
      .get<ProfileInterface>('/api/profile?name=' + name, this.httpOptions)
      .subscribe({
        next: (response) => {
          if (response != null) {
            this.profile = response;
          }
        },
        error: (error) => {},
        complete: () => {
          this.profileCompleted = true;
          console.log(this.profile);
        },
      });
  }

  async getPosts(name: string) {
    this.http
      .get<PostInterface[]>(
        '/api/profile/posts?name=' + name + '&page=' + 0,
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
          this.postsCompleted = true;
        },
      });
  }
}
