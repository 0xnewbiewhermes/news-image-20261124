// Copies the front page (entry.png, next to this file) into MAKEFUN_OUTPUT_DIR.
// The file is checked first: PNG signature and size. Nothing is read from the
// current working directory, so the program works from any folder.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR;

if (!outDir) {
  console.error("MAKEFUN_OUTPUT_DIR is not set");
  process.exit(1);
}

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
// The last chunk of a whole PNG: length 0, type IEND, and its CRC.
const PNG_IEND = [0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82];
const MAX_BYTES = 1048576;

const bytes = readFileSync(source);
const size = statSync(source).size;
if (size > MAX_BYTES) {
  console.error(`entry.png is ${size} bytes, over the 1 MiB limit`);
  process.exit(1);
}
if (!PNG_SIGNATURE.every((b, i) => bytes[i] === b)) {
  console.error("entry.png does not start with the PNG signature");
  process.exit(1);
}

const tail = bytes.subarray(bytes.length - PNG_IEND.length);
if (!PNG_IEND.every((b, i) => tail[i] === b)) {
  console.error("entry.png does not end with the IEND chunk, so the file is not whole");
  process.exit(1);
}

// The IHDR chunk follows the signature: width and height as 32-bit big-endian integers.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  console.error(`entry.png is ${width} x ${height}, over the 1024 x 1024 limit`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`copied entry.png (${size} bytes) to ${outDir}`);
