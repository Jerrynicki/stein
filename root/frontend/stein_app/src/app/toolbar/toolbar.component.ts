import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-toolbar',
  templateUrl: './toolbar.component.html',
  styleUrls: ['./toolbar.component.scss'],
})
export class ToolbarComponent {
  constructor(private router: Router) {}

  login: boolean = false;
  sidebarVisible = false;

  ngOnInit() {
    sessionStorage.getItem('login') == 'true' ? this.login = true : this.login = false;
  }

  route(destination: string) {
    if (destination != 'profile') {
      this.router.navigate(['/' + destination]);
    } else {
      this.router.navigate(['/profile', sessionStorage.getItem('username')]);
    }
  }

  logout() {
    sessionStorage.setItem('login', 'false');
    sessionStorage.setItem('token', '');
    sessionStorage.setItem('username', '');
    sessionStorage.setItem('expiry', '');
    sessionStorage.setItem('admin', 'false');
    sessionStorage.setItem('banned', 'false');
    window.location.reload();
  }
}
