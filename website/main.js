
// Load the animation file.
// In this case, the spritesheet is located at assets/stick-figure.png,
// with a corresponding metadata file at assets/stick-figure.json.
Aseprite.loadImage({
  name: 'stick-figure',
  basePath: 'assets/',
});

// Turn off smoothing so the pixels stay sharp.
Aseprite.disableSmoothing(context);

// Within a game loop, do the following:
Aseprite.drawAnimation({
  context,
  image: 'stick-figure',
  animationName: 'Idle',
  time: elapsedSeconds, // Or you can use `Date.now() / 1000` if you don't want to track elapsed time.
  position: { x: 100, y: 100 },
  scale: 2,
  anchorRatios: { x: 0.5, y: 1 }, // This sets the anchor point to the bottom middle of the sprite.
});

// Or, just render a single frame:
Aseprite.drawSprite({
  context,
  image: 'stick-figure',
  frame: 0, // Frame numbers are 0-based, so this is the first frame.
  time: elapsedSeconds + 0.5,
  position: { x: 20, y: 20 },
  scale: 2,
});

console.log(Aseprite);