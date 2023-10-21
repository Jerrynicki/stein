import { Component, Input } from '@angular/core';
import { PostSmallInterface } from './post-small.interface';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-post-small',
  templateUrl: './post-small.component.html',
  styleUrls: ['./post-small.component.scss'],
})
export class PostSmallComponent {
  constructor(private http: HttpClient, private router: Router) {}
  @Input()
  post!: PostSmallInterface;

  loginName = sessionStorage.getItem('loginName');

  onClick(id: number) {
    this.router.navigate(['/post', id]);
  }

  async deletePost() {
    return;
  }
}
