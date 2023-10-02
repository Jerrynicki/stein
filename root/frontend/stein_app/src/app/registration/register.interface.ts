export interface RegisterResponse {
  token: string;
  expiry: number;
  username: string;
}

export enum RegisterStatus {
  Initial = 'Initial',
  Loading = 'Loading',
  Success = 'Success',
  Fail = 'Fail',
  Error = 'Error',
}
