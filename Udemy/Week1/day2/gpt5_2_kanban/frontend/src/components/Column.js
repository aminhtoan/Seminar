"use client";

import { useDroppable } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import { useId, useMemo, useState } from "react";

import Card from "./Card";

export default function Column({ column, cards, onRename, onAddCard, onDeleteCard }) {
    const { setNodeRef, isOver } = useDroppable({ id: column.id });
    const inputId = useId();
    const titleInputId = useId();
    const detailsInputId = useId();

    const [isAdding, setIsAdding] = useState(false);
    const [title, setTitle] = useState("");
    const [details, setDetails] = useState("");

    const cardIds = useMemo(() => cards.map((c) => c.id), [cards]);

    function submitAdd(e) {
        e.preventDefault();
        onAddCard({ title, details });
        setTitle("");
        setDetails("");
        setIsAdding(false);
    }

    return (
        <section
            ref={setNodeRef}
            data-testid={`column-${column.id}`}
            className={
                "flex min-h-[520px] flex-col rounded-xl border bg-white p-3 shadow-sm " +
                (isOver ? "border-blue-primary" : "border-border-muted")
            }
            aria-label={column.title}
        >
            <div className="flex items-start justify-between gap-2">
                <div className="flex flex-1 flex-col gap-1">
                    <label htmlFor={inputId} className="text-xs font-medium text-gray-text">
                        Column
                    </label>
                    <input
                        id={inputId}
                        value={column.title}
                        onChange={(e) => onRename(e.target.value)}
                        className="w-full rounded-md border border-border-muted bg-white px-2 py-1 text-sm font-semibold text-dark-navy outline-none focus:border-purple-secondary"
                    />
                </div>
                <div className="mt-6 rounded-full border border-border-muted px-2 py-1 text-xs text-gray-text">
                    {cards.length}
                </div>
            </div>

            <div className="mt-3 flex flex-1 flex-col gap-2 overflow-y-auto pr-1">
                <SortableContext items={cardIds} strategy={verticalListSortingStrategy}>
                    {cards.length === 0 ? (
                        <div className="rounded-lg border border-dashed border-border-muted px-3 py-4 text-sm text-gray-text">
                            Empty
                        </div>
                    ) : (
                        cards.map((card) => (
                            <Card
                                key={card.id}
                                card={card}
                                onDelete={() => onDeleteCard(card.id)}
                            />
                        ))
                    )}
                </SortableContext>
            </div>

            <div className="mt-3">
                {isAdding ? (
                    <form onSubmit={submitAdd} className="flex flex-col gap-2">
                        <div className="flex flex-col gap-1">
                            <label htmlFor={titleInputId} className="text-xs font-medium text-gray-text">
                                Title
                            </label>
                            <input
                                id={titleInputId}
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="w-full rounded-md border border-border-muted bg-white px-2 py-1 text-sm text-dark-navy outline-none focus:border-purple-secondary"
                                autoFocus
                            />
                        </div>
                        <div className="flex flex-col gap-1">
                            <label htmlFor={detailsInputId} className="text-xs font-medium text-gray-text">
                                Details
                            </label>
                            <textarea
                                id={detailsInputId}
                                value={details}
                                onChange={(e) => setDetails(e.target.value)}
                                className="min-h-[72px] w-full resize-none rounded-md border border-border-muted bg-white px-2 py-1 text-sm text-dark-navy outline-none focus:border-purple-secondary"
                            />
                        </div>
                        <div className="flex items-center justify-end gap-2">
                            <button
                                type="button"
                                onClick={() => setIsAdding(false)}
                                className="rounded-md border border-border-muted bg-white px-3 py-1.5 text-sm font-medium text-gray-text hover:border-gray-text"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                className="rounded-md bg-purple-secondary px-3 py-1.5 text-sm font-semibold text-white hover:opacity-95"
                            >
                                Add
                            </button>
                        </div>
                    </form>
                ) : (
                    <button
                        type="button"
                        onClick={() => setIsAdding(true)}
                        className="w-full rounded-md border border-border-muted bg-white px-3 py-2 text-sm font-semibold text-purple-secondary hover:border-purple-secondary"
                    >
                        + Add card
                    </button>
                )}
            </div>
        </section>
    );
}
