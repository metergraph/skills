#!/usr/bin/env node
// Checks every skill under skills/ against the rules the supported clients
// enforce, so a skill that installs in one client installs in all of them.
// Usage: node scripts/validate.mjs
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname;
const SKILLS = join(ROOT, "skills");
// Claude Desktop rejects an uploaded skill with any other frontmatter key.
const ALLOWED_KEYS = new Set(["name", "description", "license", "compatibility", "metadata", "allowed-tools"]);
const NAME = /^[a-z0-9]+(-[a-z0-9]+)*$/;
// Built from parts, so this file does not itself name what it looks for.
const PRIVATE = [new RegExp("\\b" + "MET" + "-\\d+\\b", "i"), new RegExp("linear" + "\\.app/", "i"), new RegExp("metergraph" + "-internal", "i"), /\/Users\//, /\/home\//];
const errors = [];

function frontmatter(text, where) {
  if (!text.startsWith("---\n")) return errors.push(`${where}: must start with --- frontmatter`), null;
  const end = text.indexOf("\n---\n", 4);
  if (end === -1) return errors.push(`${where}: frontmatter is not closed`), null;
  const fields = {};
  for (const line of text.slice(4, end).split("\n")) {
    const match = /^([a-z-]+):\s?(.*)$/.exec(line);
    if (!match) return errors.push(`${where}: unsupported frontmatter line: ${line}`), null;
    fields[match[1]] = match[2];
  }
  return { fields, body: text.slice(end + 5) };
}

const names = [];
for (const dir of readdirSync(SKILLS).sort()) {
  if (!statSync(join(SKILLS, dir)).isDirectory()) continue;
  const where = `skills/${dir}/SKILL.md`;
  let text;
  try {
    text = readFileSync(join(SKILLS, dir, "SKILL.md"), "utf8");
  } catch {
    errors.push(`${where}: missing`);
    continue;
  }
  const parsed = frontmatter(text, where);
  if (!parsed) continue;
  const { fields, body } = parsed;
  for (const key of Object.keys(fields)) {
    if (!ALLOWED_KEYS.has(key)) errors.push(`${where}: frontmatter key "${key}" is not allowed`);
  }
  if (fields.name !== dir) errors.push(`${where}: name must equal the directory name "${dir}"`);
  if (!NAME.test(fields.name ?? "") || fields.name.length > 64) {
    errors.push(`${where}: name must be 1-64 lowercase letters, digits and single hyphens`);
  }
  if (!fields.description) errors.push(`${where}: description is required`);
  else if (fields.description.length > 1024) errors.push(`${where}: description is over 1024 characters`);
  if (body.trim().length === 0) errors.push(`${where}: body is empty`);
  if (text.split("\n").length > 500) errors.push(`${where}: over 500 lines; move detail to a references/ file`);
  for (const pattern of PRIVATE) {
    if (pattern.test(text)) errors.push(`${where}: looks like a private reference (${pattern})`);
  }
  names.push(dir);
}

// Skills may refer to each other by name; every such name must exist.
// These are package and marketplace names, not skills.
const NOT_SKILLS = new Set(["metergraph-cli", "metergraph-mcp", "metergraph-skills", "metergraph-agents"]);
for (const dir of names) {
  const text = readFileSync(join(SKILLS, dir, "SKILL.md"), "utf8");
  for (const [, ref] of text.matchAll(/`(metergraph-[a-z-]+)`/g)) {
    if (!names.includes(ref) && !NOT_SKILLS.has(ref)) {
      errors.push(`skills/${dir}/SKILL.md: refers to unknown skill \`${ref}\``);
    }
  }
}

const marketplace = JSON.parse(readFileSync(join(ROOT, ".claude-plugin/marketplace.json"), "utf8"));
const plugin = JSON.parse(readFileSync(join(ROOT, ".claude-plugin/plugin.json"), "utf8"));
if (!marketplace.plugins?.some((entry) => entry.name === plugin.name && entry.source === "./")) {
  errors.push(".claude-plugin/marketplace.json: must list the root plugin with source ./");
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}
console.log(`${names.length} skills valid: ${names.join(", ")}`);
