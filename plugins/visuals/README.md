# visuals

Visual asset generation for coding agents.

- **`/codex-image-gen`** — generates images headlessly with the [Codex CLI](https://developers.openai.com/codex/cli)'s built-in image tool. It handles finished pieces with typography baked in (posters, Instagram posts and stories, ads, thumbnails, covers) and components that sit in a layout (website heroes, slide backgrounds, icons, sprites, textures). It covers platform sizes and safe zones, exact-copy prompts, editing one line of copy with `-i`, and letter-by-letter proofing. The bundled `scripts/process.py` resizes, composites your real logo, keys out backgrounds, trims, makes textures tile and exports.
- **`/remotion-videos`** — builds videos (trailers, promos, explainers, social clips) in React with [Remotion](https://www.remotion.dev/docs). It plans a beat sheet first, then scaffolds from a tested data-driven template (`assets/Trailer.tsx`), follows the frame-driven rules that prevent flicker, checks stills at transition and end frames, renders, and exports a web MP4, GIF preview and poster with ffmpeg.

## Prerequisites

- `codex` CLI, logged in (`codex login status`)
- `uv` (the script declares its own Pillow/numpy dependencies)
- Node 18+ and `ffmpeg` for `/remotion-videos` (Remotion is free for teams of up to 3; larger companies need a licence)

## Usage

```
/remotion-videos a 45s trailer for the game in this repo using gameplay captures
/codex-image-gen an Instagram post + story for our autumn sale, 20% off, ends Oct 31
/codex-image-gen a hero image and 6 feature icons for the landing page in site/
/codex-image-gen slide backgrounds for a 10-slide deck about rail history, vintage poster style
```
