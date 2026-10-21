# Roadmap

## M2D migration

- Move rendering, player movement, platform collisions and scrolling to [M2D](https://github.com/mert574/m2d-engine).
- Preserve double jumps and scoring while tuning the migrated controls and physics.
- Replace frame-dependent movement and the hardcoded time step with elapsed-time updates so physics, scrolling and difficulty stay consistent across refresh rates.
- Update development dependencies and add a build workflow through `package.json`.

## Controls and game flow

- Add touch controls and responsive canvas sizing.
- Add a main menu, pause controls and an end-game menu with score, restart and return options.
- Make restarting reset the player, platforms and camera consistently.
- Add music and sound controls.

## Gameplay and presentation

- Add moving and breakable platforms, jump boosts and collectible items.
- Tune platform spacing and difficulty progression to keep routes reachable.
- Improve character animation, landing feedback and background presentation.
- Redesign the surrounding page, including layout, typography, colors, score display and control instructions, for desktop and mobile.
