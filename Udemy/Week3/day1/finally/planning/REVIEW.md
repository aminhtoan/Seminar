# Review of `planning/PLAN.md`

## Findings

1. High: The frontend requirements depend on market data that the backend contract does not define. The watchlist must show daily change percent and the main chart must show ticker history ([PLAN.md:25](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L25), [PLAN.md:26](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L26), [PLAN.md:355](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L355), [PLAN.md:356](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L356)), but the SSE cache only tracks latest and previous price ([PLAN.md:169](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L169), [PLAN.md:170](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L170)) and the stream payload only includes tick-by-tick fields ([PLAN.md:176](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L176), [PLAN.md:179](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L179)). That is not enough to render a persistent chart or a true daily change metric. The plan needs an explicit history/candle source, or the UI spec should be narrowed.

2. High: Trade execution is underspecified around atomicity and failure handling. `POST /api/portfolio/trade` updates cash, positions, trades, and portfolio snapshots ([PLAN.md:259](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L259), [PLAN.md:260](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L260), [PLAN.md:228](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L228)), and chat can auto-execute multiple actions from one LLM response ([PLAN.md:297](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L297), [PLAN.md:318](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L318), [PLAN.md:323](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L323)). The plan never states whether these writes must be wrapped in one SQLite transaction or what happens on partial failure. Without that contract, the system can drift into inconsistent state.

3. Medium: The first-launch story conflicts with the environment requirements for chat. The user experience says the AI panel is immediately ready ([PLAN.md:15](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L15), [PLAN.md:20](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L20)), but the environment section marks `OPENROUTER_API_KEY` as required for LLM chat ([PLAN.md:124](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L124)) and only defines mock mode as a testing option ([PLAN.md:131](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L131), [PLAN.md:342](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L342)). As written, a user can complete the documented startup flow and still find chat unavailable. The plan should define the fallback UX when no key is present.

4. Medium: The startup behavior is inconsistent across sections. The first-launch section says the browser opens automatically ([PLAN.md:15](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L15)), but the script section says browser opening is optional ([PLAN.md:406](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L406), [PLAN.md:410](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L410)). That mismatch will produce avoidable implementation and test ambiguity.

5. Low: The document includes a workspace-specific secret assumption that should not live in the canonical plan. It states that `OPENROUTER_API_KEY` exists in the root `.env` ([PLAN.md:286](O:\Seminar\Udemy\Week3\day1\finally\planning\PLAN.md#L286)). The plan should describe required variables and behavior, not assert the presence of a secret in a local checkout.

## Open Questions

- Should daily change mean market-session change, or just change since app load?
- Should a multi-trade assistant response be all-or-nothing, or can it partially succeed?
- If `OPENROUTER_API_KEY` is missing, should the app disable chat, force mock mode, or display a setup state?

## Summary

The plan has a solid architecture, but it still leaves a few implementation-critical contracts undefined: time-series market data, transaction boundaries, and chat startup behavior. Those gaps should be closed before implementation starts.
