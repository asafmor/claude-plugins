---
name: codex-image-gen
description: "Generate raster images headlessly with the OpenAI Codex CLI's built-in image tool, then post-process and proof them into ship-ready files. Covers finished pieces with typography baked in (posters, Instagram/TikTok/LinkedIn posts and stories, ad creatives, YouTube thumbnails, flyers, event and campaign art, book or album covers, greeting cards) and components that sit inside a layout (website heroes and banners, slide backgrounds, illustrations, icons, sprites, stickers, seamless textures, UI frames). Use this whenever the user wants an image, poster, social post, ad, thumbnail, cover, picture, artwork, background, icon set or texture created, even if they don't mention Codex. Also use it to batch-produce a consistent campaign or asset set, resize a design for several platforms, change copy on a generated image, or match a reference image's style. Not for charts, diagrams or SVG/vector work you can write as code."
---

# codex-image-gen

Generate images with `codex exec`, keep the raw output, turn it into finished files with a reproducible post-processing step, and proof every image where it will actually be seen.

## 0. Preflight

```bash
codex login status   # exit code 0 means logged in
```

If this fails, ask the user to run `! codex login` (or `! codex login --device-auth` on WSL/SSH). Don't try to authenticate on their behalf.

## 1. Decide: finished piece or component?

This one decision changes the prompt, the post-processing and the checks, so make it per image.

| | **Finished piece** | **Component** |
| --- | --- | --- |
| Examples | Poster, social post or story, ad, thumbnail, flyer, cover, invitation | Website hero, slide background, game sprite, texture, icon, illustration placed in a page |
| Text | **Baked in.** The type is part of the composition. | **None.** The page, deck or game draws the text. |
| Why | It's seen as a single image, often re-shared, and there's no layout around it to carry the text. | Text in a layout can be translated, edited, read by screen readers and search engines, and reflowed at any screen size. Baked-in text can't. |

The model renders short, exact copy reliably (headlines, prices, dates, button labels), so text is not a reason to avoid baking it in. Be deliberate in these cases:

- **Many languages or many copy variants:** each one is a separate generation or edit. When there are more than a handful, consider a text-free base image plus an HTML/CSS overlay screenshotted with Playwright. You get pixel-exact brand fonts and one design for every variant.
- **Long copy** (paragraphs, fine print, terms): generated type gets small and error-prone. Keep baked-in copy to a headline, one supporting line and a call to action, and put the rest in the post caption or landing page.
- **Logos:** the generator redraws a logo rather than copying it, so the result looks almost right. Reserve a spot for the logo in the prompt and composite the real file afterwards (step 5).

## 2. Plan the set

Write down every image you need: its name, where it appears, the target pixel size and aspect ratio, whether it needs transparency, and **the exact copy** for finished pieces. Generations take 1–3 minutes each, so knowing the full list up front lets you run them all at once.

Common targets. Generate at the target **aspect ratio**, which the model follows, and resize to the exact pixels afterwards:

| Placement | Pixels | Ratio | Keep clear |
| --- | --- | --- | --- |
| Instagram / Facebook feed (portrait) | 1080×1350 | 4:5 | ~5% margin all round |
| Square post | 1080×1080 | 1:1 | ~5% margin |
| Story / Reel / TikTok | 1080×1920 | 9:16 | top ~250 px and bottom ~340 px (app UI) |
| YouTube thumbnail | 1280×720 | 16:9 | bottom-right corner (duration badge) |
| Link preview (Open Graph) / X / LinkedIn | 1200×630 | ~1.9:1 | text centred; edges may be cropped |
| Website hero | 1920×1080 (plus a 2× version) | 16:9 | headline area empty |

**Print:** generations are roughly 1–1.5 megapixels. That's fine on screen, but far too small for print at 300 dpi (an A4 page needs about 2480×3508). Tell the user before promising print-ready files. Upscaling is a separate step and needs a separate tool.

**Consistency across a set:** define one **style prefix** (palette, medium, mood, type style, e.g. `retro travel-poster illustration, muted teal and warm orange, bold condensed sans-serif headlines`) and start every prompt with it. Attach a reference image (brand art, a previous post, a mockup) with `-i` and ask the model to match it.

## 3. Generate

