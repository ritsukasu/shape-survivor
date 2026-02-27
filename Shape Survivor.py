import pygame
import random
import math
import sys

# variables
# frame
screenWidth = 900
screenHeight = 650
fps = 60

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0) 
darkRed = (150, 0, 0)
yellow = (255, 255, 0) 
green = (0, 255, 0)

# game states
stateIntro = 'intro'
stateMenu = 'menu'
statePlaying = 'playing'
statePaused = 'paused'      
stateLevelUp = 'levelUp'
stateGameOver = 'gameOver'
stateCredits = 'credits'
stateVictoryScreen = 'victoryScreen' 
stateCutscene = 'cutscene'

# player settings
playerSpeed = 5 
playerSize = 15
lineThickness = 2

# enemy and difficulty settings
# this is where we adjust the general enemy size range
enemyMinSize = 18
enemyMaxSize = 45
enemyBaseSpeed = 0.8 
enemySpeedMultiplier = 0.39

# bullet settings
bulletSize = 4
bulletSpeed = 10 
# this is where we adjust player's base fire rate
bulletCooldown = 300 

# exp settings
# this is where we adjust the exp size
expSize = 8

# power-up settings
# this is where we adjust the health orb size
healthOrbSize = 12
# this is where we adjust the health orb spawn time
healthOrbSpawnDelay = 20000 
# this is where we adjust the magnet star size
magnetStarSize = 12
# this is where we adjust the magnet star spawn time
magnetStarSpawnDelay = 15000 
# this is where we adjust the magnet star duration
magnetStarDuration = 5000 

# score thresholds for new enemy shapes
# this is where we adjust the shape timeline for story mode
shapeTimelineStory = {
    # this is where we adjust the shape timeline
    60: 4,
    120: 5, 
    180: 6, 
    240: 7, 
    300: 8, 
    360: 9, 
} 
# this is where we adjust the shape timeline for endless mode (10 minutes per shape)
shapeTimelineEndless = {
    300: 4, #5 mins
    600: 5, #10 mins
    900: 6, #15 mins
    1200: 7, #20 mins
    1500: 8, #25 mins
    1800: 9, #30 mins
}
# this is where we adjust when the final wave starts
finalWaveStartScore = 420.0 
# this is where we adjust when the final boss starts
finalBossStartScore = 450.0 
# this is where we adjust the score when the game ends
gameEndScore = 500.0 

# spawn control (milliseconds) 
# this is where we adjust the initial spawn delay
initialSpawnDelay = 1500
# this is where we adjust the minimum spawn delay
minSpawnDelay = 220
# this is where we adjust the spawn acceleration rate
spawnAcceleration = 0.98
# this is where we adjust the exp triangle spawn time
expTriangleSpawnDelay = 90000 # right triangle is 90 degrees :DD weird math reference  

#logo
gameLogo = pygame.image.load('Shape Survivor Logo.png')

# pygame initialize
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Shape Survivor (O.O)')
pygame.display.set_icon(gameLogo)
gameClock = pygame.time.Clock()

# font variables
fontFile = 'Pix32.ttf'
try:
    fontBig = pygame.font.Font(fontFile, 44)
    fontMed = pygame.font.Font(fontFile, 26)
    fontSmall = pygame.font.Font(fontFile, 18)
except pygame.error:
    fontBig = pygame.font.SysFont('Consolas', 44, bold=True)
    fontMed = pygame.font.SysFont('Consolas', 26, bold=True)
    fontSmall = pygame.font.SysFont('Consolas', 18, bold=True)


# sound variables
try:
    soundFire = pygame.mixer.Sound('fire.wav')
    soundFire.set_volume(0.3)
    soundVictory = pygame.mixer.Sound('victory.mp3') 
    soundVictory.set_volume(0.5)
    soundFahh = pygame.mixer.Sound('fahh.mp3') 
    soundFahh.set_volume(0.6)
    pygame.mixer.music.load('bgm.mp3')
    musicLoaded = True
    pygame.mixer.music.set_volume(0.3)
except pygame.error as e:
    print(f"warning: audio file not loaded. error: {e}")
    musicLoaded = False


# utility functions
def clamp(v, a, b):
    return max(a, min(b, v))

def circleCollision(x1, y1, r1, x2, y2, r2):
    dX = x1 - x2
    dY = y1 - y2
    return dX*dX + dY*dY <= (r1 + r2) * (r1 + r2)

def pointInPolygon(x, y, points):
    n = len(points)
    inside = False
    p1X, p1Y = points[0]
    for i in range(n + 1):
        p2X, p2Y = points[i % n]
        if y > min(p1Y, p2Y):
            if y <= max(p1Y, p2Y):
                if x <= max(p1X, p2X):
                    if p1Y != p2Y:
                        xInters = (y - p1Y) * (p2X - p1X) / (p2Y - p1Y) + p1X
                    if p1X == p2X or x <= xInters:
                        inside = not inside
        p1X, p1Y = p2X, p2Y
    return inside

# game classes (player, enemies, etc.)
class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.size = playerSize
        self.alive = True
        self.hp = 3 
        self.maxHp = 3 
        
        self.shotSpeed = bulletCooldown
        self.bulletDamage = 1.5 
        self.bulletCount = 1 
        self.lastShotTime = 0
        self.movementSpeed = playerSpeed
        self.magnetRadius = 0 
        
        self.exp = 0
        self.level = 1
        # this is where we adjust exp to level up
        self.expToNextLevel = 100 
    
    def takeDamage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False

    def update(self, keys):
        dX = 0
        dY = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: dX -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dX += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]: dY -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: dY += 1
            
        if dX != 0 or dY != 0:
            dist = math.hypot(dX, dY)
            if dist != 0:
                dX = dX / dist
                dY = dY / dist
            self.x += dX * self.movementSpeed
            self.y += dY * self.movementSpeed
            
        margin = 6
        self.x = clamp(self.x, margin + self.size, screenWidth - margin - self.size)
        self.y = clamp(self.y, margin + self.size, screenHeight - margin - self.size)

    def draw(self, surface):
        now = pygame.time.get_ticks()
        pygame.draw.circle(surface, black, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, green, (int(self.x), int(self.y)), self.size, lineThickness)
        
        ringSize = self.size + 4
        ringAlpha = 100 * (math.sin(now / 150.0) * 0.5 + 0.5) + 50
        ringColor = green + (int(ringAlpha),)
        
        tempSurface = pygame.Surface((ringSize*2, ringSize*2), pygame.SRCALPHA)
        pygame.draw.circle(tempSurface, ringColor, (ringSize, ringSize), ringSize, 1)
        surface.blit(tempSurface, (self.x - ringSize, self.y - ringSize))


    def gainExp(self, amount):
        self.exp += amount
        if self.exp >= self.expToNextLevel:
            self.levelUp()

    def levelUp(self):
        global state
        self.level += 1
        self.exp -= self.expToNextLevel
        # this is where we adjust the exp multiplier when level up
        self.expToNextLevel = int(self.expToNextLevel * 1.5) 
        state = stateLevelUp

