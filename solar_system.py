import pygame
import math
 
# Initialize pygame 
pygame.init()

clock = pygame.time.Clock()

WIDTH = 2000
HEIGHT = 1000
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (176,224,230)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
GREEN = (119, 116, 81)
ORANGE = (255, 165, 0)
TAN = (210, 180, 140)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Width, height in tuple
 
pygame.display.set_caption("The Solar System")

class Planet:
    AU = 1.496e11           # 1 AU in meters
    G = 6.674e-11           # Gravitational constant
    SCALE = 250 / (1.496e11)  # Pixels per meter (200 pixels = 1 AU)
    TIMESTEP = 86400        # 1 day in seconds
    
    def __init__(self, x, y, radius, color, mass, name, y_vel=0):

        self.color = color
        self.radius = radius
        self.name = name
        self.x = x 
        self.y = y 
        self.mass = mass
        self.sun = False  
        
        self.x_vel = 0
        self.y_vel = y_vel
        
        self.distance_to_sun = 0
        self.orbit = []
        
    
    def info(self):
        pass
     
    def attraction(self, other):
        
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        
        
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        
        if other.sun:
            self.distance_to_sun = distance
        
        
        force = self.G * self.mass * other.mass / distance ** 2
        
        
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    def update_position(self, planets, substeps=1):
        sub_dt = self.TIMESTEP / substeps
        for _ in range(substeps):
            total_fx = 0
            total_fy = 0
        
            for planet in planets:
                if self == planet:
                    continue  
                
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy
        
        # Physics formula: a = F / m
        # So: velocity_change = (F / m) * time
        # In code:
            self.x_vel += total_fx / self.mass * sub_dt
            self.y_vel += total_fy / self.mass * sub_dt  # Complete this line
            
            # Physics formula: position_change = velocity * time
            self.x += self.x_vel * sub_dt
            self.y += self.y_vel * sub_dt


    def draw(self, surface, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y, self.SCALE)
        
        if self.sun:
            display_radius = max(3, int(self.radius * min(camera.zoom, 5)))
        else:
            display_radius = max(2, int(self.radius * min(camera.zoom, 3)))
        
        pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), display_radius)
            
    def draw_orbit(self, surface, center_x, center_y):
        pass
    

class Camera:
    def __init__(self):
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.follow_target = None
    
    def world_to_screen(self, x, y, base_scale):
        screen_x = x * base_scale * self.zoom + WIDTH/2 + self.offset_x
        screen_y = y * base_scale * self.zoom + HEIGHT/2 + self.offset_y
        return int(screen_x), int(screen_y)
    
    def update(self):
        """Call once per frame to follow target."""
        if self.follow_target:
            self.offset_x = -self.follow_target.x * Planet.SCALE * self.zoom
            self.offset_y = -self.follow_target.y * Planet.SCALE * self.zoom
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.zoom *= 1.2
            else:
                self.zoom /= 1.2
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0 or event.key == pygame.K_HOME:
                self.follow_target = None
                self.offset_x = 0
                self.offset_y = 0
                self.zoom = 1.0
 
def create_moon(parent, distance_km, orbital_vel_km_s, mass, radius, color, name):
    distance_m = distance_km * 1000
    moon = Planet(
        parent.x + distance_m,
        parent.y,
        radius,
        color,
        mass,
        name,
        parent.y_vel + (orbital_vel_km_s * 1000)
    )
    moon.is_moon = True
    moon.parent = parent
    return moon
    
sun_body = Planet(0, 0, 30, YELLOW, 1.989e30, "Sun")
sun_body.sun = True

mercury = Planet(0.387 * Planet.AU, 0, 8, BROWN, 3.301e23, "Mercury", 35020)
venus = Planet(0.723 * Planet.AU, 0, 14, GREEN, 4.867e24, "Venus", 35020)
earth = Planet(1.0 * Planet.AU, 0, 16, BLUE, 5.972e24, "Earth", 29780)
mars = Planet(1.524 * Planet.AU, 0, 12, RED, 6.417e23, "Mars", 24070)
jupiter = Planet(5.203 * Planet.AU, 0, 28, ORANGE, 1.899e27, "Jupiter", 13070)
saturn = Planet(9.537 * Planet.AU, 0, 24, TAN, 5.685e26, "Saturn", 9680)
uranus = Planet(19.19 * Planet.AU, 0, 18, LIGHT_BLUE, 8.681e25, "Uranus", 6800)
neptune = Planet(30.07 * Planet.AU, 0, 18, DARK_BLUE, 1.024e26, "Neptune", 5430)

