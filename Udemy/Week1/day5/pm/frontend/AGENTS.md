# Frontend Code Description

## Purpose

This document describes the current frontend implementation in frontend/ so future changes can align with existing structure and behavior.

## Current Stack

- Next.js 16 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- DnD Kit for drag-and-drop
- Vitest + Testing Library for unit/component tests
- Playwright for end-to-end tests

## Entry Points and Layout

- src/app/layout.tsx
  - Sets fonts using next/font/google (Space Grotesk for display, Manrope for body).
  - Defines metadata title and description.
- src/app/page.tsx
  - Renders KanbanBoard as the home page.
- src/app/globals.css
  - Imports Tailwind.
  - Defines global design tokens as CSS variables.
  - Implements project color scheme from root AGENTS.md.

## Main Feature: Kanban Board

- src/components/KanbanBoard.tsx
  - Client component.
  - Holds board state in memory (initialData).
  - Supports drag-and-drop via DndContext and DragOverlay.
  - Supports column rename, card add, and card delete.
- src/components/KanbanColumn.tsx
  - Renders one column.
  - Supports drop target behavior.
  - Exposes editable column title input.
  - Includes NewCardForm and card list.
- src/components/KanbanCard.tsx
  - Sortable draggable card.
  - Displays title/details and remove button.
- src/components/KanbanCardPreview.tsx
  - Preview component for DragOverlay while dragging.
- src/components/NewCardForm.tsx
  - Expand/collapse inline form for adding cards.

## Domain Logic

- src/lib/kanban.ts
  - Defines Card, Column, and BoardData types.
  - Contains initialData seed.
  - Contains moveCard utility for intra-column and cross-column moves.
  - Contains createId helper for client-side card IDs.

## Testing Setup

### Unit and Component Tests

- Vitest config: vitest.config.ts
- Test setup: src/test/setup.ts
- Existing tests:
  - src/lib/kanban.test.ts (moveCard behavior)
  - src/components/KanbanBoard.test.tsx (render, rename, add/remove card)

### End-to-End Tests

- Playwright config: playwright.config.ts
- Existing E2E tests:
  - tests/kanban.spec.ts
    - board load
    - add card
    - drag card between columns

## Scripts

- npm run dev
- npm run build
- npm run start
- npm run lint
- npm run test or npm run test:unit
- npm run test:e2e
- npm run test:all

## Current Data and State Model

- Frontend is currently demo-first and in-memory only.
- Board state is initialized from initialData and mutated client-side.
- No backend integration is currently wired in this frontend package.

## Testing/Quality Baseline for Upcoming Work

- Keep frontend unit test coverage at or above 80% for touched frontend modules.
- Maintain robust integration/end-to-end testing for critical user flows:
  - loading board
  - editing board state
  - drag-and-drop movement
  - login gating once added
  - backend persistence once integrated

## Notes for Future Integration

- Future backend integration should preserve existing component boundaries (KanbanBoard as orchestration layer).
- Prefer API adapter layer for fetch logic rather than mixing networking directly into presentational components.
- Keep data-testid attributes stable for E2E test reliability.
