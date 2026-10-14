-- PENDING: not yet applied to the live project (the apply prompt was cancelled).
-- Apply in the Supabase SQL editor or via the Supabase tools, then set tools:true in LS_CONFIG (build.py) and rebuild.
create or replace function public.ls_leave_squad(p_secret text, p_squad uuid)
returns jsonb language plpgsql security definer set search_path to 'ls','public','extensions' as $$
declare v_id uuid;
begin
  v_id := ls.me(p_secret);
  delete from ls.squad_members where squad_id = p_squad and member_id = v_id;
  if not found then raise exception 'not_in_squad'; end if;
  delete from ls.squads s where s.id = p_squad and not exists (select 1 from ls.squad_members m where m.squad_id = s.id);
  return jsonb_build_object('ok', true);
end $$;

create or replace function public.ls_delete_me(p_secret text)
returns jsonb language plpgsql security definer set search_path to 'ls','public','extensions' as $$
declare v_id uuid;
begin
  v_id := ls.me(p_secret);
  delete from ls.members where id = v_id;
  delete from ls.squads s where not exists (select 1 from ls.squad_members m where m.squad_id = s.id);
  return jsonb_build_object('ok', true);
end $$;

create or replace function public.ls_export_me(p_secret text)
returns jsonb language plpgsql security definer set search_path to 'ls','public','extensions' as $$
declare v_id uuid;
begin
  v_id := ls.me(p_secret);
  return jsonb_build_object(
    'profile', (select jsonb_build_object('nickname', nickname, 'public_board', public_board, 'streak_start', streak_start, 'best_streak_seconds', best_streak_s, 'created_at', created_at) from ls.members where id = v_id),
    'points', coalesce((select jsonb_agg(jsonb_build_object('key', key, 'points', points, 'earned_at', earned_at) order by earned_at) from ls.point_events where member_id = v_id), '[]'::jsonb),
    'squads', coalesce((select jsonb_agg(jsonb_build_object('name', s.name, 'code', s.code, 'joined_at', sm.joined_at)) from ls.squad_members sm join ls.squads s on s.id = sm.squad_id where sm.member_id = v_id), '[]'::jsonb),
    'cheers_sent', (select count(*) from ls.cheers where from_member = v_id),
    'cheers_received', (select count(*) from ls.cheers where to_member = v_id));
end $$;

revoke all on function public.ls_leave_squad(text, uuid), public.ls_delete_me(text), public.ls_export_me(text) from public;
grant execute on function public.ls_leave_squad(text, uuid), public.ls_delete_me(text), public.ls_export_me(text) to anon, authenticated;
