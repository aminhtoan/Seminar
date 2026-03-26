export const COLUMN_ORDER = [
    "col-1",
    "col-2",
    "col-3",
    "col-4",
    "col-5",
];

export function createInitialBoardState() {
    const columns = {
        "col-1": { id: "col-1", title: "Backlog", cardIds: ["card-1", "card-2"] },
        "col-2": { id: "col-2", title: "Planned", cardIds: ["card-3"] },
        "col-3": { id: "col-3", title: "In Progress", cardIds: ["card-4"] },
        "col-4": { id: "col-4", title: "Review", cardIds: [] },
        "col-5": { id: "col-5", title: "Done", cardIds: ["card-5"] },
    };

    const cards = {
        "card-1": {
            id: "card-1",
            title: "Set up project",
            details: "Scaffold the Next.js frontend and verify it runs.",
        },
        "card-2": {
            id: "card-2",
            title: "Design board UI",
            details: "Apply the color scheme and build a clean layout.",
        },
        "card-3": {
            id: "card-3",
            title: "Add cards",
            details: "Create new cards in a column with title + details.",
        },
        "card-4": {
            id: "card-4",
            title: "Drag & drop",
            details: "Move cards between columns with a smooth interaction.",
        },
        "card-5": {
            id: "card-5",
            title: "Write tests",
            details: "Add unit tests and Playwright integration tests.",
        },
    };

    return {
        columns,
        columnOrder: [...COLUMN_ORDER],
        cards,
        nextCardNumber: 6,
    };
}

export function findColumnIdByCardId(state, cardId) {
    for (const columnId of state.columnOrder) {
        const column = state.columns[columnId];
        if (column.cardIds.includes(cardId)) {
            return columnId;
        }
    }
    return null;
}

function arrayMove(list, fromIndex, toIndex) {
    const next = [...list];
    const [item] = next.splice(fromIndex, 1);
    next.splice(toIndex, 0, item);
    return next;
}

function insertAt(list, index, item) {
    const next = [...list];
    next.splice(index, 0, item);
    return next;
}

function removeItem(list, item) {
    const index = list.indexOf(item);
    if (index === -1) return list;
    const next = [...list];
    next.splice(index, 1);
    return next;
}

export function boardReducer(state, action) {
    switch (action.type) {
        case "column/rename": {
            const { columnId, title } = action;
            const column = state.columns[columnId];
            if (!column) return state;

            return {
                ...state,
                columns: {
                    ...state.columns,
                    [columnId]: {
                        ...column,
                        title,
                    },
                },
            };
        }

        case "card/add": {
            const { columnId, title, details } = action;
            const column = state.columns[columnId];
            if (!column) return state;

            const trimmedTitle = (title ?? "").trim();
            const trimmedDetails = (details ?? "").trim();
            if (!trimmedTitle) return state;

            const id = `card-${state.nextCardNumber}`;
            return {
                ...state,
                cards: {
                    ...state.cards,
                    [id]: {
                        id,
                        title: trimmedTitle,
                        details: trimmedDetails,
                    },
                },
                columns: {
                    ...state.columns,
                    [columnId]: {
                        ...column,
                        cardIds: [...column.cardIds, id],
                    },
                },
                nextCardNumber: state.nextCardNumber + 1,
            };
        }

        case "card/delete": {
            const { cardId } = action;
            if (!state.cards[cardId]) return state;

            const fromColumnId = findColumnIdByCardId(state, cardId);
            if (!fromColumnId) return state;

            const fromColumn = state.columns[fromColumnId];
            const nextCards = { ...state.cards };
            delete nextCards[cardId];

            return {
                ...state,
                cards: nextCards,
                columns: {
                    ...state.columns,
                    [fromColumnId]: {
                        ...fromColumn,
                        cardIds: removeItem(fromColumn.cardIds, cardId),
                    },
                },
            };
        }

        case "card/move": {
            const { cardId, toColumnId, toIndex } = action;
            const fromColumnId = findColumnIdByCardId(state, cardId);
            if (!fromColumnId) return state;
            if (!state.columns[toColumnId]) return state;

            const fromColumn = state.columns[fromColumnId];
            const toColumn = state.columns[toColumnId];

            if (fromColumnId === toColumnId) {
                const fromIndex = fromColumn.cardIds.indexOf(cardId);
                if (fromIndex === -1) return state;
                const nextIndex = Math.max(0, Math.min(toIndex, fromColumn.cardIds.length - 1));
                if (fromIndex === nextIndex) return state;

                return {
                    ...state,
                    columns: {
                        ...state.columns,
                        [fromColumnId]: {
                            ...fromColumn,
                            cardIds: arrayMove(fromColumn.cardIds, fromIndex, nextIndex),
                        },
                    },
                };
            }

            const nextFromIds = removeItem(fromColumn.cardIds, cardId);
            const clampedToIndex = Math.max(0, Math.min(toIndex, toColumn.cardIds.length));
            const nextToIds = insertAt(toColumn.cardIds, clampedToIndex, cardId);

            return {
                ...state,
                columns: {
                    ...state.columns,
                    [fromColumnId]: { ...fromColumn, cardIds: nextFromIds },
                    [toColumnId]: { ...toColumn, cardIds: nextToIds },
                },
            };
        }

        default:
            return state;
    }
}
