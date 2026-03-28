import React from "react";
import { Composition } from "remotion";

const Placeholder: React.FC = () => (
  <div style={{
    background: '#050508',
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#f0654a',
    fontFamily: 'Impact',
    fontSize: 80,
    letterSpacing: '0.06em',
    flexDirection: 'column',
    gap: 8,
  }}>
    <div>DJ GIANNI</div>
    <div style={{ fontSize: 28, color: '#ededf0', opacity: 0.5 }}>RELEASE CLIP POC</div>
  </div>
);

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ReleaseClip"
      component={Placeholder}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{}}
    />
  );
};
