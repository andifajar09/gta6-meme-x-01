// main.ts — entry program for make.fun bounty gta6-meme-x-01
// ("Post a GTA 6 meme on X"). Node 22, standard library only.
//
// What the house grades is the post itself: its address sits in
// POST.json at this repository's root, and the house reads the post
// from X's public view. This program's whole job, when the house runs
// it in its sandbox, is to hand that file over: copy POST.json from
// the repository directory to the output directory.
//
// Locally the same run looks like:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// MAKEFUN_BOT_DIR names the repository directory (the grader mounts
// it at /bot) and MAKEFUN_OUTPUT_DIR the output directory (/output).

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

if (!existsSync(source)) {
  console.error(`main.ts: no POST.json at ${source}; nothing to hand over`);
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);
console.log(`main.ts: copied ${source} -> ${target}`);
