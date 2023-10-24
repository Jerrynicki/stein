import { HttpClient } from '@angular/common/http';
import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { PostInterface } from '../post.interface';

@Component({
  selector: 'app-post-small',
  templateUrl: './post-small.component.html',
  styleUrls: ['./post-small.component.scss'],
})
export class PostSmallComponent {
  constructor(private http: HttpClient, private router: Router) {}

  @Input() post!: PostInterface;
  @Input() delete!: boolean;
  @Input() distance!: boolean;

  username = sessionStorage.getItem('username');
  api = 'http://127.0.0.1:5000';

  goToPost(id: number) {
    this.router.navigate(['/post', id]);
  }

  goToProfile(author: string) {
    this.router.navigate(['/profile', author]);
  }

  async deletePost() {
    return;
  }

  formatDistance(meters: number) {
    if (meters < 1000) {
      return meters + 'm';
    } else {
      return (meters / 1000).toFixed(1) + 'km';
    }
  }
}
