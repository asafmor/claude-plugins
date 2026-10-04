---
name: remotion-videos
description: "Make videos programmatically with Remotion (React → MP4): trailers, product promos, explainers, animated title cards, social clips (vertical or square), slide-style videos, README GIFs and poster frames. Use this whenever the user wants a video, trailer, teaser, promo, intro/outro, animated clip, motion graphics or GIF made from code, screenshots, generated images or captured footage, even if they don't mention Remotion. Covers scaffolding, frame-driven animation, transitions, fonts, audio, deterministic capture of app or game footage, frame-accurate verification, rendering, and ffmpeg web exports."
---

# remotion-videos

Remotion renders React components to video. A component is a function from a **frame number** to an image. Remotion screenshots every frame (in parallel browser tabs) and encodes the result. Almost every Remotion bug comes from forgetting this.

## 0. Preflight

- Node 18+ (`node --version`) and `npx`. System `ffmpeg` is only needed for the web exports in step 7.
- On Linux, Remotion needs glibc 2.35+ (`ldd --version`) and the headless-Chrome libraries listed at remotion.dev/docs/miscellaneous/linux-dependencies. If a render fails to launch the browser, that list is the first thing to check. Alpine and NixOS are unsupported.
- **Licence:** Remotion is free for individuals and companies of up to 3 people. Larger companies need a company licence (remotion.pro/license). Mention this once if the user seems to be working for a company.

## 1. Plan the video as a beat sheet before writing code

Write a table of beats, each with a duration in seconds, the on-screen content, a short caption, and the transition into it. Frame counts follow from that. Defaults that work:

- **Trailer / promo:** cold open → logo/title → 4–8 short beats with one-line captions → 2–3 feature cards → climax → call to action with the URL. 45–60 s total, 2–4 s per beat.
- **Social clip:** 1080×1920 (vertical) or 1080×1080, 10–30 s, a hook in the first second, large text inside a safe area of about 8% from each edge.
- **Explainer / slide video:** one idea per beat, give the viewer time to read (roughly 1 s per 3 words), and keep every slide the same layout.

Collect assets up front. For still images, use the `codex-image-gen` skill in this plugin, and ask for a "no text" version, because Remotion should draw all text. Source images should be at least their on-screen size, since upscaled images go soft. Music and SFX: Pixabay (no attribution), OpenGameArt/Kenney (CC0), Incompetech (CC-BY). Record CC-BY credits as you download them.

## 2. Scaffold

New standalone project (non-interactive):

```bash
npx create-video@latest --yes --blank --no-tailwind video
cd video && npm i
npx remotion add @remotion/transitions @remotion/google-fonts @remotion/media
```

Inside an existing repo, still give the video its own folder (`video/` or `trailer/`), so Remotion's dependencies stay separate from the app's. To embed Remotion in an existing React or Next app instead, follow remotion.dev/docs/brownfield. `npx remotion add` pins every `@remotion/*` package to the installed `remotion` version. Mismatched versions are a common breakage, so don't `npm i` them with `^` ranges.

**Starter template:** `assets/Trailer.tsx` in this skill's directory is a tested, data-driven trailer. It has a `BEATS` array, title and image beats, spring entrances, exit fades, alternating fade/slide transitions, a Google Font, and music with a volume fade. Copy it to `src/Trailer.tsx`, render `<TrailerComposition />` inside `RemotionRoot` in `src/Root.tsx`, put media in `public/`, and edit `BEATS`. Starting from it is much faster than starting from a blank composition.

**Deeper API reference:** Remotion publishes official agent skills covering the long tail of the API (e.g. `/remotion-docs`, `/remotion-maps`, `/remotion-markup`). They're installed into the project with `npx remotion skills add`. Suggest them to the user when the video needs something beyond this skill, and ask before installing, because they add third-party skill files to the repo.

## 3. The rules that prevent flicker and broken renders

Frames render out of order in separate tabs, so a frame's pixels must depend only on its frame number:

- **Animate only from `useCurrentFrame()`**, using `interpolate()` or `spring()`. CSS animations and transitions, `setTimeout`/`requestAnimationFrame`, GIF-like state and `Date.now()` all flicker or freeze.
- **No `Math.random()`.** Use `random("seed")` from `remotion`, which returns the same value on every frame.
- **Load assets through Remotion's components, so the renderer waits for them:** `<Img>`, `<Audio>`/`<Video>` from `@remotion/media`, `<OffthreadVideo>`. Reference files in `public/` with `staticFile("name.png")`. Avoid CSS `background-image`/`mask-image`, which aren't waited on and can render blank. For fetched data, use `delayRender()`/`continueRender()`.
- **Fonts:** load them once in a module with `loadFont("normal", { weights: [...], subsets: ["latin"] })` from `@remotion/google-fonts/<Name>`, and use the returned `fontFamily`. Always pass weights and subsets: without them every variant loads, and Remotion 5 requires them.
- `--concurrency=1` sometimes "fixes" flicker by coincidence. Fix the component instead.

## 4. Core APIs

```tsx
const frame = useCurrentFrame();
const { fps, durationInFrames, width, height } = useVideoConfig();

// Linear mapping. Always clamp, or values overshoot outside the range.
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

// Natural motion 0→1. damping: 200 = smooth, no bounce. The default bounces a little.
const enter = spring({ frame: frame - delay, fps, config: { damping: 200 } });
const y = interpolate(enter, [0, 1], [40, 0]);
```

