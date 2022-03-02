import pygame
import math
pygame.init()

#Windows setup (dimensions)
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation des planètes")
#Define the colors
Midnightblue = (25, 25, 112)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
Orangered = (255, 69, 0)
Darkgrey = (169, 169, 169)
White = (255, 255, 255)
Silver = (192, 192, 192)
FONT = pygame.font.SysFont("comicsans", 16)

#Implementing the planets
class Planet:
    #Distance from the earth to the sun
    ES = 149.6e6 * 1000
    #Gravity
    G = 6.67428e-11
    # 1ES = 100 pixels
    Scale = 250 / ES
    # 1 day
    Time_step = 3600 * 24

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        #velocity (moving in circle)
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.Scale + WIDTH / 2
        y = self.y * self.Scale + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.Scale + WIDTH / 2
                y = y * self.Scale + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        #Text on planets
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 10)}km", 1, Silver)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

        pygame.draw.circle(win, self.color, (x,y), self.radius)

    #Implementing mouvement
    def attraction(self, other):
        #The distance between two objects
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y **2)

        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance **2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.Time_step
        self.y_vel += total_fy / self.mass * self.Time_step

        self.x += self.x_vel * self.Time_step
        self.y += self.y_vel * self.Time_step
        self.orbit.append((self.x, self.y))

def window():
    run = True
    clock = pygame.time.Clock()
    #Drawing the sun
    sun = Planet(0, 0, 30, Yellow, 1.98892 * 10**30)
    sun.sun = True
    #Drawing earth
    earth = Planet(-1* Planet.ES, 0, 16, Blue, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    #Drawing mars
    mars = Planet(-1.524* Planet.ES, 0, 12, Orangered, 6.39 * 10**23)
    mars.y_vel = 24.007 * 1000
    #Drawing mercury
    mercury = Planet(0.387* Planet.ES, 0, 8, Darkgrey, 0.330 * 10**23)
    mercury.y_vel = -47.4 * 1000
    #Drawing venus
    venus = Planet(0.723* Planet.ES, 0, 14, White, 4.8685 * 10**24 )
    venus.y_vel = -35.02 * 1000
    planets = [sun, earth, mars, mercury, venus]
    while run:
        clock.tick(60)
        WIN.fill(Midnightblue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        pygame.display.update()

    pygame.quit()

window()