class Enemy:
    def __init__(self, playerX, playerY, sides, currentSpeed, score, enemyHpWaveMultiplier): 
        self.size = random.randint(enemyMinSize, enemyMaxSize)
        
        edge = random.randint(0, 3)
        if edge == 0: self.x, self.y = random.randint(self.size, screenWidth - self.size), -self.size
        elif edge == 1: self.x, self.y = random.randint(self.size, screenWidth - self.size), screenHeight + self.size
        elif edge == 2: self.x, self.y = -self.size, random.randint(self.size, screenHeight - self.size)
        else: self.x, self.y = screenWidth + self.size, random.randint(self.size, screenHeight - self.size)
            
        self.sides = sides 
        # this is where we adjust the enemy hp
        self.hp = int(max(1, sides - 2) * enemyHpWaveMultiplier + 1)
        self.maxHp = self.hp
        
        speed = currentSpeed + random.random() * 0.5 
        
        angle = math.atan2(playerY - self.y, playerX - self.x)
        self.vX = math.cos(angle) * speed
        self.vY = math.sin(angle) * speed
        
        self.angle = random.random() * 360
        self.spin = (random.random() - 0.5) * 4
        self.fillColor = black
        
        hpRatio = self.hp / self.maxHp
        r = int(255)
        g = int(255 * hpRatio)
        b = int(255 * hpRatio)
        self.outlineColor = (r, g, b)

    def update(self, dT):
        self.x += self.vX * dT
        self.y += self.vY * dT
        self.angle += self.spin * dT
        
    def draw(self, surface):
        points = []
        for i in range(self.sides):
            a = math.radians(self.angle + i * 360 / self.sides)
            r = self.size
            pX = int(self.x + math.cos(a) * r)
            pY = int(self.y + math.sin(a) * r)
            points.append((pX, pY))
            
        if len(points) >= 3:
            pygame.draw.polygon(surface, self.fillColor, points) 
            
            hpRatio = clamp(self.hp / self.maxHp, 0, 1)
            
            if hpRatio < 0.3 and pygame.time.get_ticks() % 200 < 100:
                outlineColor = red
            else:
                outlineColor = white
                
            pygame.draw.polygon(surface, outlineColor, points, lineThickness)

    def isOnScreen(self):
        """checks if enemy is near screen bounds."""
        margin = self.size + 10
        return (self.x > -margin and self.x < screenWidth + margin and
                self.y > -margin and self.y < screenHeight + margin)

class ExpTriangle(Enemy):
    def __init__(self, playerX, playerY, currentSpeed):
        self.sides = 3 
        self.size = 25
        
        edge = random.randint(0, 3)
        if edge == 0: self.x, self.y = random.randint(self.size, screenWidth - self.size), -self.size
        elif edge == 1: self.x, self.y = random.randint(self.size, screenWidth - self.size), screenHeight + self.size
        elif edge == 2: self.x, self.y = -self.size, random.randint(self.size, screenHeight - self.size)
        else: self.x, self.y = screenWidth + self.size, random.randint(self.size, screenHeight - self.size)
        
        # this is where we adjust the exp triangle hp
        self.hp = 5 
        self.maxHp = 5
        # this is where we adjust the exp value
        self.expValue = 2000 
        
        speed = currentSpeed * 1.5 + random.random() * 1.0 
        angle = math.atan2(playerY - self.y, playerX - self.x)
        self.vX = math.cos(angle) * speed
        self.vY = math.sin(angle) * speed
        
        self.angle = random.random() * 360
        # this is where we adjust the spin rate
        self.spin = (random.random() - 0.5) * 8 
        self.fillColor = black 
        self.outlineColor = yellow 
        
    def draw(self, surface):
        angleRad = math.radians(self.angle)
        r = self.size
        
        # calculate points for a right triangle shape
        points = [
            (self.x + r * math.cos(angleRad), 
             self.y + r * math.sin(angleRad)),
            (self.x + r * math.cos(angleRad + math.pi/2), 
             self.y + r * math.sin(angleRad + math.pi/2)),
            (self.x + math.sqrt(2) * r * math.cos(angleRad + 3*math.pi/4),
             self.y + math.sqrt(2) * r * math.sin(angleRad + 3*math.pi/4))
        ]
        
        points = [(int(p[0]), int(p[1])) for p in points]
        
        if len(points) >= 3:
            # draws the triangle
            pygame.draw.polygon(surface, self.outlineColor, points, lineThickness)