- `<AbsoluteFill>` is a full-frame layer. Stack them for layers.
- `<Sequence from={30} durationInFrames={60}>` shifts time: children see `useCurrentFrame()` starting at 0. `<Series>` puts sequences back to back.
- Frames run from `0` to `durationInFrames - 1`.

**Transitions** (`@remotion/transitions`):

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={75}><A /></TransitionSeries.Sequence>
  <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
  <TransitionSeries.Sequence durationInFrames={90}><B /></TransitionSeries.Sequence>
</TransitionSeries>
```

- Import presentations from subpaths: `@remotion/transitions/fade`, `/slide` (`slide({ direction: "from-right" })`), `/wipe`, `/flip`, `/clock-wipe`, `/iris`. Timing comes from `linearTiming({ durationInFrames })` or `springTiming({ config: { damping: 200 }, durationInFrames })`.
- **Transitions overlap their neighbours, so they shorten the total:** total = sum(sequences) − sum(transitions). Compute `durationInFrames` that way, or the video ends early or freezes on the last frame.
- A transition must be shorter than both neighbouring sequences, and two transitions can't be adjacent.
- `<TransitionSeries.Overlay durationInFrames={20}>` draws something (a flash or light leak) over a cut without shortening the timeline.
- A crossfade stacks two full layouts on top of each other. Fade each scene's content out over its last `TRANSITION` frames (the template does this), or use `slide`/`wipe` between busy scenes.

**Audio:** `<Audio src={staticFile("music.mp3")} volume={v} />` from `@remotion/media`. Add one tag per track to mix them. For a fade, drive `volume` with a clamped `interpolate()` over the frame, never below 0. Delay an SFX by wrapping it in `<Sequence from={n}>`.

**Video clips:** use `<OffthreadVideo src={staticFile("clip.mp4")} />` (frame-accurate). Trim with `trimBefore`/`trimAfter` (in frames).

## 5. Capturing footage from a real app or game

Screen recordings stutter and can't be repeated. For smooth, repeatable footage:

1. Drive the real app with Playwright (scripted input, or a bot or autopilot for a game).
2. **Freeze real time:** stub `performance.now`/`Date.now`/`requestAnimationFrame`, step the simulation exactly `1/fps` s per frame, and screenshot each frame (`f_00001.jpg` …).
3. Encode the frames: `ffmpeg -framerate 30 -i f_%05d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p clip.mp4`. This gives smooth 30 fps footage even when headless rendering only manages 3 fps.
4. Frame for the viewer: hide or shrink the HUD with injected CSS, bring the camera closer than in normal play, and seek to interesting moments by condition (a fight, a new area, a win) rather than by fixed time.

Put clips in `public/` and use them with `<OffthreadVideo>`. Keep raw captures out of git.

## 6. Verify: look at frames, not just exit codes

A render can exit 0 and still be wrong. Check these before calling the video done:

```bash
npx tsc --noEmit                          # type errors surface here faster than in a render
npx remotion compositions                 # id, fps, size, duration: is the duration what you planned?
npx remotion still <Id> out/f.png --frame=<N> --scale=0.5
```

Render stills **at the risky frames** and look at each one with the Read tool:

- the middle of every transition (overlapping layouts, ghosted text);
- each beat at its peak (text fully in, nothing clipped or overlapping images, captions readable against the background);
- the **last frame**, `durationInFrames - 1` (the call to action is visible and nothing is cut off). `--frame` beyond the end throws.

Several stills combined into one contact-sheet image (Pillow) are quicker to review. A human can scrub the whole video in `npx remotion studio`, so suggest it to the user for the final review. After rendering, confirm an audio track exists if the video should have one: `ffprobe -v error -show_entries stream=codec_type -of csv=p=0 out/video.mp4`.

## 7. Render and export

```bash
npx remotion render <Id> out/video.mp4 --codec h264 --crf 18
```

Useful flags: `--frames=0-89` for a quick partial render, `--scale=0.5` for fast drafts, `--props='{"title":"x"}'` (or a JSON file path) for input props, `--muted`, `--concurrency=N`, `--codec prores` / `vp9` / `gif`, `--sequence` for an image sequence.

Then make the web deliverables from the master render:

```bash
# Web MP4: smaller, starts playing before it finishes downloading
ffmpeg -y -i out/video.mp4 -vf "scale=1600:-2" -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart out/video-web.mp4
# README/preview GIF: aim for under 5 MB (lower fps/width if larger)
ffmpeg -y -i out/video.mp4 -vf "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer" out/preview.gif
# Poster frame for <video poster=…> and social cards
ffmpeg -y -ss 3.5 -i out/video.mp4 -frames:v 1 -q:v 2 out/poster.jpg
```

- On GitHub, the README can't play repo videos inline. Show the GIF and link it to the MP4 hosted on Pages.
- Commit only the final media, never `out/` drafts or raw captures.
- Credit the music and any CC-BY assets in a `CREDITS.md`.

## 8. Report

Tell the user the composition id, length and resolution; the output files with their sizes; which frames you checked and what you fixed; the music credits; and how to tweak it (edit `BEATS`, run `npx remotion studio` to preview, re-run the render command).
