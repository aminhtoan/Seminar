import { render, screen } from "@testing-library/react";
import { KanbanCardPreview } from "./KanbanCardPreview";
import type { Card } from "@/lib/kanban";

describe("KanbanCardPreview", () => {
  const mockCard: Card = {
    id: "card-1",
    title: "Test Card Title",
    details: "This is a test card description",
  };

  it("renders card title and details", () => {
    render(<KanbanCardPreview card={mockCard} />);

    expect(screen.getByText("Test Card Title")).toBeInTheDocument();
    expect(
      screen.getByText("This is a test card description"),
    ).toBeInTheDocument();
  });

  it("renders with correct structure", () => {
    render(<KanbanCardPreview card={mockCard} />);

    const article = screen.getByRole("article");
    expect(article).toBeInTheDocument();

    const title = screen.getByRole("heading", { level: 4 });
    expect(title).toHaveClass("font-semibold");
  });

  it("handles cards with empty details", () => {
    const cardWithoutDetails: Card = {
      id: "card-2",
      title: "Another Card",
      details: "",
    };

    render(<KanbanCardPreview card={cardWithoutDetails} />);

    expect(screen.getByText("Another Card")).toBeInTheDocument();
    const article = screen.getByRole("article");
    expect(article).toBeInTheDocument();
  });
});
