import { moveCard, type Column, createId } from "@/lib/kanban";

describe("moveCard", () => {
  const baseColumns: Column[] = [
    { id: "col-a", title: "A", cardIds: ["card-1", "card-2"] },
    { id: "col-b", title: "B", cardIds: ["card-3"] },
  ];

  it("reorders cards in the same column", () => {
    const result = moveCard(baseColumns, "card-2", "card-1");
    expect(result[0].cardIds).toEqual(["card-2", "card-1"]);
  });

  it("moves cards to another column", () => {
    const result = moveCard(baseColumns, "card-2", "card-3");
    expect(result[0].cardIds).toEqual(["card-1"]);
    expect(result[1].cardIds).toEqual(["card-2", "card-3"]);
  });

  it("drops cards to the end of a column", () => {
    const result = moveCard(baseColumns, "card-1", "col-b");
    expect(result[0].cardIds).toEqual(["card-2"]);
    expect(result[1].cardIds).toEqual(["card-3", "card-1"]);
  });

  it("handles missing active card gracefully", () => {
    const result = moveCard(baseColumns, "card-nonexistent", "card-1");
    expect(result).toEqual(baseColumns);
  });

  it("handles no movement when moving to adjacent card", () => {
    const result = moveCard(baseColumns, "card-1", "card-2");
    // Moving card-1 onto card-2 reorders them
    expect(result[0].cardIds).toEqual(["card-2", "card-1"]);
  });
});

describe("createId", () => {
  it("generates unique IDs with correct prefix", () => {
    const id1 = createId("card");
    const id2 = createId("card");

    expect(id1).toMatch(/^card-/);
    expect(id2).toMatch(/^card-/);
    expect(id1).not.toEqual(id2);
  });

  it("generates IDs for different prefixes", () => {
    const cardId = createId("card");
    const colId = createId("col");

    expect(cardId).toMatch(/^card-/);
    expect(colId).toMatch(/^col-/);
  });
});
