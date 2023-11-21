import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  constructor() {}

  // checks if the token is valid
  isValid(expiry: number): boolean {
    if (expiry > Date.now()) {
      return true;
    } else {
      return false;
    }
  }

  // return the Username for given token
  // TODO: implement
  getUser(token: string): string {
    let user: string = 'user';
    return user;
  }
}
