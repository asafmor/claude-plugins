// Starter trailer: copy into src/, register <TrailerComposition /> in src/Root.tsx,
// put media in public/, then edit BEATS. Needs:
//   npx remotion add @remotion/transitions @remotion/google-fonts @remotion/media
import { Audio } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/Inter";
import { linearTiming, TransitionSeries } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import {
  AbsoluteFill,
  Composition,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const { fontFamily } = loadFont("normal", { weights: ["400", "800"], subsets: ["latin"] });

const FPS = 30;
const TRANSITION = 15; // frames; must be shorter than both neighbouring beats
const MUSIC: string | null = "music.mp3"; // file in public/, or null

type Beat =
  | { kind: "title"; text: string; sub?: string; bg: string; seconds: number }
  | { kind: "image"; src: string; caption?: string; bg: string; seconds: number };

// One idea per beat. Keep captions to a few words; viewers get ~2 s to read them.
const BEATS: Beat[] = [
  { kind: "title", text: "Last Train North", sub: "A survival run across the tundra", bg: "#1f6f6a", seconds: 2.5 },
  { kind: "image", src: "train.webp", caption: "Keep the engine alive", bg: "#14141e", seconds: 3 },
  { kind: "title", text: "Play free", sub: "example.github.io/last-train-north", bg: "#e07b39", seconds: 3 },
];

const frames = (s: number) => Math.round(s * FPS);
const DURATION = BEATS.reduce((sum, b) => sum + frames(b.seconds), 0) - TRANSITION * (BEATS.length - 1);

// Fade content out over the last frames of a beat, so a crossfade never stacks two layouts.
const useExit = (length: number) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [length - TRANSITION, length], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
};

const useEnter = (delay = 0) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - delay, fps, config: { damping: 200 } }); // damping 200 = no bounce
};

const Title: React.FC<{ beat: Extract<Beat, { kind: "title" }>; length: number; last: boolean }> = ({ beat, length, last }) => {
  const enter = useEnter();
  const sub = useEnter(8);
  const exit = useExit(length);
  const out = last ? 1 : exit; // the final beat holds instead of fading
  return (
    <AbsoluteFill style={{ backgroundColor: beat.bg, justifyContent: "center", alignItems: "center", fontFamily, color: "white" }}>
      <div style={{ opacity: enter * out, transform: `translateY(${interpolate(enter, [0, 1], [40, 0])}px)`, fontSize: 110, fontWeight: 800 }}>
        {beat.text}
      </div>
      {beat.sub && <div style={{ opacity: sub * out, fontSize: 44, marginTop: 24 }}>{beat.sub}</div>}
    </AbsoluteFill>
  );
};

const ImageBeat: React.FC<{ beat: Extract<Beat, { kind: "image" }>; length: number }> = ({ beat, length }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, length], [1, 1.12]); // slow Ken Burns push-in
  const caption = useEnter(10) * useExit(length);
  return (
    <AbsoluteFill style={{ backgroundColor: beat.bg, justifyContent: "center", alignItems: "center", fontFamily }}>
      <Img src={staticFile(beat.src)} style={{ width: "70%", height: "62%", marginBottom: beat.caption ? 160 : 0, objectFit: "contain", transform: `scale(${scale})` }} />
      {beat.caption && (
        <div style={{ position: "absolute", bottom: 90, fontSize: 64, fontWeight: 800, color: "white", opacity: caption }}>
          {beat.caption}
        </div>
      )}
    </AbsoluteFill>
  );
};

export const Trailer: React.FC = () => {
  const frame = useCurrentFrame();
  const volume = interpolate(frame, [0, 15, DURATION - 30, DURATION], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <TransitionSeries>
        {BEATS.flatMap((beat, i) => {
          const length = frames(beat.seconds);
          const scene = (
            <TransitionSeries.Sequence key={`s${i}`} durationInFrames={length}>
              {beat.kind === "title" ? <Title beat={beat} length={length} last={i === BEATS.length - 1} /> : <ImageBeat beat={beat} length={length} />}
            </TransitionSeries.Sequence>
          );
          if (i === 0) return [scene];
          return [
            <TransitionSeries.Transition
              key={`t${i}`}
              presentation={i % 2 ? fade() : slide({ direction: "from-right" })}
              timing={linearTiming({ durationInFrames: TRANSITION })}
            />,
            scene,
          ];
        })}
      </TransitionSeries>
      {MUSIC && <Audio src={staticFile(MUSIC)} volume={volume} />}
    </AbsoluteFill>
  );
};

export const TrailerComposition: React.FC = () => (
  <Composition id="Trailer" component={Trailer} durationInFrames={DURATION} fps={FPS} width={1920} height={1080} />
);
