"use client";

import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";

export default function Card({ card, onDelete, isOverlay = false }) {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({ id: card.id, disabled: isOverlay });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
    };

    const draggingStyles = isDragging ? "opacity-60" : "opacity-100";

    return (
        <article
            ref={setNodeRef}
            style={style}
            data-testid={`card-${card.id}`}
            className={
                "group rounded-xl border border-border-muted bg-white p-3 shadow-sm " +
                draggingStyles +
                (isOverlay ? " shadow-md" : "")
            }
            aria-label={card.title}
            {...attributes}
            {...listeners}
        >
            <div className="flex items-start justify-between gap-2">
                <h3 className="text-sm font-semibold text-dark-navy leading-5">
                    {card.title}
                </h3>
                {onDelete ? (
                    <button
                        type="button"
                        onClick={(e) => {
                            e.stopPropagation();
                            onDelete();
                        }}
                        className="rounded-md border border-transparent px-2 py-1 text-xs font-semibold text-gray-text hover:border-border-muted hover:text-dark-navy"
                        aria-label={`Delete ${card.title}`}
                    >
                        Delete
                    </button>
                ) : null}
            </div>
            {card.details ? (
                <p className="mt-2 whitespace-pre-wrap text-sm text-gray-text leading-6">
                    {card.details}
                </p>
            ) : null}

            <div className="mt-3 h-0.5 w-10 rounded-full bg-accent-yellow" />
        </article>
    );
}
