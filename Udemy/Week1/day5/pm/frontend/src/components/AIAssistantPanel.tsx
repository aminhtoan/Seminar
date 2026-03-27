"use client";

import { FormEvent, useState } from "react";

type ChatMessage = {
  role: "assistant" | "user" | "error";
  content: string;
};

type ChatApiSuccess = {
  status: "ok";
  model: string;
  answer: string;
};

type ChatApiError = {
  error?: {
    message?: string;
  };
};

export const AIAssistantPanel = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [prompt, setPrompt] = useState("");
  const [isSending, setIsSending] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const trimmed = prompt.trim();
    if (!trimmed || isSending) {
      return;
    }

    setPrompt("");
    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setIsSending(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!response.ok) {
        let errorMessage = "Unable to reach AI assistant.";

        try {
          const errorPayload = (await response.json()) as ChatApiError;
          if (errorPayload.error?.message) {
            errorMessage = errorPayload.error.message;
          }
        } catch {
          // Keep fallback message when response is not valid JSON.
        }

        setMessages((prev) => [...prev, { role: "error", content: errorMessage }]);
        return;
      }

      const payload = (await response.json()) as ChatApiSuccess;
      setMessages((prev) => [...prev, { role: "assistant", content: payload.answer }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "error",
          content: "Network error while contacting AI assistant.",
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <aside
      className="rounded-3xl border border-[var(--stroke)] bg-[var(--surface-strong)] p-4 shadow-[var(--shadow)]"
      data-testid="ai-chat-panel"
    >
      <div className="flex items-center justify-between gap-3">
        <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--gray-text)]">
          AI Assistant
        </p>
        <span className="text-[10px] font-semibold uppercase tracking-[0.22em] text-[var(--primary-blue)]">
          Live
        </span>
      </div>

      <h2 className="mt-2 font-display text-2xl font-semibold text-[var(--navy-dark)]">
        Chat
      </h2>

      <div className="mt-4 h-[260px] overflow-y-auto rounded-2xl border border-[var(--stroke)] bg-[var(--surface)] p-3">
        {messages.length === 0 ? (
          <p className="text-sm leading-6 text-[var(--gray-text)]">
            Ask the assistant to create, move, or update cards.
          </p>
        ) : (
          <ul className="space-y-3">
            {messages.map((message, index) => (
              <li
                key={`${message.role}-${index}`}
                className={`rounded-xl px-3 py-2 text-sm leading-6 ${
                  message.role === "user"
                    ? "bg-[var(--secondary-purple)] text-white"
                    : message.role === "error"
                      ? "border border-red-200 bg-red-50 text-red-700"
                      : "bg-white text-[var(--navy-dark)]"
                }`}
              >
                {message.content}
              </li>
            ))}
          </ul>
        )}
      </div>

      <form className="mt-4" onSubmit={handleSubmit}>
        <label htmlFor="ai-chat-input" className="sr-only">
          Ask the assistant
        </label>
        <textarea
          id="ai-chat-input"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          placeholder="Ask the assistant"
          rows={3}
          className="w-full resize-none rounded-2xl border border-[var(--stroke)] bg-[var(--surface)] px-3 py-2 text-sm text-[var(--navy-dark)] outline-none transition placeholder:text-[var(--gray-text)] focus:border-[var(--primary-blue)]"
        />
        <button
          type="submit"
          disabled={isSending || prompt.trim().length === 0}
          className="mt-3 w-full rounded-full bg-[var(--secondary-purple)] px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-white transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSending ? "Sending..." : "Send"}
        </button>
      </form>
    </aside>
  );
};