class DecagonBoss(Enemy):
    def __init__(self, playerX, playerY, currentSpeed, waveSides):
        # this is where we adjust the size of the decagon
        self.size = 150 
        self.sides = 10 
        self.x = screenWidth // 2
        self.y = -self.size * 3 
        
        # this is where we adjust the decagon hp
        self.hp = 10000 
        self.maxHp = self.hp
        
        # this is where we adjust the speed of the decagon
        self.speed = currentSpeed * 0.85
        
        angle = math.atan2(playerY - self.y, playerX - self.x)
        self.vX = math.cos(angle) * self.speed
        self.vY = math.sin(angle) * self.speed
        
        self.angle = 0
        # this is where we adjust the spin of the decagon
        self.spin = 0.5
        self.fillColor = black 
        self.outlineColor = green
        
        # custom properties for cutscene movement
        self.targetY = screenHeight // 2 
        self.entering = True
        
        # laser properties for story mode final boss
        self.isFinalBoss = True
        self.lastLaserTime = pygame.time.get_ticks()
        # this is where we adjust the laser cooldown
        self.laserCooldown = 10000 #10 secs fire rate for laser 
        # this is where we adjust the laser warning duration
        self.laserWarningDuration = 3000 #3 secs warning

    def shootLaser(self, player):
        now = pygame.time.get_ticks()
        # only shoot if it's the final boss, it's playing, and cooldown is ready
        if self.isFinalBoss and now - self.lastLaserTime > self.laserCooldown and state == statePlaying:
            self.lastLaserTime = now
            
            num_lasers = 10
            base_angle_rad = math.radians(self.angle)
            
            for i in range(num_lasers):
                angle_offset_rad = i * (2 * math.pi / num_lasers)
                current_angle = base_angle_rad + angle_offset_rad
                
                # laser starts from the boss's edge
                startX = self.x + math.cos(current_angle) * (self.size + 10)
                startY = self.y + math.sin(current_angle) * (self.size + 10)
                
                # laser extends past the screen bounds
                endX = self.x + math.cos(current_angle) * screenWidth * 1.5
                endY = self.y + math.sin(current_angle) * screenHeight * 1.5
                
                lasers.append(Laser(startX, startY, endX, endY, self.laserWarningDuration))

    def update(self, dT):
        
        if state == stateCutscene and self.entering:
            moveSpeed = 1.0 
            if self.y < self.targetY:
                self.y += moveSpeed * dT
            else:
                self.y = self.targetY
                self.entering = False 

            self.vX = 0
            self.vY = 0
            self.angle += self.spin * dT

        elif state == statePlaying or state == stateCutscene: 
            targetX = player.x
            targetY = player.y
            
            angle = math.atan2(targetY - self.y, targetX - self.x)
            
            followMultiplier = 0.05 
            
            self.vX = self.vX * (1 - followMultiplier) + (math.cos(angle) * self.speed) * followMultiplier
            self.vY = self.vY * (1 - followMultiplier) + (math.sin(angle) * self.speed) * followMultiplier
            
            self.x += self.vX * dT
            self.y += self.vY * dT
            self.angle += self.spin * dT
    
    def draw(self, surface):
        points = []
        for i in range(self.sides):
            a = math.radians(self.angle + i * 360 / self.sides)
            r = self.size
            pX = int(self.x + math.cos(a) * r)
            pY = int(self.y + math.sin(a) * r)
            points.append((pX, pY))
            
        if len(points) >= 3:
            pygame.draw.polygon(surface, self.fillColor, points) 
            
            hpRatio = clamp(self.hp / self.maxHp, 0, 1)
            
            outlineColor = white
            if self.hp < self.maxHp and pygame.time.get_ticks() % 100 < 50:
                 outlineColor = red

            pygame.draw.polygon(surface, outlineColor, points, lineThickness * 2) 
            
            if state != stateCutscene:
                barW = 100
                barH = 8
                barX = self.x - barW // 2
                barY = self.y - self.size - barH - 10
                
                pygame.draw.rect(surface, black, (barX, barY, barW, barH))
                pygame.draw.rect(surface, white, (barX, barY, barW * hpRatio, barH))
                pygame.draw.rect(surface, white, (barX, barY, barW, barH), 1)

class MenuEnemy(Enemy):
    def __init__(self):
        self.size = random.randint(enemyMinSize, enemyMaxSize)
        self.sides = random.randint(3, 7)
        self.hp = 1 
        self.maxHp = 1 
        
        self.x = screenWidth + self.size
        self.y = random.randint(self.size, screenHeight - self.size)
        
        self.spin = (random.random() - 0.5) * 4
        self.angle = random.random() * 360
        self.fillColor = black 
        self.outlineColor = white
        
        speed = 0.5 + random.random() * 1.0 
        self.vX = -speed
        self.vY = (random.random() - 0.5) * 0.5 
        
    def update(self, dT):
        self.x += self.vX * dT
        self.y += self.vY * dT
        self.angle += self.spin * dT
    
    def isOffScreen(self):
        return self.x < -self.size
        
class Bullet:
    def __init__(self, x, y, targetX, targetY, damage):
        self.x = float(x)
        self.y = float(y)
        self.size = bulletSize
        self.damage = damage
        
        angle = math.atan2(targetY - y, targetX - x)
        self.vX = math.cos(angle) * bulletSpeed
        self.vY = math.sin(angle) * bulletSpeed

    def update(self, dT):
        self.x += self.vX * dT
        self.y += self.vY * dT

    def draw(self, surface):
        pygame.draw.circle(surface, white, (int(self.x), int(self.y)), self.size)

    def isOnScreen(self):
        return 0 < self.x < screenWidth and 0 < self.y < screenHeight

class ExpGem:
    def __init__(self, x, y, amount):
        self.x = float(x)
        self.y = float(y)
        self.size = expSize
        self.amount = amount
        self.collected = False

    def update(self, playerX, playerY, magnetRadius=0):
        # this is where we adjust the pull distance
        pullDistance = 60 + magnetRadius
        # this is where we adjust the attraction speed
        attractionSpeed = 4 
        
        dX = playerX - self.x
        dY = playerY - self.y
        dist = math.hypot(dX, dY)
        
        if dist < pullDistance:
            if dist != 0:
                self.x += (dX / dist) * attractionSpeed
                self.y += (dY / dist) * attractionSpeed
    
    def draw(self, surface):
        points = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y),
        ]
        pygame.draw.polygon(surface, black, points)
        pygame.draw.polygon(surface, white, points, 1)

class HealthOrb: 
    def __init__(self):
        self.x = random.randint(50, screenWidth - 50)
        self.y = random.randint(50, screenHeight - 50)
        self.size = healthOrbSize
        self.alive = True

    def update(self, playerX, playerY, magnetRadius=0):
        # this is where we adjust the pull distance
        pullDistance = 60 + magnetRadius * 1.5 
        # this is where we adjust the attraction speed
        attractionSpeed = 4 
        
        dX = playerX - self.x
        dY = playerY - self.y
        dist = math.hypot(dX, dY)
        
        if dist < pullDistance:
            if dist != 0:
                self.x += (dX / dist) * attractionSpeed
                self.y += (dY / dist) * attractionSpeed

    def draw(self, surface):
        pygame.draw.circle(surface, white, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, black, (int(self.x), int(self.y)), self.size, 1)

class MagnetStar: 
    def __init__(self):
        self.x = random.randint(50, screenWidth - 50)
        self.y = random.randint(50, screenHeight - 50)
        self.size = magnetStarSize
        self.alive = True

    def draw(self, surface):
        points = []
        for i in range(5):
            angle = i * 2 * math.pi / 5 - math.pi / 2
            x = self.x + self.size * math.cos(angle)
            y = self.y + self.size * math.sin(angle)
            points.append((x, y))

            angle = i * 2 * math.pi / 5 - math.pi / 2 + math.pi / 5
            x = self.x + self.size * 0.4 * math.cos(angle)
            y = self.y + self.size * 0.4 * math.sin(angle)
            points.append((x, y))

        if len(points) >= 3:
            pygame.draw.polygon(surface, white, points)
            pygame.draw.polygon(surface, black, points, 1)

