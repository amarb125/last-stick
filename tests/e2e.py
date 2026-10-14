"""End-to-end smoke test with a mocked Squads backend. Run: python3 tests/e2e.py"""
import json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errs = []

def handle(route):
    req = route.request
    fn = req.url.split('/rpc/')[-1]
    hdr = {'access-control-allow-origin': '*', 'access-control-allow-headers': '*'}
    if req.method == 'OPTIONS':
        route.fulfill(status=200, headers=hdr); return
    prof = {'id': 'u1', 'nickname': 'BraveOtter11', 'public_board': False, 'streak_start': None, 'tot': 20, 'wk': 20}
    board = [{'id': 'u1', 'nickname': 'BraveOtter11', 'tot': 20, 'wk': 20, 'streak_start': None, 'best_s': 0, 'rk': 1, 'me': True, 'cheered': False, 'can_cheer': False},
             {'id': 'u2', 'nickname': 'WiseYak91', 'tot': 50, 'wk': 30, 'streak_start': '2026-10-10T00:00:00Z', 'best_s': 0, 'rk': 2, 'me': False, 'cheered': False, 'can_cheer': True}]
    out = {'ls_register': prof, 'ls_profile': prof, 'ls_sync': prof,
           'ls_my_squads': [{'id': 's1', 'name': 'Calm Lemur Squad', 'code': 'ABCDEFGH', 'theme': 'any', 'is_open': True, 'members': 2}],
           'ls_inbox': {'total': 0, 'recent': []}, 'ls_leaderboard': board, 'ls_cheer': {'ok': True}}.get(fn, [])
    route.fulfill(status=200, content_type='application/json', body=json.dumps(out), headers=hdr)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 800})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/rest/v1/rpc/*', handle)
    pg.route('**/fonts.*/**', lambda r: r.abort())
    pg.goto('file://' + os.path.join(ROOT, 'index.html'))

    pg.fill('#price', '20')
    pg.click('#tab-ach')
    assert '1 of' in pg.inner_text('#a-count'), 'calculator achievement should unlock'
    pg.click('#tab-streak'); pg.click('#s-start')
    pg.click('#tab-lungs'); pg.click('#ex-list summary >> nth=0'); pg.click('#ex-list button[data-log] >> nth=0')
    assert 'POINTS EARNED 5' in pg.inner_text('#pr-stats').replace('\n', ' ').upper()
    pg.click('#tab-social')
    assert pg.is_disabled('#so-join'), 'join must require the 18+ box'
    pg.check('#so-age'); assert not pg.is_disabled('#so-join')
    pg.click('#so-join'); pg.wait_for_selector('#so-me:not([hidden])')
    assert not pg.is_visible('#so-tools'), 'delete/export stay hidden until the backend functions exist'
    assert 'WiseYak91' in pg.inner_text('#so-table')
    pg.click('button[data-cheer=u2]'); pg.click('button[data-kind=proud]')
    pg.wait_for_selector('#so-msg:has-text("Cheer sent")')
    assert pg.is_visible('#legal'), 'legal links show in the web app'
    pg.click('#tab-lungs'); pg.click('#br-go'); pg.wait_for_timeout(600)
    assert 'BREATHE IN' in pg.inner_text('#orb-phase').upper(); pg.click('#br-go')
    b.close()

assert not errs, errs
print('e2e ok')