```bash
mkdir -p assets/raw logs
timeout 900 codex exec --skip-git-repo-check -s workspace-write --ephemeral \
  "Use your image generation tool to create this image: <style prefix>, <prompt>. \
   Save the PNG to ./assets/raw/<name>.png. Do not create any other files. \
   Reply only with the saved path." \
  < /dev/null > logs/gen_<name>.log 2>&1
```

Why each piece matters:

- `< /dev/null`: without it, `codex` waits on stdin forever when it runs in the background or in parallel. This is the most common way a batch hangs.
- `timeout 900`: one stuck generation shouldn't block the batch.
- `-s workspace-write`: Codex can write the file into the current directory and nowhere else.
- `--ephemeral`: one-off generations stay out of the user's session history.
- `--skip-git-repo-check`: lets it run outside a git repo.
- "Do not create any other files": otherwise Codex tends to leave helper scripts behind.
- **`-i ref.png` goes *after* the prompt.** `-i` accepts several files, so `codex exec -i ref.png "prompt"` treats the prompt as a second image path. Codex then reads an empty prompt from `/dev/null` and exits with "No prompt provided via stdin".

For several images, run them in parallel and wait:

```bash
for name in feed-post story thumbnail; do
  timeout 900 codex exec ... "./assets/raw/$name.png ..." < /dev/null > "logs/gen_$name.log" 2>&1 &
done
wait
ls -la assets/raw/
```

If a file is missing, read its log before retrying. Usual causes are auth, rate limits, the model refusing the prompt, or the `-i` ordering above.

## 4. Prompt recipes

**Finished pieces.** Name the format and ratio, give the composition, then specify the type:

- Put every piece of copy in quotes with its role and position: `headline at the top in large bold condensed sans-serif, exactly "LAST TRAIN NORTH"; below the illustration a smaller line exactly "Autumn rail tours - from $49"; a rounded orange button at the bottom with the text exactly "BOOK NOW"`.
- End with `All text spelled exactly as given, no other text, no watermark, keep all text well inside the edges`. Without the "no other text" line, the model fills empty space with invented signage and small print.
- State the clear zones: `keep the top 250px and bottom 300px free of text`, `keep the top-right corner empty for a logo`.
- Describe type by its look (weight, width, serif or sans, case), not by font name. A font name is only a loose hint.

| Piece | Pattern |
| --- | --- |
| Poster / flyer | "portrait poster 2:3 …, strong focal illustration, headline …, date/venue line …" |
| Feed post | "Instagram feed post, portrait 4:5 …, headline …, offer line …, button …" |
| Story / Reel cover | "vertical 9:16 …, text in the middle third only …, top/bottom clear for app UI" |
| YouTube thumbnail | "16:9 …, one expressive subject, 2–4 word headline huge and high-contrast, bottom-right clear" |
| Ad creative | "<ratio> …, product/subject hero, one benefit headline, call-to-action button …" |
| Cover (book/album/podcast) | "square or 2:3 …, title …, author/artist name …, legible at small sizes" |

**Components.** Say `no text` explicitly, or the model may add signage or captions:

