const test = require('node:test'), assert = require('node:assert'), fs = require('fs'), vm = require('vm'), path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'src', 'last-stick.html'), 'utf8');
const js = html.match(/<script>([\s\S]*?)<\/script>/g).pop().replace(/<\/?script>/g, '');
const logic = js.slice(0, js.indexOf('function $(id)'));
const ctx = {}; vm.createContext(ctx); vm.runInContext(logic + '\nthis.api={BRANDS,ACHIEVEMENTS,LEVELS,levelFor,intake,project,minPerStick,streakStats,practicePoints,practiceKeys,practiceDayStreak,dayKey,genNick,genSquad,achValue,DAY_MS};', ctx);
const a = ctx.api;

test('deeper inhalation costs more life per cigarette', () => {
  assert.ok(a.minPerStick(2.2) > a.minPerStick(1.5));
  assert.ok(a.minPerStick(1.5) > a.minPerStick(1));
});
test('achievement ids are unique and points are positive', () => {
  const ids = a.ACHIEVEMENTS.map(x => x.id);
  assert.strictEqual(new Set(ids).size, ids.length);
  assert.ok(a.ACHIEVEMENTS.every(x => x.pts > 0 && x.target > 0));
});
test('levels are sorted and levelFor picks the right one', () => {
  assert.strictEqual(a.levelFor(0).i, 0);
  assert.strictEqual(a.levelFor(100).cur.name, 'Fresh Air');
  assert.strictEqual(a.levelFor(999999).next, null);
});
test('streak stats scale linearly with time', () => {
  const b = { sticks: 10, nic: 8, tar: 100, co: 100, price: 15, minPer: 20 };
  const one = a.streakStats(b, a.DAY_MS), two = a.streakStats(b, 2 * a.DAY_MS);
  assert.strictEqual(one.sticks, 10); assert.strictEqual(two.mins, 2 * one.mins);
});
test('practice points cap at 3 sessions a day', () => {
  const t = new Date(2026, 9, 14, 12).getTime();
  const log = [1, 2, 3, 4, 5].map(i => ({ t: t + i * 1000, c: 'yoga', n: 'x' }));
  assert.strictEqual(a.practicePoints(log), 15);
  assert.strictEqual(a.practiceKeys(log).length, 3);
});
test('practice day streak counts consecutive days', () => {
  const now = new Date(2026, 9, 14, 12).getTime();
  const log = [0, 1, 2].map(i => ({ t: now - i * a.DAY_MS, c: 'yoga', n: 'x' }));
  assert.strictEqual(a.practiceDayStreak(log, now), 3);
});
test('generated names match the server format', () => {
  for (let i = 0; i < 200; i++) { assert.match(a.genNick(), /^[A-Z][a-z]+[A-Z][a-z]+[0-9]{2}$/); assert.match(a.genSquad(), /^[A-Z][a-z]+ [A-Z][a-z]+ Squad$/); }
});
