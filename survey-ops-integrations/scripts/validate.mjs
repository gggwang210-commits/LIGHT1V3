import { readFile, readdir } from 'node:fs/promises';
import { join, relative } from 'node:path';

const root = new URL('..', import.meta.url).pathname;

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];
    if (char === '"' && quoted && next === '"') {
      cell += '"';
      i += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === ',' && !quoted) {
      row.push(cell);
      cell = '';
    } else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && next === '\n') i += 1;
      row.push(cell);
      if (row.some((value) => value !== '')) rows.push(row);
      row = [];
      cell = '';
    } else {
      cell += char;
    }
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  return rows;
}

async function collectFiles(directory) {
  const output = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) output.push(...await collectFiles(path));
    else output.push(path);
  }
  return output;
}

for (const file of [
  'schemas/survey-response.schema.json',
  'schemas/public-export.schema.json',
  'data/sample_response.json',
  'airtable/base_schema.json',
  'slack/notification-template.json',
  'package.json'
]) {
  JSON.parse(await readFile(join(root, file), 'utf8'));
}

const catalogRows = parseCsv(await readFile(join(root, 'data/question_catalog.csv'), 'utf8'));
const headers = catalogRows.shift();
assert(headers[0] === 'question_key', 'question_catalog.csv header is invalid');
assert(catalogRows.length === 45, `expected 45 questions, found ${catalogRows.length}`);

const keys = catalogRows.map((row) => row[0]);
assert(new Set(keys).size === 45, 'question keys must be unique');
for (const role of ['owner', 'coach', 'member']) {
  assert(catalogRows.filter((row) => row[1] === role).length === 15, `${role} must have 15 questions`);
  for (let index = 1; index <= 15; index += 1) {
    assert(keys.includes(`${role}_${String(index).padStart(2, '0')}`), `missing ${role}_${index}`);
  }
}

const sample = JSON.parse(await readFile(join(root, 'data/sample_response.json'), 'utf8'));
assert(sample.role === 'coach', 'sample role must remain synthetic coach data');
assert(Object.keys(sample.answers).length === 15, 'sample must contain exactly 15 answers');
assert(!sample.contact, 'sample must not contain contact data');
assert(!sample.comment, 'sample must not contain free-form comment data');

const publicSchema = JSON.parse(await readFile(join(root, 'schemas/public-export.schema.json'), 'utf8'));
const publicFields = Object.keys(publicSchema.properties || {});
for (const forbidden of ['contact', 'comment', 'reply_email', 'phone', 'pdf', 'response_id']) {
  assert(!publicFields.includes(forbidden), `public schema exposes ${forbidden}`);
}

const allFiles = await collectFiles(root);
for (const file of allFiles) {
  const path = relative(root, file);
  assert(path !== '.env', '.env must not be committed');
  if (!/\.(md|json|js|mjs|gs|csv|example|yml)$/.test(path)) continue;
  const text = await readFile(file, 'utf8');
  const suspiciousSlack = text.match(/hooks\.slack\.com\/services\/(?!replace|\[REDACTED\]|\{\{)[A-Za-z0-9]{6,}/i);
  assert(!suspiciousSlack, `possible live Slack webhook in ${path}`);
  const suspiciousAirtable = text.match(/\bpat[A-Za-z0-9]{20,}\b/);
  assert(!suspiciousAirtable, `possible live Airtable token in ${path}`);
}

console.log('LIGHT ONE survey integration validation passed: 45 questions, JSON valid, no obvious secrets.');

