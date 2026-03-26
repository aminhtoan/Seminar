# Frontend Beginner Tutorial: Building a Professional Next.js Portfolio with an AI Digital Twin

## 1. What You Built

You now have a modern personal website that includes:

- A premium, responsive one-page profile site
- About, journey, portfolio placeholder, and contact sections
- A Digital Twin chat widget on the same page
- A backend API route that calls OpenRouter securely
- A fallback environment-variable strategy to avoid key-sync issues

This is a full-stack frontend project because your user interface (frontend) and your API route (backend endpoint inside Next.js) live in one app.

---

## 2. Technology Summary (Beginner Friendly)

### Next.js (App Router)

Next.js is a React framework that gives you:

- File-based routing (folders become routes)
- Server and client component support
- API routes in the same project
- Good defaults for build and performance

You used the App Router structure under `src/app`.

### React

React is used for building the UI from components.

- `page.tsx` builds the main page
- `DigitalTwinChat.tsx` is an interactive chat component

### TypeScript

TypeScript adds static typing so your code is safer and easier to maintain.

### CSS Modules

You used scoped CSS files:

- `page.module.css` for page-level styling
- `DigitalTwinChat.module.css` for chat component styling

This avoids global class name collisions.

### OpenRouter API

Your API route sends chat requests to OpenRouter using this model:

- `openai/gpt-oss-120b`

### Environment Variables

The OpenRouter key is loaded from:

1. `professional-site/.env.local` (primary)
2. `day4/.env` (fallback)

That fallback was added to prevent mismatch problems between two env files.

---

## 3. Project Structure You Worked With

```text
professional-site/
  src/
    app/
      api/
        digital-twin/
          route.ts
      globals.css
      layout.tsx
      page.module.css
      page.tsx
    components/
      DigitalTwinChat.module.css
      DigitalTwinChat.tsx
  .env.local
  package.json
```

---

## 4. High-Level Walkthrough

### Step A: Build the static professional website

You created a strong one-page layout in `page.tsx` and styled it with:

- Visual brand blocks (hero, metrics, timeline)
- Typography hierarchy (headline font + body font)
- Rich background effects and responsive grids

### Step B: Add a chat widget (client-side UI)

In `DigitalTwinChat.tsx`, you added:

- Local state for messages
- A text input and starter question chips
- Request handling with loading and error states

### Step C: Add a secure server API route

In `route.ts`, you built a `POST` endpoint that:

- Accepts message history from frontend
- Injects a system prompt describing the Digital Twin behavior
- Calls OpenRouter and returns the assistant answer

### Step D: Connect frontend to backend

The chat component calls `/api/digital-twin`.

So the browser does not directly call OpenRouter with your secret key.

### Step E: Handle real-world key/env issues

You added:

- Key normalization (trim quotes and optional `Bearer ` prefix)
- Fallback env loading from parent `.env`
- Better error messages shown in UI

This made debugging much easier.

---

## 5. Request Flow (End-to-End)

1. User types a question in the chat box.
2. `DigitalTwinChat.tsx` sends a `POST` request to `/api/digital-twin`.
3. `route.ts` validates input and builds OpenRouter payload.
4. `route.ts` calls OpenRouter using your API key from env.
5. OpenRouter returns assistant content.
6. Frontend appends answer to chat history and re-renders.

---

## 6. Detailed Code Review with Samples

## 6.1 App Shell and Fonts (`src/app/layout.tsx`)

This file sets metadata and global font variables.

```tsx
import { IBM_Plex_Sans, JetBrains_Mono, Space_Grotesk } from "next/font/google";

const bodyFont = IBM_Plex_Sans({ variable: "--font-body", subsets: ["latin"], weight: ["400", "500", "600", "700"] });
const headingFont = Space_Grotesk({ variable: "--font-heading", subsets: ["latin"], weight: ["500", "600", "700"] });

export const metadata = {
  title: "Ed Donner | AI Leader & CTO",
  description: "Professional profile website highlighting AI leadership, career journey, and portfolio roadmap.",
};
```

Why this matters for beginners:

- `next/font/google` optimizes font loading automatically
- Metadata improves SEO and link previews

---

## 6.2 Global Theme Tokens (`src/app/globals.css`)

You used CSS custom properties (variables) for colors and surfaces.

```css
:root {
  --bg-main: #050810;
  --surface-elevated: linear-gradient(160deg, rgba(16, 26, 46, 0.78), rgba(6, 12, 23, 0.92));
  --text-main: #f3f8ff;
  --accent-strong: #ff6032;
}
```

Why this matters:

- Easy design consistency
- Easy future rebranding (edit in one place)

---

## 6.3 Main Page Composition (`src/app/page.tsx`)