# Dwarf Planetss
ceres = Planet(2.77 * Planet.AU, 0, 6, (169, 169, 169), 9.39e20, "Ceres", 17900)
pluto = Planet(29.66 * Planet.AU, 0, 8, (210, 180, 140), 1.303e22, "Pluto", 6100)
haumea = Planet(34.72 * Planet.AU, 0, 6, (180, 160, 150), 4.006e21, "Haumea", 5520)
makemake = Planet(38.59 * Planet.AU, 0, 6, (160, 120, 100), 3.1e21, "Makemake", 5240)
eris = Planet(37.91 * Planet.AU, 0, 8, (200, 200, 210), 1.66e22, "Eris", 5580)

# MOONS
# Earth's Moon
moon = create_moon(earth, 384400, 1.022, 7.342e22, 4, (169, 169, 169), "Moon")

# Mars's Moons
phobos = create_moon(mars, 9376, 2.138, 1.066e16, 2, (139, 119, 101), "Phobos")
deimos = create_moon(mars, 23463, 1.351, 1.476e15, 2, (180, 166, 152), "Deimos")

# Jupiter's Galilean Moons
io = create_moon(jupiter, 421700, 17.334, 8.932e22, 4, (255, 200, 50), "Io")
europa = create_moon(jupiter, 671034, 13.740, 4.800e22, 4, (220, 210, 200), "Europa")
ganymede = create_moon(jupiter, 1070412, 10.880, 1.482e23, 5, (160, 145, 130), "Ganymede")
callisto = create_moon(jupiter, 1882709, 8.204, 1.076e23, 5, (100, 100, 110), "Callisto")

# Saturn's Major Moons
enceladus = create_moon(saturn, 237948, 12.64, 1.080e20, 2, (240, 245, 255), "Enceladus")
tethys = create_moon(saturn, 294619, 11.35, 6.175e20, 3, (200, 200, 210), "Tethys")
dione = create_moon(saturn, 377396, 10.03, 1.095e21, 3, (200, 200, 210), "Dione")
rhea = create_moon(saturn, 527108, 8.48, 2.307e21, 4, (200, 200, 210), "Rhea")
titan = create_moon(saturn, 1221870, 5.57, 1.345e23, 5, (230, 190, 100), "Titan")
iapetus = create_moon(saturn, 3560820, 3.26, 1.806e21, 3, (200, 200, 210), "Iapetus")

# Uranus's Major Moons
miranda = create_moon(uranus, 129390, 6.66, 6.59e19, 2, (180, 180, 190), "Miranda")
ariel = create_moon(uranus, 190020, 5.51, 1.251e21, 3, (180, 180, 190), "Ariel")
umbriel = create_moon(uranus, 266300, 4.67, 1.172e21, 3, (180, 180, 190), "Umbriel")
titania = create_moon(uranus, 435910, 3.64, 3.527e21, 4, (180, 180, 190), "Titania")
oberon = create_moon(uranus, 583520, 3.15, 3.014e21, 4, (160, 155, 150), "Oberon")

# Neptune's Moons
proteus = create_moon(neptune, 117647, 7.62, 4.4e19, 2, (180, 180, 190), "Proteus")
triton = create_moon(neptune, 354759, -4.39, 2.14e22, 4, (180, 200, 210), "Triton")

# Pluto's Moons
charon = create_moon(pluto, 19591, 0.21, 1.586e21, 4, (150, 150, 160), "Charon")
nix = create_moon(pluto, 48694, 0.13, 4.5e17, 2, (200, 200, 200), "Nix")
hydra = create_moon(pluto, 64738, 0.11, 4.8e17, 2, (200, 200, 200), "Hydra")

