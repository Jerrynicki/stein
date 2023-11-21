import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  constructor() {}

  // checks if the user is banned
  // TODO: implement
  isBanned(input: string, type: 'token' | 'username'): boolean {
    switch (type) {
      case 'username':
        return false;
        break;

      case 'token':
        return false;
        break;

      default:
        return false;
        break;
    }
  }
}
