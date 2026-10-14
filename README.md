# last-stick

## Achievements, Lung care and Squads

The app now has points and levels for milestones, a Lung care tab (guided breathing, exercise, yoga and pranayama) and Squads, where people quitting together compare points on friendly weekly boards. Squads use a small Supabase backend: players appear under generated names only, cheers are preset, and points are self-reported.


## Development

- Source is `src/last-stick.html`. `python3 build.py` produces the deployable `index.html` (adds PWA head, CSP, service worker and the Squads config). Commit both.
- `npm test` runs logic tests (node) and an end-to-end browser test with a mocked backend (Python Playwright).
- GitHub Actions runs the same checks and fails if `index.html` is stale.
- Backend notes are in `docs/backend.md`. `supabase/migrations/0002_leave_delete_export.sql` is pending: apply it, set `tools:true` in `build.py`, rebuild, push.
- `privacy.html` and `terms.html` are drafts. Fill in the owner name and contact email and have them reviewed before launch.