class Particle:
    def __init__(self, x, y, particleColor=white): 
        self.x = float(x)
        self.y = float(y)
        # this is where we adjust the particle speed
        self.vX = (random.random() - 0.5) * 6 
        self.vY = (random.random() - 0.5) * 6 
        # this is where we adjust the particle life
        self.life = random.randint(20, 50) 
        # this is where we adjust the particle size
        self.size = random.randint(2, 5)
        self.color = particleColor 

    def update(self):
        self.x += self.vX
        self.y += self.vY
        # this is where we adjust the gravity
        self.vY += 0.12 
        self.life -= 1

    def draw(self, surface):
        alpha = clamp(int(255 * (self.life / 50)), 0, 255)
        
        tempSurface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        particleColorWithAlpha = (self.color[0], self.color[1], self.color[2], alpha)
        
        pygame.draw.circle(tempSurface, particleColorWithAlpha, (self.size, self.size), self.size)
        surface.blit(tempSurface, (self.x - self.size, self.y - self.size))

class Laser:
    def __init__(self, startX, startY, endX, endY, warningDuration=1000):
        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        # this is where we adjust the warning duration
        self.warningDuration = warningDuration 
        # this is where we adjust the active duration
        self.activeDuration = 200 
        self.spawnTime = pygame.time.get_ticks()
        self.state = 'warning'
        self.damage = 1 

    def update(self):
        now = pygame.time.get_ticks()
        if self.state == 'warning' and now > self.spawnTime + self.warningDuration:
            self.state = 'active'
        elif self.state == 'active' and now > self.spawnTime + self.warningDuration + self.activeDuration:
            self.state = 'dead' 
    
    def draw(self, surface):
        now = pygame.time.get_ticks()
        if self.state == 'warning':
            flash = now % 300 < 150 
            if flash:
                # Set laser width to 5 for warning state
                pygame.draw.line(surface, white, (int(self.startX), int(self.startY)), 
                                 (int(self.endX), int(self.endY)), 5)
        elif self.state == 'active':
            # Set laser width to 5 for active state
            pygame.draw.line(surface, white, (int(self.startX), int(self.startY)), 
                                 (int(self.endX), int(self.endY)), 5)
            if random.random() < 0.2:
                particles.append(Particle(self.endX, self.endY, particleColor=white))

    def isColliding(self, player):
        if self.state != 'active':
            return False
        
        dx = self.endX - self.startX
        dy = self.endY - self.startY
        lengthSq = dx*dx + dy*dy
        
        if lengthSq == 0:
            return circleCollision(self.startX, self.startY, 1, player.x, player.y, player.size)

        t = ((player.x - self.startX) * dx + (player.y - self.startY) * dy) / lengthSq
        t = clamp(t, 0, 1) 
        
        closestX = self.startX + t * dx
        closestY = self.startY + t * dy
        
        distSq = (player.x - closestX)**2 + (player.y - closestY)**2
        
        return distSq <= player.size**2

# utility function to update endless high scores
def updateEndlessHighScores(newScore): # this is where we update the endless mode leaderboard
    global endlessHighScores
    endlessHighScores.append(newScore)
    endlessHighScores.sort(reverse=True)
    endlessHighScores = endlessHighScores[:3]

def playerShoot(player, bulletsList): # changed to camelCase
    now = pygame.time.get_ticks()
    if now - player.lastShotTime > player.shotSpeed:
        player.lastShotTime = now
        
        if musicLoaded: soundFire.play()

        targetableEnemies = [
            e for e in enemies 
            if 0 < e.x < screenWidth and 0 < e.y < screenHeight
        ]

        if targetableEnemies:
            nearestEnemy = min(targetableEnemies, key=lambda e: math.hypot(e.x - player.x, e.y - player.y))
            
            for i in range(player.bulletCount):
                # this is where we adjust the spread of the bullets
                angleOffset = (i - (player.bulletCount - 1) / 2) * math.radians(15) 
                baseAngle = math.atan2(nearestEnemy.y - player.y, nearestEnemy.x - player.x)
                targetAngle = baseAngle + angleOffset
                
                targetX = player.x + math.cos(targetAngle) * screenWidth
                targetY = player.y + math.sin(targetAngle) * screenWidth
                
                bulletsList.append(Bullet(player.x, player.y, targetX, targetY, player.bulletDamage))