# Eris's Moon
dysnomia = create_moon(eris, 37273, 0.13, 8.2e19, 2, (170, 170, 180), "Dysnomia")

# Haumea's Moons
hiiaka = create_moon(haumea, 49880, 0.11, 1.79e19, 2, (190, 180, 170), "Hi'iaka")
namaka = create_moon(haumea, 25657, 0.11, 1.79e18, 2, (190, 180, 170), "Namaka")



planets = [
    sun_body,
    mercury, venus, earth, mars, jupiter, saturn, uranus, neptune,
    ceres, pluto, haumea, makemake, eris,
    moon,
    phobos, deimos,
    io, europa, ganymede, callisto,
    enceladus, tethys, dione, rhea, titan, iapetus,
    miranda, ariel, umbriel, titania, oberon,
    proteus, triton,
    charon, nix, hydra,
    dysnomia,
    hiiaka, namaka,
]
 
running = True

camera = Camera()


time_scale = 1.0

planet_lookup = {p.name.lower(): p for p in planets}

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        camera.handle_input(event)
        
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: 'mercury', pygame.K_2: 'venus',
                pygame.K_3: 'earth',   pygame.K_4: 'mars',
                pygame.K_5: 'jupiter', pygame.K_6: 'saturn',
                pygame.K_7: 'uranus',  pygame.K_8: 'neptune',
            }
            if event.key in key_map:
                camera.follow_target = planet_lookup[key_map[event.key]]
            if event.key == pygame.K_EQUALS:  # + key
                time_scale *= 2
                print(f"Speed: {time_scale}x")
            elif event.key == pygame.K_MINUS:  # - key
                time_scale /= 2
                print(f"Speed: {time_scale}x")
            elif event.key == pygame.K_SPACE:
                time_scale = 0 if time_scale > 0 else 1.0
                print("PAUSED" if time_scale == 0 else "RUNNING")
                
    screen.fill(BLACK)
    
    sub_dt = Planet.TIMESTEP * time_scale / 96
    
    for _ in range(96):
        # Calculate planet forces (ignore moons)
        planet_forces = {}
        for planet in planets:
            if planet.sun or hasattr(planet, 'is_moon'):
                continue
            fx, fy = 0, 0
            for other in planets:
                if other == planet or hasattr(other, 'is_moon'):
                    continue
                f_x, f_y = planet.attraction(other)
                fx += f_x
                fy += f_y
            planet_forces[planet.name] = (fx, fy)

        # Calculate moon forces (only parent + Sun)
        moon_forces = {}
        for planet in planets:
            if not hasattr(planet, 'is_moon'):
                continue
            fx, fy = 0, 0
            for other in [sun_body, planet.parent]:
                f_x, f_y = planet.attraction(other)
                fx += f_x
                fy += f_y
            moon_forces[planet.name] = (fx, fy)

        # Update ALL positions together
        for planet in planets:
            if planet.sun:
                continue
            if hasattr(planet, 'is_moon'):
                fx, fy = moon_forces[planet.name]
            else:
                fx, fy = planet_forces[planet.name]
            planet.x_vel += fx / planet.mass * sub_dt
            planet.y_vel += fy / planet.mass * sub_dt
            planet.x += planet.x_vel * sub_dt
            planet.y += planet.y_vel * sub_dt
            
    camera.update()
    # Draw once per frame
    for planet in planets:
        planet.draw(screen, camera)
    font = pygame.font.SysFont("Arial", 16)

# After drawing planets, before pygame.display.update():
    target_name = camera.follow_target.name if camera.follow_target else "Sun"
    hud_lines = [
        f"Following: {target_name}",
        f"Speed: {time_scale}x",
        f"Zoom: {camera.zoom:.1f}",
        "0: Sun  1-8: Planets  +/-: Speed  Space: Pause",
    ]
    for i, line in enumerate(hud_lines):
        text = font.render(line, True, (200, 200, 200))
        screen.blit(text, (10, 10 + i * 22))
    pygame.display.update()
    clock.tick(60)

pygame.quit()