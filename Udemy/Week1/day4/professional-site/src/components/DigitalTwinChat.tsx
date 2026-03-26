"use client";

import { FormEvent, useState } from "react";
import styles from "./DigitalTwinChat.module.css";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

const starterQuestions = [
  "What is Ed working on at Nebula right now?",
  "How did Ed transition from banking to AI startups?",
  "What technical leadership experience does Ed have?",
  "What speaking topics can Ed cover for events?",
];

const initialMessages: ChatMessage[] = [
  {
    role: "assistant",
    content:
      "I am Ed's Digital Twin. Ask me about his career journey, AI leadership, speaking experience, or startup background.",
  },
];

export default function DigitalTwinChat() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function sendMessage(rawInput: string) {
    const content = rawInput.trim();
    if (!content || isSending) {
      return;
    }

    setError(null);
    setInput("");
    const userMessage: ChatMessage = { role: "user", content };
    const outboundMessages = [...messages, userMessage];
    setMessages(outboundMessages);
    setIsSending(true);

    try {
      const response = await fetch("/api/digital-twin", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages: outboundMessages }),
      });

      const payload = (await response.json()) as {
        answer?: string;
        message?: string;
        detail?: string;
      };

      if (!response.ok || !payload.answer) {
        const failureMessage = [
          payload.message || "The Digital Twin is unavailable right now.",
          payload.detail,
        ]
          .filter(Boolean)
          .join(" ");
        setError(failureMessage);
        return;
      }

      setMessages((current) => [
        ...current,
        { role: "assistant", content: payload.answer as string },
      ]);
    } catch {
      setError("Network error while reaching the Digital Twin service.");
    } finally {
      setIsSending(false);
    }
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendMessage(input);
  }

  return (
    <div className={styles.chatCard}>
      <div className={styles.starters}>
        {starterQuestions.map((question) => (
          <button
            key={question}
            type="button"
            onClick={() => {
              void sendMessage(question);
            }}
            disabled={isSending}
          >
            {question}
          </button>
        ))}
      </div>

      <div className={styles.messages}>
        {messages.map((message, index) => (
          <article
            key={`${message.role}-${index}`}
            className={
              message.role === "assistant"
                ? styles.assistantMessage
                : styles.userMessage
            }
          >
            <p>{message.content}</p>
          </article>
        ))}

        {isSending ? (
          <p className={styles.status}>Digital Twin is thinking...</p>
        ) : null}
      </div>

      <form className={styles.composer} onSubmit={onSubmit}>
        <label htmlFor="digital-twin-input" className={styles.label}>
          Ask about Ed&apos;s experience
        </label>
        <div className={styles.inputRow}>
          <input
            id="digital-twin-input"
            value={input}
            onChange={(event) => {
              setInput(event.target.value);
            }}
            placeholder="Example: What makes Ed valuable as a CTO advisor?"
            disabled={isSending}
          />
          <button type="submit" disabled={isSending || !input.trim()}>
            Send
          </button>
        </div>
      </form>

      {error ? <p className={styles.error}>{error}</p> : null}
    </div>
  );
}
