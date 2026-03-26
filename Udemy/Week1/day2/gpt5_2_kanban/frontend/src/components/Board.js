"use client";

import { useReducer, useState } from "react";
import {
    DndContext,
    DragOverlay,
    KeyboardSensor,
    PointerSensor,
    closestCorners,
    useSensor,
    useSensors,
} from "@dnd-kit/core";

import Column from "./Column";
import Card from "./Card";
import {
    boardReducer,
    createInitialBoardState,
    findColumnIdByCardId,
} from "../lib/boardState";

export default function Board() {
    const [state, dispatch] = useReducer(boardReducer, undefined, () =>
        createInitialBoardState()
    );
    const [activeCardId, setActiveCardId] = useState(null);

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: { distance: 6 },
        }),
        useSensor(KeyboardSensor)
    );

    const activeCard = activeCardId ? state.cards[activeCardId] : null;

    function handleDragStart(event) {
        const id = event.active?.id;
        if (typeof id === "string" && state.cards[id]) {
            setActiveCardId(id);
        }
    }

    function handleDragCancel() {
        setActiveCardId(null);
    }

    function handleDragEnd(event) {
        const activeId = event.active?.id;
        const overId = event.over?.id;

        setActiveCardId(null);

        if (typeof activeId !== "string" || typeof overId !== "string") return;
        if (!state.cards[activeId]) return;
        if (activeId === overId) return;

        const fromColumnId = findColumnIdByCardId(state, activeId);
        if (!fromColumnId) return;

        // Dropped on a column container.
        if (state.columns[overId]) {
            const toColumnId = overId;
            const toIndex = state.columns[toColumnId].cardIds.length;
            dispatch({
                type: "card/move",
                cardId: activeId,
                toColumnId,
                toIndex,
            });
            return;
        }

        // Dropped on a card.
        if (state.cards[overId]) {
            const toColumnId = findColumnIdByCardId(state, overId);
            if (!toColumnId) return;

            const toIndex =
                toColumnId === fromColumnId
                    ? state.columns[toColumnId].cardIds.indexOf(overId)
                    : state.columns[toColumnId].cardIds.length;

            dispatch({
                type: "card/move",
                cardId: activeId,
                toColumnId,
                toIndex,
            });
        }
    }

    return (
        <section
            className="rounded-xl border border-border-muted bg-white/80 p-4 shadow-sm"
            aria-label="Kanban board"
        >
            <div
                className="grid gap-4"
                style={{ gridTemplateColumns: "repeat(5, minmax(220px, 1fr))" }}
            >
                <DndContext
                    sensors={sensors}
                    collisionDetection={closestCorners}
                    onDragStart={handleDragStart}
                    onDragCancel={handleDragCancel}
                    onDragEnd={handleDragEnd}
                >
                    {state.columnOrder.map((columnId) => {
                        const column = state.columns[columnId];
                        const cards = column.cardIds
                            .map((cardId) => state.cards[cardId])
                            .filter(Boolean);

                        return (
                            <Column
                                key={column.id}
                                column={column}
                                cards={cards}
                                onRename={(title) =>
                                    dispatch({ type: "column/rename", columnId, title })
                                }
                                onAddCard={({ title, details }) =>
                                    dispatch({ type: "card/add", columnId, title, details })
                                }
                                onDeleteCard={(cardId) => dispatch({ type: "card/delete", cardId })}
                            />
                        );
                    })}

                    <DragOverlay>
                        {activeCard ? (
                            <div className="w-[220px]">
                                <Card card={activeCard} isOverlay />
                            </div>
                        ) : null}
                    </DragOverlay>
                </DndContext>
            </div>

            <p className="mt-3 text-xs text-gray-text">
                Tip: Drag onto a column to append, or onto a card to reorder.
            </p>
        </section>
    );
}
