export interface LoginResponse {
  token: string;
  expiry: number;
}

export enum LoginStatus {
  Initial = 'Initial',
  Loading = 'Loading',
  Success = 'Success',
  Fail = 'Fail',
  Error = 'Error',
}
