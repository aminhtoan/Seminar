"use client";

import dynamic from "next/dynamic";

const Board = dynamic(() => import("../components/Board"), { ssr: false });

export default function HomeClient() {
    return (
        <main className="flex flex-1 flex-col gap-4 px-6 py-6">
            <header className="flex items-end justify-between gap-4">
                <div className="flex flex-col gap-1">
                    <h1 className="text-2xl font-semibold tracking-tight text-dark-navy">
                        Kanban Board
                    </h1>
                    <p className="text-sm text-gray-text">
                        Single board. Five columns. Drag cards to move.
                    </p>
                </div>
                <div className="hidden sm:block text-sm text-gray-text">
                    No persistence (MVP)
                </div>
            </header>

            <Board />
        </main>
    );
}
