"use client";

import { FormEvent, useEffect, useState } from "react";
import { KanbanBoard } from "@/components/KanbanBoard";
import {
  AUTH_SESSION_KEY,
  LOGIN_CREDENTIALS,
  isValidCredentials,
} from "@/lib/auth";

export const AuthGate = () => {
  const [isReady, setIsReady] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const storedState = window.localStorage.getItem(AUTH_SESSION_KEY);
    setIsAuthenticated(storedState === "true");
    setIsReady(true);
  }, []);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setErrorMessage("");

    if (!isValidCredentials(username.trim(), password)) {
      setErrorMessage("Invalid credentials. Use user/password.");
      return;
    }

    window.localStorage.setItem(AUTH_SESSION_KEY, "true");
    setIsAuthenticated(true);
    setPassword("");
  };

  const handleLogout = () => {
    window.localStorage.removeItem(AUTH_SESSION_KEY);
    setIsAuthenticated(false);
    setUsername("");
    setPassword("");
    setErrorMessage("");
  };

  if (!isReady) {
    return null;
  }

  if (isAuthenticated) {
    return <KanbanBoard onLogout={handleLogout} />;
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-xl items-center px-6 py-12">
      <section className="w-full rounded-[28px] border border-[var(--stroke)] bg-white p-8 shadow-[var(--shadow)]">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-[var(--gray-text)]">
          PM MVP Access
        </p>
        <h1 className="mt-3 font-display text-3xl font-semibold text-[var(--navy-dark)]">
          Sign in to continue
        </h1>
        <p className="mt-3 text-sm text-[var(--gray-text)]">
          Use credentials: <strong>{LOGIN_CREDENTIALS.username}</strong>/
          <strong>{LOGIN_CREDENTIALS.password}</strong>
        </p>

        <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
          <label className="block text-sm font-medium text-[var(--navy-dark)]">
            Username
            <input
              className="mt-2 w-full rounded-xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm outline-none transition focus:border-[var(--primary-blue)]"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="Enter username"
              autoComplete="username"
            />
          </label>

          <label className="block text-sm font-medium text-[var(--navy-dark)]">
            Password
            <input
              type="password"
              className="mt-2 w-full rounded-xl border border-[var(--stroke)] bg-white px-4 py-3 text-sm outline-none transition focus:border-[var(--primary-blue)]"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter password"
              autoComplete="current-password"
            />
          </label>

          {errorMessage ? (
            <p className="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
              {errorMessage}
            </p>
          ) : null}

          <button
            type="submit"
            className="w-full rounded-xl bg-[var(--navy-dark)] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[var(--primary-blue)]"
          >
            Sign in
          </button>
        </form>
      </section>
    </main>
  );
};
