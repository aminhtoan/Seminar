import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AuthGate } from "@/components/AuthGate";
import { AUTH_SESSION_KEY } from "@/lib/auth";

describe("AuthGate", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("shows login gate when unauthenticated", () => {
    render(<AuthGate />);

    expect(
      screen.getByRole("heading", { name: /sign in to continue/i }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: /kanban studio/i }),
    ).not.toBeInTheDocument();
  });

  it("logs in with valid credentials and shows board", async () => {
    const user = userEvent.setup();
    render(<AuthGate />);

    await user.type(screen.getByLabelText(/username/i), "user");
    await user.type(screen.getByLabelText(/password/i), "password");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(
      screen.getByRole("heading", { name: /kanban studio/i }),
    ).toBeInTheDocument();
    expect(window.localStorage.getItem(AUTH_SESSION_KEY)).toBe("true");
  });

  it("rejects invalid credentials", async () => {
    const user = userEvent.setup();
    render(<AuthGate />);

    await user.type(screen.getByLabelText(/username/i), "wrong");
    await user.type(screen.getByLabelText(/password/i), "credentials");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: /kanban studio/i }),
    ).not.toBeInTheDocument();
  });

  it("restores persisted session and allows logout", async () => {
    const user = userEvent.setup();
    window.localStorage.setItem(AUTH_SESSION_KEY, "true");

    render(<AuthGate />);

    expect(
      screen.getByRole("heading", { name: /kanban studio/i }),
    ).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /log out/i }));

    expect(
      screen.getByRole("heading", { name: /sign in to continue/i }),
    ).toBeInTheDocument();
    expect(window.localStorage.getItem(AUTH_SESSION_KEY)).toBeNull();
  });
});
