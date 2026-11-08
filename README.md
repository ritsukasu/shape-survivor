<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/PYTHON-3670A0?style=for-the-badge&amp;logo=python&amp;logoColor=ffdd54">
  <img alt="Pygame" src="https://img.shields.io/badge/PYGAME-1572B6?style=for-the-badge&amp;logo=pygame&amp;logoColor=white">
  <img alt="Genre" src="https://img.shields.io/badge/GENRE-BULLET--HELL-ff0055?style=for-the-badge">
</p>

```text
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

   ▲  ■  ⬟  ⬢  ⬣  ◆      S H A P E      ●
                          S U R V I V O R

▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
```

<p align="center">
  <strong>A GEOMETRY BULLET-HELL</strong><br>
  Shoot. Dodge. Level up. Survive the polygons.
</p>

<p align="center">
  <img alt="Shape Survivor gameplay" src="screenshot.png" width="100%">
</p>

```text
 1UP            HI-SCORE            WAVE
 ●              ??????              01
```

You are a lone circle. Everything else is a polygon, and every minute it gets worse. Blast shapes, grab EXP gems, pick an upgrade each level and see how long you last. Think *Asteroids* meets *Vampire Survivors*, with a Reddit-inspired shape prototype in the mix.

## ▶ PRESS START

You need Python 3 and Pygame.

```bash
git clone https://github.com/yourusername/shape-survivor.git
cd shape-survivor
pip install pygame
python main.py
```

## ▶ ENEMY ROSTER

Enemies are drawn in code with Python's `math` library, so each one is a procedurally generated polygon. They start with 3 sides and climb to 10.

| Sides | Enemy |
| :---: | --- |
| 3 | Triangle |
| 4 | Square |
| 5 | Pentagon |
| 6 | Hexagon |
| 7 | Heptagon |
| 8 | Octagon |
| 9 | Nonagon |
| 10 | Decagon |

> **BONUS ENEMY:** a **right triangle** spawns every **90 seconds**, in honor of its 90° angle.

## ▶ GAME RULES

| Mechanic | What it does |
| --- | --- |
| **Waves** | Every 60 seconds the world levels up, and enemies get faster and tougher. |
| **EXP gems** | Collect them to level up and pick an upgrade. |
| **Upgrades** | Boost things like fire rate and damage. |
| **Health orbs** | Restore your health. |
| **Magnet stars** | Pull in distant EXP gems. |

## ▶ SOUND AND VISUALS

All graphics are drawn directly in the game window, backed by an energetic *Invader Disco* soundtrack.

## ▶ BUILT WITH

- [Python](https://www.python.org)
- [Pygame](https://www.pygame.org)

## ▶ LICENSE

No license has been added yet.

```text
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
              THANKS FOR PLAYING
                  GAME  OVER
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
```