| Asset | Pattern |
| --- | --- |
| Website hero / banner | "wide 16:9 …, empty negative space on the left for a headline, no text" |
| Slide background | "16:9 …, low contrast, subtle, large empty centre for content, no text" |
| Illustration / spot art | "… isolated subject, simple composition, no text" |
| Icons / sprites / stickers | "… single subject centred on a solid pure chroma-key green (#00FF00) background, no text, no shadow" (use magenta #FF00FF if the subject is green) |
| Seamless texture / pattern | "seamless tileable top-down texture of …, flat even lighting, no text, square" |
| Frame / panel | "ornate frame …, empty centre, symmetric, no text" (for CSS `border-image`) |

The model can't produce real alpha. For transparency, ask for a flat chroma-key colour and key it out in step 6. Don't use black or white for this: keying is by colour, so it would also remove the subject's own black outlines or white highlights and leave holes. Pick a colour the subject doesn't contain.

## 5. Edits and variants

To change copy (a new price, date or language) or fix one detail, edit instead of regenerating. Attach the current version, **after the prompt**, and limit the change:

```bash
timeout 900 codex exec --skip-git-repo-check -s workspace-write --ephemeral \
  "Use your image generation tool to edit the attached image: change only the price text from \"\$49\" to \"\$39\". \
   Keep everything else identical: illustration, layout, typography, colours, size. \
   Save the PNG to ./assets/raw/post-v2.png. Do not create any other files. Reply only with the saved path." \
  -i assets/raw/post.png < /dev/null > logs/gen_post-v2.log 2>&1
```

The edit looks the same, but the model **re-renders the whole image**, so it isn't pixel-identical: details can shift subtly anywhere. Proof every word again after each edit, not just the one you changed. Save each version as a new file (`-v2`, `-v3`) so you can go back.

For a campaign in several formats (feed + story + thumbnail), generate each format from the same style prefix and copy, at its own ratio. A crop of one format to another usually cuts off text or the subject.

## 6. Post-process (never ship raw output)

Leave originals untouched in `assets/raw/`, so any image can be reprocessed without regenerating. Use the bundled script (`scripts/process.py` in this skill's directory). `uv run` installs Pillow and numpy automatically:

```bash
P=<this skill dir>/scripts/process.py
uv run $P assets/raw/post.png      out/post.jpg       --size 1080x1350 --logo brand/logo.png --logo-pos br
uv run $P assets/raw/story.png     out/story.jpg      --size 1080x1920
uv run $P assets/raw/hero.png      out/hero.jpg       --size 1920x1080
uv run $P assets/raw/icon-sync.png out/icon-sync.webp --key auto --trim --pad 8 --size 256x256 --contain
uv run $P assets/raw/stone.png     out/stone.jpg      --tile --size 1024x1024
```

| Flag | Does |
| --- | --- |
| `--size WxH` (`--contain`) | Crops to fill the size, or fits inside it without cropping |
| `--logo PATH` `--logo-pos tl\|tr\|bl\|br\|bc` `--logo-width 0.18` | Pastes the real logo file into a corner, with a 5% margin |
| `--key auto\|#RRGGBB` (`--tol N`) | Makes the background colour transparent. `auto` samples the corners |
| `--trim` (`--pad N`) | Crops to the visible content |
| `--tile` | Cross-fades the edges so the image tiles seamlessly |
| output extension | `.jpg` for opaque images, `.png`/`.webp` to keep alpha |

- **Finished pieces:** crop-to-fill is safe only when the raw image already has the target ratio, because then it only trims a few pixels. If the ratios differ, regenerate at the right ratio rather than cropping, since cropping cuts off text.
- **`--logo`** only pastes the file. It doesn't look for empty space, so the prompt must have reserved that corner.
- If a project needs several of these commands, put them in a small `assets/build.sh` so the whole set can be rebuilt with one command.
- Web images: produce 2× sizes for retina, and keep JPG/WebP files reasonably small (a hero image under about 400 KB).

## 7. Proof and verify where the image is seen

The model adds things you didn't ask for (extra text, frames, borders, watermarks, cropped subjects), and occasionally misspells. Check each image with the Read tool:

**Finished pieces:**
1. **Proof every word letter by letter against the brief.** Pay most attention to numbers, prices, dates, URLs, handles, brand and product names. A wrong price or date on a published ad is the costliest kind of error here. List the copy you read back in your report.
2. **No extra text:** look for invented signage, small print or fake logos in the background.
3. **Clear zones and logo:** text stays out of the reserved areas, and a composited logo doesn't overlap the type or the subject.
4. **Legibility at feed size:** look at a 25–30% downscale (`--size` to a temporary file). The headline should still read at a glance. If it doesn't, ask for larger, bolder type with more contrast.

**Components:** check the subject, that there's no text, and for clean alpha edges with no coloured halo. Then **view it in place**: render the slide, or screenshot the page in a browser (Playwright works) at each breakpoint you ship. Check that the headline space really is empty, that crops hold at each aspect ratio, and that tiles show no seams when repeated.

If an image fails, use an edit (step 5) for small fixes. For structural problems, regenerate with a more specific prompt that names the unwanted element ("no border", "no other text", "subject fully in frame"). Give web images a fallback (a CSS background colour) so a missing file doesn't break the layout.

## 8. Report

Tell the user:
- the final files (paths, pixel sizes, formats);
- for finished pieces, the copy exactly as it appears in each image;
- what you checked, and anything you regenerated or still have doubts about;
- any limits that apply (resolution too low for print, a logo composited rather than generated).

For social posts, suggest alt text that includes the image's text, since screen readers can't read it from the pixels. Mention that the originals are in `assets/raw/` for later edits or other crops.
