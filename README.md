# 💠 Shape Survivor: A Geometry Bullet-Hell

A fast-paced PVE shooting and dodging game featuring procedural shape-based enemies, progressive waves, and a rogue-lite upgrade system.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pygame](https://img.shields.io/badge/pygame-%231572B6.svg?style=for-the-badge&logo=pygame&logoColor=white)

---

## ✨ Features
* **Geometric Combat:** A curated fusion of *Asteroids*, *Vampire Survivors*, and a Reddit-inspired shape prototype. You play as a lone circle fighting increasingly complex polygons.
* **Procedural Shapes:** Enemies are dynamically drawn using the Python `math` library, evolving from 3-sided triangles to 10-sided decagons.
* **Progressive Waves:** The environment evolves every 60 seconds, upgrading enemy speed and health to keep the challenge fresh.
* **The 90° Easter Egg:** A special Right Triangle enemy spawns every 90 seconds in honor of its 90-degree internal angle.
* **Leveling & Arsenal:** Consume EXP Gems to level up and choose upgrades like fire rate and damage to survive the onslaught.
* **Survival Tools:** Features Health Orbs for recovery and Magnet Stars to help pull in distant experience gems.
* **Immersion:** Visuals are drawn directly in the window frame, accompanied by an energetic *Invader Disco* soundtrack.

## 🚀 Getting Started
1. Clone the repository.
2. Ensure you have the `Invader Disco` audio file in your assets folder.
3. Ensure the Python `math` library and `pygame` are installed.
4. **Game Modes:** Choose between **Story Mode** to find the "weird surprise" at the end, or the **"Endless" Mode** for a longer survival challenge.
5. Run `main.py` in your terminal or IDE.

## 🛠️ Customization
The enemy spawning logic and difficulty scaling are tied to the game clock. To adjust how fast enemies grow stronger, update the scaling factors in the wave logic:

```python
# Every 60 seconds, complexity and health increase
if time_passed > 60:
    enemy_sides += 1 # Transitions from triangle to decagon
    enemy_hp *= 1.2  # Scaling difficulty
