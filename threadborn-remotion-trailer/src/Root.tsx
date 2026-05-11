import {Composition} from 'remotion';
import {ThreadbornTrailer} from './ThreadbornTrailer';

export const TRAILER_FPS = 30;
export const TRAILER_DURATION = 58 * TRAILER_FPS;

export const RemotionRoot = () => {
  return (
    <Composition
      id="ThreadbornTrailer"
      component={ThreadbornTrailer}
      durationInFrames={TRAILER_DURATION}
      fps={TRAILER_FPS}
      width={1920}
      height={1080}
    />
  );
};
