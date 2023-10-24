export interface LoginResponse {
  token: string;
  expiry: number;
  admin: boolean;
  banned: boolean;
}

export enum LoginStatus {
  Initial = 'Initial',
  Loading = 'Loading',
  Success = 'Success',
  Fail = 'Fail',
  Error = 'Error',
}
