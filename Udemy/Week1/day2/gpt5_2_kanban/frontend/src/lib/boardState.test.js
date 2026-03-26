import {
    boardReducer,
    createInitialBoardState,
    findColumnIdByCardId,
} from "./boardState";

describe("boardState", () => {
    test("creates a single board with five columns", () => {
        const state = createInitialBoardState();
        expect(state.columnOrder).toHaveLength(5);
        for (const colId of state.columnOrder) {
            expect(state.columns[colId]).toBeTruthy();
        }
    });

    test("renames a column", () => {
        const state = createInitialBoardState();
        const next = boardReducer(state, {
            type: "column/rename",
            columnId: "col-1",
            title: "Ideas",
        });
        expect(next.columns["col-1"].title).toBe("Ideas");
    });

    test("adds a card to a column", () => {
        const state = createInitialBoardState();
        const next = boardReducer(state, {
            type: "card/add",
            columnId: "col-4",
            title: "New card",
            details: "Some details",
        });

        const col = next.columns["col-4"];
        expect(col.cardIds).toHaveLength(1);
        const newId = col.cardIds[0];
        expect(next.cards[newId].title).toBe("New card");
        expect(next.cards[newId].details).toBe("Some details");
    });

    test("deletes a card", () => {
        const state = createInitialBoardState();
        const next = boardReducer(state, { type: "card/delete", cardId: "card-1" });
        expect(next.cards["card-1"]).toBeUndefined();
        expect(next.columns["col-1"].cardIds.includes("card-1")).toBe(false);
    });

    test("moves a card within the same column", () => {
        const state = createInitialBoardState();
        expect(state.columns["col-1"].cardIds).toEqual(["card-1", "card-2"]);

        const next = boardReducer(state, {
            type: "card/move",
            cardId: "card-1",
            toColumnId: "col-1",
            toIndex: 1,
        });

        expect(next.columns["col-1"].cardIds).toEqual(["card-2", "card-1"]);
    });

    test("moves a card to a different column", () => {
        const state = createInitialBoardState();
        const fromColumnId = findColumnIdByCardId(state, "card-3");
        expect(fromColumnId).toBe("col-2");

        const next = boardReducer(state, {
            type: "card/move",
            cardId: "card-3",
            toColumnId: "col-3",
            toIndex: 0,
        });

        expect(next.columns["col-2"].cardIds.includes("card-3")).toBe(false);
        expect(next.columns["col-3"].cardIds[0]).toBe("card-3");
    });
});
