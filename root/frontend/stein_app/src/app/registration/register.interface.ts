export interface RegisterResponse {
  token: string;
  expiry: number;
  username: string;
}

export interface TeamResponse extends Array<string | number> {
  id: string;
  name: number;
  color: string;
}

export enum RegisterStatus {
  Initial = 'Initial',
  Loading = 'Loading',
  Success = 'Success',
  Fail = 'Fail',
  Error = 'Error',
}
