<h1 align="center">● Shape Survivor ▲</h1>

<p align="center">
  <sub>▲ &nbsp; ■ &nbsp; ⬟ &nbsp; ⬢ &nbsp; ⬣ &nbsp; ◆ &nbsp; ⬠ &nbsp; ● &nbsp; ▲ &nbsp; ■ &nbsp; ⬟ &nbsp; ⬢ &nbsp; ⬣ &nbsp; ◆</sub>
</p>

<p align="center">
  <strong>A geometry bullet-hell.</strong><br>
  A fast-paced PvE shooting and dodging game with procedural shape-based enemies, progressive waves and a rogue-lite upgrade system.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3670A0?logo=python&amp;logoColor=ffdd54">
  <img alt="Pygame" src="https://img.shields.io/badge/Pygame-1572B6?logo=pygame&amp;logoColor=white">
  <img alt="Genre: bullet hell" src="https://img.shields.io/badge/genre-bullet--hell-blueviolet">
</p>

You play a lone circle against polygons that grow more complex as the game goes on. Shoot, dodge, collect experience gems and pick an upgrade each time you level up. The game blends *Asteroids*, *Vampire Survivors* and a Reddit-inspired shape prototype.

## Quick start

**Requirements:** Python 3 and Pygame.

```bash
git clone https://github.com/yourusername/shape-survivor.git
cd shape-survivor
pip install pygame
python main.py
```

## Features

- **Geometric combat:** fight increasingly complex polygons as a single circle.
- **Procedural enemies:** shapes are drawn in code with Python's `math` library and range from 3-sided triangles to 10-sided decagons.
- **Progressive waves:** every 60 seconds the environment evolves, raising enemy speed and health.
- **Leveling and upgrades:** collect EXP gems to level up and choose upgrades such as fire rate and damage.
- **Pickups:** health orbs restore health, and magnet stars pull in distant EXP gems.
- **Special enemy:** a right triangle spawns every 90 seconds, a nod to its 90-degree angle.
- **Presentation:** all visuals are drawn directly in the game window, with an *Invader Disco* soundtrack.

## Enemy shapes

Enemies start simple and gain a side with each tier, up to ten.

| Sides | Shape | |
| :---: | --- | :---: |
| 3 | Triangle | ▲ |
| 4 | Square | ■ |
| 5 | Pentagon | ⬟ |
| 6 | Hexagon | ⬢ |
| 7 | Heptagon | ⬣ |
| 8 | Octagon | ⯄ |
| 9 | Nonagon | ◉ |
| 10 | Decagon | ● |

A **right triangle** (◣) also appears every 90 seconds.

## Built with

- [Python](https://www.python.org)
- [Pygame](https://www.pygame.org)

## License

No license has been added yet.