Your page is structured as reusable content sections.

```tsx
<section id="digital-twin" className={styles.sectionPanel}>
  <p className={styles.sectionLabel}>AI Digital Twin</p>
  <h2>Ask Ed&apos;s AI twin about his career.</h2>
  <p>
    This assistant is powered by OpenRouter using model
    openai/gpt-oss-120b, with context grounded in Ed&apos;s career history.
  </p>
  <DigitalTwinChat />
</section>
```

Why this matters:

- Sections are easy to reorder or expand
- Navigation links target each section by `id`

---

## 6.4 Chat UI State Management (`src/components/DigitalTwinChat.tsx`)

This is where React state drives interaction.

```tsx
type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
const [input, setInput] = useState("");
const [isSending, setIsSending] = useState(false);
const [error, setError] = useState<string | null>(null);
```

When user submits:

```tsx
const response = await fetch("/api/digital-twin", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ messages: outboundMessages }),
});
```

If API fails:

```tsx
const failureMessage = [
  payload.message || "The Digital Twin is unavailable right now.",
  payload.detail,
].filter(Boolean).join(" ");
setError(failureMessage);
```

Why this matters:

- Clear loading and error UX
- Immediate user feedback
- Better debuggability

---

## 6.5 Chat Styling (`src/components/DigitalTwinChat.module.css`)

You used scoped styles and states for better UX:

```css
.messages {
  max-height: 360px;
  overflow-y: auto;
}

.starters button:hover:not(:disabled) {
  transform: translateY(-1px);
}
```

Why this matters:

- Scrollable chat history prevents layout break
- Hover and disabled states improve usability

---

## 6.6 Server API Route (`src/app/api/digital-twin/route.ts`)

This file does the secure OpenRouter call.

### Model and system prompt

```ts
const MODEL_NAME = "openai/gpt-oss-120b";
const DIGITAL_TWIN_SYSTEM_PROMPT = `You are the digital twin of Ed Donner...`;
```

### Env loading and fallback

```ts
const envKey = process.env.OPENROUTER_API_KEY?.trim()
  .replace(/^Bearer\s+/i, "")
  .replace(/^['"]|['"]$/g, "");
const apiKey = envKey || (await loadApiKeyFromParentEnv());
```

### OpenRouter request

```ts
const upstreamResponse = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${apiKey}`,
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:3000",
    "X-Title": "Ed Donner Digital Twin",
  },
  body: JSON.stringify({
    model: MODEL_NAME,
    temperature: 0.35,
    max_tokens: 450,
    messages: [{ role: "system", content: DIGITAL_TWIN_SYSTEM_PROMPT }, ...messages],
  }),
});
```

Why this matters:

- Secret key stays server-side
- Prompt controls persona and factual boundaries
- Validation and normalized parsing reduce runtime failures

---

## 7. Environment Setup and Common Pitfalls

### Expected variable

In `.env.local` (or parent `.env`):

```dotenv
OPENROUTER_API_KEY=your-real-openrouter-key
```

### Important beginner note

When you change `.env.local`, restart dev server so Next.js picks up the new value.

### The real issue you hit

You had a mismatch between root `.env` and app `.env.local`. The app was reading one key while you were editing another file. Syncing both fixed it.

---

## 8. Commands You Use Most

```bash
npm run dev
npm run lint
npm run build
```

---

## 9. How to Read the App as a Beginner

Use this order:

1. `layout.tsx` to understand shell + fonts
2. `globals.css` for design tokens
3. `page.tsx` for page structure
4. `DigitalTwinChat.tsx` for interactive logic
5. `route.ts` for server-side AI integration

This sequence goes from broad architecture to deepest logic.

---

## 10. Self-Review: 5 Improvements to Make Next

1. Add streaming responses for chat
- Right now answers appear only when full response arrives.
- Streaming tokens would feel faster and more modern.

2. Add stronger input validation and moderation
- Add max input length and optional content filtering before sending to model.

3. Add chat persistence
- Save conversation history in local storage or a lightweight database.
- This keeps context across page refreshes.

4. Improve accessibility
- Add ARIA live regions for new assistant responses.
- Improve focus handling after send.
- Add better keyboard shortcuts (for example, Enter to send, Shift+Enter newline).

5. Improve backend robustness
- Add timeout + retry policy for OpenRouter calls.
- Add structured logging and request IDs for easier production debugging.

---

## 11. Final Takeaway

You have built a polished, professional, beginner-friendly full-stack frontend project:

- Strong visual design
- Clear React component structure
- Practical AI integration through a secure server route
- Real troubleshooting experience with environment and API auth issues

That is exactly the type of project that builds real frontend engineering confidence.
