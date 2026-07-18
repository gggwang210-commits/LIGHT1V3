import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';

const inputPath = process.argv[2];
if (!inputPath) {
  throw new Error('Usage: EXPORT_SALT=... node export_public_jsonl.mjs input.json');
}

const salt = process.env.EXPORT_SALT;
if (!salt || salt.length < 16) {
  throw new Error('EXPORT_SALT must be at least 16 characters');
}

const SCALE = new Map([
  ['전혀 그렇지 않음', 1],
  ['매우 낮음', 1],
  ['그렇지 않음', 2],
  ['낮음', 2],
  ['보통', 3],
  ['그렇다', 4],
  ['높음', 4],
  ['매우 그렇다', 5],
  ['매우 높음', 5]
]);

function exportRecord(record) {
  if (!record.response_id || !record.received_at || !record.role || !record.answers) {
    throw new Error('Input record is missing required fields');
  }
  const anonymousId = createHash('sha256')
    .update(`${salt}:${record.response_id}`)
    .digest('hex')
    .slice(0, 12)
    .toUpperCase();

  const answers = Object.fromEntries(Object.entries(record.answers).map(([key, value]) => {
    if (!SCALE.has(value)) throw new Error(`Unsupported answer value for ${key}`);
    return [key, SCALE.get(value)];
  }));

  return {
    anonymous_id: `ANON-${anonymousId}`,
    received_month: String(record.received_at).slice(0, 7),
    role: record.role,
    answers,
    source_version: record.source_version || '2026-07',
    deidentified: true
  };
}

const parsed = JSON.parse(await readFile(inputPath, 'utf8'));
const records = Array.isArray(parsed) ? parsed : [parsed];
for (const record of records) {
  process.stdout.write(`${JSON.stringify(exportRecord(record))}\n`);
}

