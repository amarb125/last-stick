# Squads backend (Supabase)

Project: `vrkdyikakhgmcbzvgtfe` (free plan, ap-south-1). Private schema `ls` (RLS on, no policies, so tables are unreachable from the API). The only entry points are SECURITY DEFINER RPCs in `public`, called at `/rest/v1/rpc/<name>` with the anon key.

Tables: `members`, `squads`, `squad_members`, `point_events`, `cheers`, `catalog` (server-side list of valid achievement keys and points).

Identity: the app generates a 48-character secret; only its SHA-256 hash is stored. Names and squad names are generated from fixed word lists and validated server-side. Cheers are four presets, one per person per day.

Live RPCs: `ls_register`, `ls_profile`, `ls_sync`, `ls_create_squad`, `ls_join_squad`, `ls_my_squads`, `ls_open_squads`, `ls_leaderboard`, `ls_cheer`, `ls_inbox`.
Pending (see `supabase/migrations/0002_leave_delete_export.sql`): `ls_leave_squad`, `ls_delete_me`, `ls_export_me`.

Known limits: points are self-reported (streak achievements are checked against the streak start sent by the client); the project is on the free plan (pauses when idle, no backups). The original schema was applied by hand, so dump it with `supabase db dump --schema ls,public` and commit the result as `0001_schema.sql` before making further changes.
