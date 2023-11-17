export interface Login {
  token: string;
  expiry: number;
  admin: boolean;
  banned: boolean;
}