# game state variables
player = Player(screenWidth // 2, screenHeight - 120)
enemies = []
menuEnemies = [] 
bullets = []
expGems = []
healthOrbs = [] 
magnetStars = [] 
particles = []
lasers = [] 

state = stateIntro
spawnDelay = initialSpawnDelay
lastSpawnTime = 0
lastExpTriangleSpawnTime = 0 
currentEnemySpeed = enemyBaseSpeed 
startTime = None
score = 0.0
highScore = 0.0
menuEnemySpawnTime = 0 

lastHealthOrbSpawnTime = 0 
lastMagnetStarSpawnTime = 0 
magnetStartTime = 0

# endless mode variables
isEndlessMode = False # this is the flag for the endless mode
# this is where we store the top 3 longest endless mode times (in seconds)
endlessHighScores = [0.0, 0.0, 0.0] 

# game win variables
finalWaveActive = False
finalBossActive = False 
gameWon = False
victorySoundPlayed = False
victoryFadeAlpha = 0

# cutscene variables
# this is where we adjust the cutscene duration
cutsceneDuration = 8000 
cutsceneStartTime = 0
bossDialogue = "Hello Father!" 
playerDialogue = "FAHHHH" 
# this is where we adjust the boss dialogue start time
bossDialogueStart = 500
# this is where we adjust the player dialogue start time
playerDialogueStart = 5500
# this is where we adjust the dialogue character delay
dialogueCharDelay = 50 


# leveling up options (balancing skills part)
levelUpOptions = {
    'Max HP Up': lambda p: (setattr(p, 'maxHp', p.maxHp + 1), setattr(p, 'hp', min(p.maxHp, p.hp + 1))), 
    'Speed Up': lambda p: setattr(p, 'movementSpeed', p.movementSpeed + 1), 
    'Damage Up': lambda p: setattr(p, 'bulletDamage', p.bulletDamage + 1.5), 
    'Fire Rate Up': lambda p: setattr(p, 'shotSpeed', max(50, p.shotSpeed - 30)), 
    'Extra Bullet': lambda p: setattr(p, 'bulletCount', p.bulletCount + 1), 
}
currentLevelUpChoices = []


def resetGame(endlessMode=False): #this is the function to reset the game state
    global enemies, bullets, expGems, particles, healthOrbs, magnetStars, spawnDelay, lastSpawnTime, startTime, score, player, finalWaveActive, finalBossActive, gameWon, lastHealthOrbSpawnTime, lastMagnetStarSpawnTime, currentEnemySpeed, victorySoundPlayed, magnetStartTime, victoryFadeAlpha, cutsceneStartTime, lastExpTriangleSpawnTime, lasers, isEndlessMode
    
    enemies = []
    bullets = []
    expGems = []
    particles = []
    healthOrbs = [] 
    magnetStars = []
    lasers = [] 
    
    spawnDelay = initialSpawnDelay
    currentEnemySpeed = enemyBaseSpeed
    
    lastSpawnTime = pygame.time.get_ticks()
    lastExpTriangleSpawnTime = pygame.time.get_ticks() 
    lastHealthOrbSpawnTime = pygame.time.get_ticks() 
    lastMagnetStarSpawnTime = pygame.time.get_ticks() 
    magnetStartTime = 0
    cutsceneStartTime = 0
    
    startTime = pygame.time.get_ticks()
    score = 0.0
    
    player = Player(screenWidth // 2, screenHeight - 120)
    finalWaveActive = False
    finalBossActive = False
    gameWon = False
    victorySoundPlayed = False
    victoryFadeAlpha = 0
    
    isEndlessMode = endlessMode # this is where we set the mode

    if musicLoaded:
        pygame.mixer.music.play(-1) 


introLines = [
    "SURVIVE",
    "DEFEAT THE POLYGONS",
    "PRESS ENTER"
]
introText = ""
introCharIndex = 0
introLineIndex = 0
introLastCharTime = 0
charDelay = 100 
linePause = 1000

lastSpawnTime = pygame.time.get_ticks()
introLastCharTime = pygame.time.get_ticks()
menuEnemySpawnTime = pygame.time.get_ticks() 
lastHealthOrbSpawnTime = pygame.time.get_ticks()
lastMagnetStarSpawnTime = pygame.time.get_ticks()
lastExpTriangleSpawnTime = pygame.time.get_ticks() 

# main loop
running = True
while running:
    dT = gameClock.tick(fps) / 16.0 
    now = pygame.time.get_ticks()

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state == stateIntro:
                if event.key == pygame.K_RETURN: 
                    state = stateMenu
            elif state == stateMenu:
                if event.key == pygame.K_SPACE:
                    resetGame(endlessMode=False) # this is for story mode
                    state = statePlaying
                if event.key == pygame.K_e: # this is for endless mode
                    resetGame(endlessMode=True)
                    state = statePlaying
            elif state == stateGameOver:
                if event.key == pygame.K_r: state = stateMenu
            elif state == stateCredits:
                if event.key == pygame.K_SPACE: 
                    if hasattr(sys.modules[__name__], 'scrollY'):
                        del sys.modules[__name__].scrollY
                    state = stateMenu
            elif state == stateLevelUp:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    try:
                        choiceIndex = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2}[event.key]
                        choiceKey = currentLevelUpChoices[choiceIndex]
                        levelUpOptions[choiceKey](player)
                        currentLevelUpChoices = [] 
                        state = statePlaying
                    except IndexError: pass
            
            elif state == statePlaying and event.key == pygame.K_x:
                state = statePaused
                if musicLoaded: pygame.mixer.music.pause()
            
            elif state == statePaused:
                if event.key == pygame.K_SPACE:
                    state = statePlaying
                    if musicLoaded: pygame.mixer.music.unpause()
                if event.key == pygame.K_m: # this is for the menu
                    state = stateMenu
                    if musicLoaded: pygame.mixer.music.unpause()


    # updating states(if there is input)
    if state == stateIntro:
        titleText = "SHAPE SURVIVOR"
        introText = "PRESS ENTER"
        
    elif state == stateMenu:
        if now - menuEnemySpawnTime > 1500 and len(menuEnemies) < 5:
            menuEnemySpawnTime = now
            menuEnemies.append(MenuEnemy())
        
        for e in menuEnemies: e.update(dT)
        menuEnemies = [e for e in menuEnemies if not e.isOffScreen()]


    elif state == stateLevelUp:
        if not currentLevelUpChoices:
            optionsKeys = list(levelUpOptions.keys())
            currentLevelUpChoices = random.sample(optionsKeys, min(3, len(optionsKeys)))

    elif state == stateCutscene:
        cutsceneElapsed = now - cutsceneStartTime
        
        boss = next((e for e in enemies if isinstance(e, DecagonBoss)), None)
        if boss:
            boss.update(dT) 

        if cutsceneElapsed > cutsceneDuration:
            state = statePlaying
            if musicLoaded:
                pygame.mixer.music.unpause()
        
        for p in particles: p.update()
        particles = [p for p in particles if p.life > 0]
        

    elif state == statePlaying:
        elapsed = (pygame.time.get_ticks() - startTime) / 1000.0 if startTime else 0.0
        score = elapsed
        
        # game end score is only relevant for story mode
        if not isEndlessMode and score >= gameEndScore:
            score = gameEndScore
            
        currentTimeSeconds = int(score)
        
        # difficulty and enemy waves
        currentTimeline = shapeTimelineEndless if isEndlessMode else shapeTimelineStory #this is where we select the appropriate timeline
        
        currentSides = 3 
        for timeReq, sides in sorted(currentTimeline.items()):
            if currentTimeSeconds >= timeReq:
                currentSides = sides
        
        currentEnemySpeed = enemyBaseSpeed + (currentTimeSeconds // 60) * enemySpeedMultiplier
        waveSides = currentSides 
        
        enemyHPScale = clamp(0.5 + (currentTimeSeconds / 240.0), 0.5, 1.0) 
        enemyHPWaveMultiplier = currentSides * enemyHPScale 
        
        # Story Mode Logic (Final Wave/Boss and Victory)
        if not isEndlessMode: # this is to ensure final wave and boss only happen in story mode
            
            if currentTimeSeconds >= finalWaveStartScore and not finalBossActive:
                finalWaveActive = True
                waveSides = 10 
                spawnDelay = 200 
                enemyHPWaveMultiplier = 8 

            if currentTimeSeconds >= finalBossStartScore and not finalBossActive:
                finalBossActive = True
                if not any(isinstance(e, DecagonBoss) for e in enemies):
                    enemies.append(DecagonBoss(player.x, player.y, currentEnemySpeed, enemyHPWaveMultiplier * 3))
                    state = stateCutscene
                    cutsceneStartTime = now
                    if musicLoaded:
                        pygame.mixer.music.pause()
                    spawnDelay = 5000 
                else:
                     spawnDelay = min(spawnDelay, 500) 

            if score >= gameEndScore and finalBossActive and not enemies and not gameWon:
                gameWon = True
                if score > highScore: highScore = score 
                
                state = stateCredits 
                if musicLoaded and not victorySoundPlayed:
                    pygame.mixer.music.stop()
                    soundVictory.play()
                    victorySoundPlayed = True
        
        # enemy spawning
        
        if not isEndlessMode and now - lastExpTriangleSpawnTime > expTriangleSpawnDelay and not finalBossActive and not any(isinstance(e, ExpTriangle) for e in enemies):
             lastExpTriangleSpawnTime = now
             enemies.append(ExpTriangle(player.x, player.y, currentEnemySpeed))
        
        if now - lastSpawnTime > spawnDelay:
            lastSpawnTime = now
            
            canSpawnRegular = True 
            
            if not isEndlessMode: # story mode spawning
                if not finalBossActive and canSpawnRegular:
                    if not finalWaveActive:
                        enemies.append(Enemy(player.x, player.y, currentSides, currentEnemySpeed, score, enemyHPWaveMultiplier)) 
                        spawnDelay = max(minSpawnDelay, int(spawnDelay * spawnAcceleration))
                    elif finalWaveActive and len(enemies) < 10:
                        enemies.append(Enemy(player.x, player.y, waveSides, currentEnemySpeed, score, enemyHPWaveMultiplier))
                
                elif finalBossActive and score < gameEndScore and not enemies and not any(isinstance(e, DecagonBoss) for e in enemies):
                     enemies.append(DecagonBoss(player.x, player.y, currentEnemySpeed, enemyHPWaveMultiplier * 3))
                     spawnDelay = 5000 
            
            elif isEndlessMode: # endless mode spawning
                enemies.append(Enemy(player.x, player.y, currentSides, currentEnemySpeed, score, enemyHPWaveMultiplier)) 
                spawnDelay = max(minSpawnDelay, int(spawnDelay * spawnAcceleration))


        if not isEndlessMode and finalBossActive: # only the final boss shoots a laser in story mode
            boss = next((e for e in enemies if isinstance(e, DecagonBoss)), None)
            if boss:
                boss.shootLaser(player)


        if now - lastHealthOrbSpawnTime > healthOrbSpawnDelay and not healthOrbs and random.random() < 0.3: 
            healthOrbs.append(HealthOrb())
            lastHealthOrbSpawnTime = now
            
        if now - lastMagnetStarSpawnTime > magnetStarSpawnDelay and not magnetStars and random.random() < 0.3: 
            magnetStars.append(MagnetStar())
            lastMagnetStarSpawnTime = now
        
        if player.magnetRadius > 0 and now - magnetStartTime > magnetStarDuration:
            player.magnetRadius = 0 

        keys = pygame.key.get_pressed()
        if player.alive:
            player.update(keys)
            playerShoot(player, bullets)

        for e in enemies: e.update(dT)
        for b in bullets: b.update(dT)
        for l in lasers: l.update() 
        for g in expGems: g.update(player.x, player.y, player.magnetRadius) 
        for p in particles: p.update()
        
        lasers = [l for l in lasers if l.state != 'dead'] 
        
        for orb in healthOrbs: 
            if player.magnetRadius > 0:
                orb.update(player.x, player.y, player.magnetRadius)
            
        healthOrbsToKeep = []
        for orb in healthOrbs:
            if circleCollision(orb.x, orb.y, orb.size, player.x, player.y, player.size):
                if player.hp < player.maxHp:
                    player.hp += 1 
                for i in range(20): particles.append(Particle(orb.x, orb.y, particleColor=white)) 
            else: healthOrbsToKeep.append(orb)
        healthOrbs = healthOrbsToKeep
        
        magnetStarsToKeep = []
        for star in magnetStars:
            if circleCollision(star.x, star.y, star.size, player.x, player.y, player.size):
                # this is where we adjust the magnet radius
                player.magnetRadius = 200 
                magnetStartTime = now 
                for i in range(30): particles.append(Particle(star.x, star.y, particleColor=white))
                star.alive = False 
            
            if star.alive: 
                magnetStarsToKeep.append(star)
        magnetStars = magnetStarsToKeep
        
        # laser collision with player
        activeLasers = [l for l in lasers if l.state == 'active']
        for l in activeLasers:
            if player.alive and l.isColliding(player):
                player.takeDamage()
                for i in range(30): particles.append(Particle(player.x, player.y, particleColor=red))
                break 

        bulletsToKeep = []
        for b in bullets:
            hit = False
            for e in enemies:
                if isinstance(e, ExpTriangle) or isinstance(e, DecagonBoss):
                     if circleCollision(b.x, b.y, b.size, e.x, e.y, e.size):
                        e.hp -= b.damage
                        hit = True
                        pColor = yellow if isinstance(e, ExpTriangle) else (red if isinstance(e, DecagonBoss) else white)
                        for i in range(5): particles.append(Particle(b.x, b.y, particleColor=pColor))
                        break
                else:
                    enemyPoints = [(int(e.x + math.cos(math.radians(e.angle + i * 360 / e.sides)) * e.size), 
                                     int(e.y + math.sin(math.radians(e.angle + i * 360 / e.sides)) * e.size))
                                     for i in range(e.sides)]
                    
                    if pointInPolygon(b.x, b.y, enemyPoints):
                        e.hp -= b.damage
                        hit = True
                        for i in range(5): particles.append(Particle(b.x, b.y, particleColor=white))
                        break
            
            if not hit and b.isOnScreen(): bulletsToKeep.append(b)
        bullets = bulletsToKeep
        
        enemiesToKeep = []
        for e in enemies:
            isDead = False
            if e.hp <= 0:
                isDead = True
                expAmount = e.maxHp * 5 
                
                pColor = white 
                
                if isinstance(e, DecagonBoss):
                    expAmount = e.maxHp * 15 
                    pColor = red
                elif isinstance(e, ExpTriangle):
                    expAmount = e.expValue 
                    pColor = yellow

                expGems.append(ExpGem(e.x, e.y, expAmount))
                
                for i in range(20): 
                    particles.append(Particle(e.x, e.y, particleColor=pColor)) 
            
            if player.alive and not isDead and circleCollision(e.x, e.y, e.size*0.6, player.x, player.y, player.size):
                player.takeDamage()
                isDead = True
                for i in range(30): particles.append(Particle(player.x, player.y, particleColor=white))
            
            if not isDead: 
                if e.isOnScreen() or isinstance(e, DecagonBoss):
                    enemiesToKeep.append(e)
        enemies = enemiesToKeep

        expGemsToKeep = []
        for g in expGems:
            if circleCollision(g.x, g.y, g.size, player.x, player.y, player.size):
                player.gainExp(g.amount)
            else: expGemsToKeep.append(g)
        expGems = expGemsToKeep

        particles = [p for p in particles if p.life > 0]

        if not player.alive:
            # this is where we check if we need to update endless high scores
            if isEndlessMode:
                updateEndlessHighScores(score)
                
            state = stateGameOver
            if musicLoaded: pygame.mixer.music.stop()
            if not isEndlessMode and score > highScore: highScore = score

    elif state == stateVictoryScreen:
        if victoryFadeAlpha < 255:
            victoryFadeAlpha = min(255, victoryFadeAlpha + 2 * dT)
        else:
            state = stateCredits
            
        for p in particles: p.update()
        particles = [p for p in particles if p.life > 0]

    elif state == stateGameOver or state == stateCredits:
        for p in particles: p.update()
        particles = [p for p in particles if p.life > 0]


    # draws screen
    screen.fill(black)

    if state == stateIntro:
        title = fontBig.render('SHAPE SURVIVOR', True, white)
        screen.blit(title, (screenWidth//2 - title.get_width()//2, screenHeight//2 - 100))
        
        textSurf = fontMed.render(introText, True, white)
        
        lines = [
            fontMed.render("DEFEAT THE POLYGONS", True, white),
        ]
        
        screen.blit(lines[0], lines[0].get_rect(center=(screenWidth//2, screenHeight//2 - 20)))
        
        rect = textSurf.get_rect(center=(screenWidth//2, screenHeight//2 + 60))
        screen.blit(textSurf, rect)
        
    elif state == stateMenu:
        for e in menuEnemies: e.draw(screen)

        title = fontBig.render('SHAPE SURVIVOR', True, white)
        screen.blit(title, (screenWidth//2 - title.get_width()//2, 80))
        
        # Story Mode
        storyModeTxt = fontMed.render("START GAME [SPACE] (STORY MODE)", True, white)
        screen.blit(storyModeTxt, storyModeTxt.get_rect(center=(screenWidth//2, 180)))
        
        # Endless Mode
        endlessModeTxt = fontMed.render("ENDLESS MODE [E]", True, white)
        screen.blit(endlessModeTxt, endlessModeTxt.get_rect(center=(screenWidth//2, 220)))

        # Story High Score
        hsLabelTxt = fontMed.render("STORY HIGH SCORE:", True, white)
        hsValueTxt = fontBig.render(f"{highScore:.2f} S", True, white)
        screen.blit(hsLabelTxt, hsLabelTxt.get_rect(center=(screenWidth//2, 280)))
        screen.blit(hsValueTxt, hsValueTxt.get_rect(center=(screenWidth//2, 320)))

        # Endless High Scores
        endlessLabelTxt = fontMed.render("LONGEST ENDLESS RUNS:", True, white)
        screen.blit(endlessLabelTxt, endlessLabelTxt.get_rect(center=(screenWidth//2, 380)))
        
        yPos = 420
        # this is where we display the top 3 endless mode scores
        for i, scoreValue in enumerate(endlessHighScores):
             # Fixed suffixes and added space for better readability
             suffix = "ST" if i == 0 else ("ND" if i == 1 else "RD")
             scoreLine = f"{i+1}{suffix}: {scoreValue:.2f} S"
             scoreTxt = fontMed.render(scoreLine, True, white)
             screen.blit(scoreTxt, scoreTxt.get_rect(center=(screenWidth//2, yPos)))
             yPos += 30

        # Controls
        controlsTxt = fontMed.render("CONTROLS: WASD/ARROWS", True, white)
        screen.blit(controlsTxt, controlsTxt.get_rect(center=(screenWidth//2, screenHeight - 60)))

    elif state == statePlaying or state == stateLevelUp or state == statePaused or state == stateCutscene:
        for m in enemies: m.draw(screen)
        for b in bullets: b.draw(screen)
        for g in expGems: g.draw(screen)
        
        for orb in healthOrbs: orb.draw(screen) 
        for star in magnetStars: star.draw(screen) 
        
        for l in lasers: l.draw(screen)
            
        for part in particles: part.draw(screen)

        if player.alive: player.draw(screen)

        # ui overlay (hp bars, and stuff)
        
        s = fontMed.render(f'{score:.2f}', True, white)
        screen.blit(s, (10, 10))
        
        hpSize = 10
        hpSpacing = 5
        startX = 10
        startY = 50
        
        for i in range(player.maxHp):
            outlineColor = white
            fillColor = white if i < player.hp else black
            
            circleCenter = (startX + hpSize, startY + hpSize)

            pygame.draw.circle(screen, fillColor, circleCenter, hpSize)
            pygame.draw.circle(screen, outlineColor, circleCenter, hpSize, 1)
            
            startX += hpSize * 2 + hpSpacing

        lvlText = fontSmall.render(f'LV: {player.level}', True, white)
        screen.blit(lvlText, (screenWidth - lvlText.get_width() - 10, 10))
        
        expRatio = player.exp / player.expToNextLevel
        barWidth = 100
        barHeight = 4
        barX = screenWidth - barWidth - 10
        barY = 35
        
        pygame.draw.rect(screen, white, (barX, barY, barWidth, barHeight), 1)
        pygame.draw.rect(screen, white, (barX + 1, barY + 1, (barWidth - 2) * expRatio, barHeight - 2))

        waveName = {
            3: "Triangle", 4: "Square", 5: "Pentagon", 
            6: "Hexagon", 7: "Heptagon", 8: "Octagon", 9: "Nonagon", 10: "Decagon"
        }.get(currentSides, "??")
        
        indicatorText = f'CURRENT WAVE ({waveName.upper()})' 
        
        if not isEndlessMode: # story mode specific indicators
            if finalWaveActive and not finalBossActive:
                indicatorText = 'FINAL WAVE (DECAGONS)'
            elif finalBossActive:
                 indicatorText = 'FINAL BOSS (HUGE DECAGON) | SURVIVE 50S'
        else: # endless mode indicator
            if currentSides < 9: # waves before max level
                timeLeft = 600 - (currentTimeSeconds % 600)
                indicatorText = f'ENDLESS WAVE ({waveName.upper()}) | NEXT WAVE IN: {timeLeft} S' #this is the endless mode wave timer
            else: # max level reached (nonagon / 9 sides is max difficulty in timeline)
                indicatorText = f'ENDLESS WAVE (NONAGONS+) | MAX DIFFICULTY'

        waveText = fontMed.render(indicatorText, True, white)
        waveTextX = screenWidth//2 - waveText.get_width()//2
        screen.blit(waveText, (waveTextX, 10))
        
        pauseText = fontSmall.render('[X] PAUSE', True, white)
        screen.blit(pauseText, (screenWidth//2 - pauseText.get_width()//2, 40))
            
        if player.magnetRadius > 0:
            magnetTimeLeft = max(0, magnetStarDuration - (now - magnetStartTime)) / 1000
            magText = fontSmall.render(f'MAG: {magnetTimeLeft:.1f} S', True, white)
            screen.blit(magText, (screenWidth - magText.get_width() - 10, 50))


        if state == stateLevelUp:
            boxW, boxH = 400, 250
            boxX, boxY = screenWidth//2 - boxW//2, screenHeight//2 - boxH//2
            
            pygame.draw.rect(screen, black, (boxX, boxY, boxW, boxH))
            pygame.draw.rect(screen, white, (boxX, boxY, boxW, boxH), lineThickness)
            
            lvltxt = fontBig.render('LEVEL UP', True, white)
            screen.blit(lvltxt, (screenWidth//2 - lvltxt.get_width()//2, boxY + 15))
            
            for i, choice in enumerate(currentLevelUpChoices):
                choiceText = f"[{i+1}] {choice}"
                optTxt = fontMed.render(choiceText, True, white)
                screen.blit(optTxt, (boxX + 40, boxY + 80 + i * 50))
                
        elif state == statePaused:
            overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            screen.blit(overlay, (0, 0))
            
            pauseTxt = fontBig.render('PAUSED', True, white)
            resumeTxt = fontMed.render('PRESS SPACE TO RESUME', True, white)
            menuTxt = fontMed.render('PRESS [M] FOR MENU', True, white) # Added Menu text
            
            screen.blit(pauseTxt, (screenWidth//2 - pauseTxt.get_width()//2, screenHeight//2 - 60))
            screen.blit(resumeTxt, (screenWidth//2 - resumeTxt.get_width()//2, screenHeight//2))
            screen.blit(menuTxt, (screenWidth//2 - menuTxt.get_width()//2, screenHeight//2 + 40)) # Placed Menu text
            
        elif state == stateCutscene:
            overlay = pygame.Surface((screenWidth, screenHeight), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200)) 
            screen.blit(overlay, (0, 0))
            
            boss = next((e for e in enemies if isinstance(e, DecagonBoss)), None)
            cutsceneElapsed = now - cutsceneStartTime
            
            # boss dialogue
            if cutsceneElapsed > bossDialogueStart:
                
                typingTime = cutsceneElapsed - bossDialogueStart
                charCount = min(len(bossDialogue), int(typingTime / dialogueCharDelay))
                currentDialogue = bossDialogue[:charCount]
                
                dialogueTxt = fontMed.render(currentDialogue, True, white)
                
                dialogueX = screenWidth//2 + 20 
                dialogueY = screenHeight//2 - 100
                
                boxW = dialogueTxt.get_width() + 40
                boxH = dialogueTxt.get_height() + 20
                
                if charCount > 0:
                    pygame.draw.rect(screen, black, (dialogueX - 20, dialogueY - 10, boxW, boxH))
                    pygame.draw.rect(screen, white, (dialogueX - 20, dialogueY - 10, boxW, boxH), 2)
                    screen.blit(dialogueTxt, (dialogueX, dialogueY))
            
            # player dialogue
            if cutsceneElapsed > playerDialogueStart:
                
                playerTxt = fontMed.render(playerDialogue, True, white)
                
                playerDialogueX = player.x - playerTxt.get_width() // 2
                playerDialogueY = player.y - 60
                
                boxW = playerTxt.get_width() + 40
                boxH = playerTxt.get_height() + 20
                
                pygame.draw.rect(screen, black, (playerDialogueX - 20, playerDialogueY - 10, boxW, boxH))
                pygame.draw.rect(screen, white, (playerDialogueX - 20, playerDialogueY - 10, boxW, boxH), 2)
                
                screen.blit(playerTxt, (playerDialogueX, playerDialogueY))
                
                if musicLoaded and cutsceneElapsed - playerDialogueStart < 50:
                    soundFahh.play()

            cutTxt = fontSmall.render('--- cutscene ---', True, white)
            screen.blit(cutTxt, (screenWidth//2 - cutTxt.get_width()//2, screenHeight - 30))


    elif state == stateVictoryScreen:
        if victoryFadeAlpha < 255:
            victoryFadeAlpha = min(255, victoryFadeAlpha + 2 * dT)
        else:
            state = stateCredits
            
        for p in particles: p.update()
        particles = [p for p in particles if p.life > 0]

    elif state == stateGameOver:
        for m in enemies: m.draw(screen)
        for part in particles: part.draw(screen)

        go = fontBig.render('GAME OVER', True, white)
        
        # this is where we show the score depending on the mode
        modeName = "STORY" if not isEndlessMode else "ENDLESS"
        sub = fontMed.render(f'TIME: {score:.2f} S ({modeName} MODE)', True, white)
        
        sub2 = fontMed.render('PRESS R TO MENU', True, white)
        screen.blit(go, (screenWidth//2 - go.get_width()//2, screenHeight//2 - 60))
        screen.blit(sub, (screenWidth//2 - sub.get_width()//2, screenHeight//2 + 10))
        screen.blit(sub2, (screenWidth//2 - sub2.get_width()//2, screenHeight//2 + 48))

    elif state == stateCredits:
        if gameWon and not victorySoundPlayed:
            if musicLoaded: soundVictory.play()
            victorySoundPlayed = True
            
        winText = fontBig.render('YOU WON!', True, white)
        screen.blit(winText, (screenWidth//2 - winText.get_width()//2, 50))
        
        creditLines = [
            "You've successfully beat Shape Survivor!",
            "Congratulations player!",
            "",
            "This a Computer Graphics Programming Project",
            "Submitted to Sir Brian Steven Pajarillo",
            "",
            "Submitted by:",
            "Joel Hans Apostol",
            "John Daniel Descutido",
            "Junnel Talaver",
            "Ryan Valencia",
            "",
            "BSIT 4C",
            "",
            "Game Concept Inspired by: Asteroids and Vampire Survivors",
            "",
            "Sfx: Invader Disco by ZUNTATA and more",
            "",
            "--- The end ---",
            "",
            "",
            "PRESS SPACE TO RETURN TO MENU"
        ]
        
        if not hasattr(sys.modules[__name__], 'scrollY'):
            sys.modules[__name__].scrollY = screenHeight + 50
        
        scrollSpeed = 0.5 * dT 
        sys.modules[__name__].scrollY -= scrollSpeed
        
        scrollY = sys.modules[__name__].scrollY 
        
        yPos = scrollY
        
        for line in creditLines:
            fnt = fontMed 
            
            if line == "":
                yPos += fnt.get_height() + 5
                continue
                
            txt = fnt.render(line, True, white)
            screen.blit(txt, (screenWidth//2 - txt.get_width()//2, int(yPos)))
            yPos += fnt.get_height() + 10 

        if yPos < 0:
            sys.modules[__name__].scrollY = screenHeight + 50 


    pygame.display.flip()

pygame.quit()
sys.exit()

#shoutout to stackoverflow and reddit threads, heroes for this project!/ᐠ ˵> ⩊ <˵マ
