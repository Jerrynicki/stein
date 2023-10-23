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

  loginName = sessionStorage.getItem('loginName');
  api = '';

  goToPost(id: number) {
    this.router.navigate(['/post', id]);
  }

  goToProfile(author: string) {
    this.router.navigate(['/profile', author]);
  }

  async deletePost() {
    return;
  }

  distance(meters: number) {
    if (meters < 1000) {
      return meters + 'm';
    } else {
      return (meters / 1000).toFixed(1) + 'km';
    }
  }
}
