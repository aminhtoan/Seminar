export const LOGIN_CREDENTIALS = {
  username: "user",
  password: "password",
} as const;

export const AUTH_SESSION_KEY = "pm-mvp-authenticated";

export const isValidCredentials = (username: string, password: string) =>
  username === LOGIN_CREDENTIALS.username &&
  password === LOGIN_CREDENTIALS.password;
