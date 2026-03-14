import pygame
import math
import re

pygame.init()

clock = pygame.time.Clock()

WIDTH = 2000
HEIGHT = 1000
PANEL_SPLIT = 1200

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

    def __init__(self, name, color, mass, x, y, radius, y_vel=0 ):
        self.name = name
        self.color = color
        self.mass = mass
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = 0
        self.y_vel = y_vel
        self.sun = False
        self.hovered =False
        self.selected = False
    
    def draw(self, surface, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        
        if self.sun:
            dot_radius = 8
        else:
            dot_radius = 6
        
        if self.hovered:
            draw_color = (min(self.color[0]+60, 255),
                          min(self.color[1]+60, 255),
                          min(self.color[2]+60, 255))
        else: 
            draw_color = self.color
            
        if self.selected:
            pygame.draw.circle(surface, (255, 255, 255), (int(screen_x), int(screen_y)), dot_radius + 4, 1)
            
        pygame.draw.circle(surface, draw_color, (int(screen_x), int(screen_y)), dot_radius)
        
        label = font_name.render(self.name, True, (200,200,200))
        surface.blit(label, (screen_x + dot_radius + 4, screen_y -6))
        
    def attraction(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        force = self.G * self.mass * other.mass / distance**2
        angle = math.atan2(dy, dx)
        return (math.cos(angle) * force, math.sin(angle) * force)
    
    def hit_test(self, mouse_x, mouse_y, camera):
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        dist = math.sqrt((mouse_x - screen_x)**2 + (mouse_y - screen_y)**2)
        if dist < 10:
            return True
        else:
            return False
        
     
class Camera:
    def __init__(self):
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.base_scale = (PANEL_SPLIT / 2) / (32 * Planet.AU)
    
    def world_to_screen(self, x_meters, y_meters):
        px = x_meters * self.base_scale * self.zoom + PANEL_SPLIT/2 + self.offset_x
        py = y_meters * self.base_scale * self.zoom + HEIGHT/2 + self.offset_y
        return (int(px), int(py))
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.zoom *= 1.15
            else:
                self.zoom /= 1.15
                
# Helper Functions

def select_planet(planet):
        global selected_planet
        if selected_planet:
            selected_planet.selected = False
        selected_planet = planet
        planet.selected = True
        
def format_period(days):
    if days == 0:
        return 'N/A'
    if days < 1:
        return f'{days * 24:.1f} hours ({days:.2f} days)'
    if days < 365:
        return f'{days:.1f} days ({days * 24:,.0f} hours)'
    return f'{days/365.25:.2f} years ({days:,.0f} days)'

def format_mass(kg):
    earths = kg / 5.972e24
    if earths > 10:
        return f'{earths:,.1f} Earths ({kg:.3e} kg)'
    if earths > 0.01:
        return f'{earths:.3f} Earths ({kg:.3e} kg)'
    return f'{kg:.3e} kg ({earths:.6f} Earths)' 

def format_gravity(g):
    earth_g = g / 9.81
    return f'{g} m/s² ({earth_g:.2f}x Earth)'

def format_radius(km):
    miles = km * 0.621371
    return f'{km:,} km ({miles:,.0f} miles)'

def format_temp(temp_str):
    numbers = re.findall(r'-?\d+', temp_str)
    if len(numbers) == 2:
        f1 = int(numbers[0]) * 9/5 + 32
        f2 = int(numbers[1]) * 9/5 + 32
        return f'{temp_str} ({f1:.0f} to {f2:.0f}°F)'
    elif len(numbers) == 1:
        f1 = int(numbers[0]) * 9/5 + 32
        return f'{temp_str} ({f1:.0f}°F)'
    return temp_str

def format_au(au):
    if au == 0:
        return 'N/A (center)'
    miles = au * 92955807.3
    return f'{au:.3f} AU ({miles:,.0f} miles)'       
        
PLANET_DATA = {
    'Sun': {
        'dist_au': 0,
        'mass_kg': 1.989e30,
        'radius_km': 696340,
        'period_days': 0,
        'eccentricity': 0,
        'velocity_km_s': 0,
        'surface_gravity_m_s2': 274.0,
        'temperature': '5,500°C (surface)',
        'type': 'G-type Main Sequence Star',
        'description': 'The star at the center of the Solar System. Contains 99.86% of the total mass. Powered by nuclear fusion converting hydrogen to helium.',
        'moons': [],
    },
    'Mercury': {
        'dist_au': 0.387,
        'mass_kg': 3.301e23,
        'radius_km': 2440,
        'period_days': 87.97,
        'eccentricity': 0.2056,
        'velocity_km_s': 47.36,
        'surface_gravity_m_s2': 3.7,
        'temperature': '-180 to 430°C',
        'type': 'Terrestrial Planet',
        'description': 'Smallest planet. Extreme temperature swings due to lack of atmosphere. Heavily cratered surface resembling Earth\'s Moon. Tidally locked in a 3:2 spin-orbit resonance.',
        'moons': [],
    },
    'Venus': {
        'dist_au': 0.723,
        'mass_kg': 4.867e24,
        'radius_km': 6052,
        'period_days': 224.7,
        'eccentricity': 0.0068,
        'velocity_km_s': 35.02,
        'surface_gravity_m_s2': 8.87,
        'temperature': '465°C (surface)',
        'type': 'Terrestrial Planet',
        'description': 'Hottest planet due to runaway greenhouse effect. Dense CO2 atmosphere with sulfuric acid clouds. Rotates backwards (retrograde) and slower than its orbit.',
        'moons': [],
    },
    'Earth': {
        'dist_au': 1.0,
        'mass_kg': 5.972e24,
        'radius_km': 6371,
        'period_days': 365.25,
        'eccentricity': 0.0167,
        'velocity_km_s': 29.78,
        'surface_gravity_m_s2': 9.81,
        'temperature': '-89 to 57°C',
        'type': 'Terrestrial Planet',
        'description': 'Only known planet with liquid surface water and life. Protected by a magnetic field and ozone layer. One natural satellite.',
        'moons': ['Moon'],
    },
    'Mars': {
        'dist_au': 1.524,
        'mass_kg': 6.417e23,
        'radius_km': 3390,
        'period_days': 687.0,
        'eccentricity': 0.0934,
        'velocity_km_s': 24.07,
        'surface_gravity_m_s2': 3.72,
        'temperature': '-140 to 20°C',
        'type': 'Terrestrial Planet',
        'description': 'The Red Planet. Thin CO2 atmosphere. Home to Olympus Mons (tallest volcano) and Valles Marineris (largest canyon) in the solar system.',
        'moons': ['Phobos', 'Deimos'],
    },
    'Jupiter': {
        'dist_au': 5.203,
        'mass_kg': 1.899e27,
        'radius_km': 69911,
        'period_days': 4332.6,
        'eccentricity': 0.0489,
        'velocity_km_s': 13.07,
        'surface_gravity_m_s2': 24.79,
        'temperature': '-110°C (cloud tops)',
        'type': 'Gas Giant',
        'description': 'Largest planet. Mass is 2.5x all other planets combined. Great Red Spot is a storm larger than Earth lasting 350+ years. Strong magnetic field.',
        'moons': ['Io', 'Europa', 'Ganymede', 'Callisto'],
    },
    'Saturn': {
        'dist_au': 9.537,
        'mass_kg': 5.685e26,
        'radius_km': 58232,
        'period_days': 10759,
        'eccentricity': 0.0565,
        'velocity_km_s': 9.68,
        'surface_gravity_m_s2': 10.44,
        'temperature': '-140°C (cloud tops)',
        'type': 'Gas Giant',
        'description': 'Known for its spectacular ring system made of ice and rock. Least dense planet — would float in water. 146 known moons.',
        'moons': ['Enceladus', 'Tethys', 'Dione', 'Rhea', 'Titan', 'Iapetus'],
    },
    'Uranus': {
        'dist_au': 19.19,
        'mass_kg': 8.681e25,
        'radius_km': 25362,
        'period_days': 30687,
        'eccentricity': 0.0457,
        'velocity_km_s': 6.80,
        'surface_gravity_m_s2': 8.87,
        'temperature': '-195°C (cloud tops)',
        'type': 'Ice Giant',
        'description': 'Rotates on its side (98° axial tilt), likely from an ancient collision. Blue-green color from methane in atmosphere. Faint ring system.',
        'moons': ['Miranda', 'Ariel', 'Umbriel', 'Titania', 'Oberon'],
    },
    'Neptune': {
        'dist_au': 30.07,
        'mass_kg': 1.024e26,
        'radius_km': 24622,
        'period_days': 60190,
        'eccentricity': 0.0113,
        'velocity_km_s': 5.43,
        'surface_gravity_m_s2': 11.15,
        'temperature': '-200°C (cloud tops)',
        'type': 'Ice Giant',
        'description': 'Windiest planet with speeds up to 2,100 km/h. Deep blue from methane absorption. Has the largest moon with a retrograde orbit (Triton).',
        'moons': ['Proteus', 'Triton'],
    },
    'Ceres': {
        'dist_au': 2.77,
        'mass_kg': 9.39e20,
        'radius_km': 473,
        'period_days': 1680,
        'eccentricity': 0.0758,
        'velocity_km_s': 17.90,
        'surface_gravity_m_s2': 0.28,
        'temperature': '-105°C (average)',
        'type': 'Dwarf Planet (Asteroid Belt)',
        'description': 'Largest object in the asteroid belt. Contains subsurface ocean of salty water. Bright spots are sodium carbonate deposits. Visited by Dawn spacecraft.',
        'moons': [],
    },
    'Pluto': {
        'dist_au': 39.48,
        'mass_kg': 1.303e22,
        'radius_km': 1188,
        'period_days': 90560,
        'eccentricity': 0.2488,
        'velocity_km_s': 4.74,
        'surface_gravity_m_s2': 0.62,
        'temperature': '-230°C (average)',
        'type': 'Dwarf Planet (Kuiper Belt)',
        'description': 'Reclassified from planet in 2006. Heart-shaped nitrogen ice plain (Sputnik Planitia). Binary system with Charon. Visited by New Horizons in 2015.',
        'moons': ['Charon', 'Nix', 'Hydra'],
    },
    'Haumea': {
        'dist_au': 43.13,
        'mass_kg': 4.006e21,
        'radius_km': 816,
        'period_days': 103774,
        'eccentricity': 0.1912,
        'velocity_km_s': 4.53,
        'surface_gravity_m_s2': 0.40,
        'temperature': '-241°C (estimated)',
        'type': 'Dwarf Planet (Kuiper Belt)',
        'description': 'Fastest rotating large body in the solar system (3.9 hour day). Elongated egg shape from rapid spin. Has a faint ring system. Named after Hawaiian goddess of fertility.',
        'moons': ["Hi'iaka", 'Namaka'],
    },
    'Makemake': {
        'dist_au': 45.79,
        'mass_kg': 3.1e21,
        'radius_km': 715,
        'period_days': 111845,
        'eccentricity': 0.1559,
        'velocity_km_s': 4.42,
        'surface_gravity_m_s2': 0.37,
        'temperature': '-243°C (estimated)',
        'type': 'Dwarf Planet (Kuiper Belt)',
        'description': 'Second brightest Kuiper Belt object after Pluto. Reddish-brown surface with frozen methane and ethane. Named after Rapa Nui creator god.',
        'moons': [],
    },
    'Eris': {
        'dist_au': 67.78,
        'mass_kg': 1.66e22,
        'radius_km': 1163,
        'period_days': 204199,
        'eccentricity': 0.4407,
        'velocity_km_s': 3.43,
        'surface_gravity_m_s2': 0.82,
        'temperature': '-243°C (estimated)',
        'type': 'Dwarf Planet (Scattered Disc)',
        'description': 'Most massive known dwarf planet. Its discovery triggered Pluto\'s reclassification. Highly elliptical orbit ranging from 38 to 98 AU. Named after Greek goddess of discord.',
        'moons': ['Dysnomia'],
    },
}
MOON_DATA = {
    # ---- Earth ----
    'Moon': {
        'parent': 'Earth',
        'dist_km': 384400,
        'period_days': 27.32,
        'radius_km': 1737,
        'mass_kg': 7.342e22,
        'color': (169, 169, 169),
        'description': 'Fifth largest moon. Tidally locked to Earth. Only celestial body visited by humans. Stabilizes Earth\'s axial tilt.',
    },
    # ---- Mars ----
    'Phobos': {
        'parent': 'Mars',
        'dist_km': 9376,
        'period_days': 0.32,
        'radius_km': 11,
        'mass_kg': 1.066e16,
        'color': (139, 119, 101),
        'description': 'Larger of Mars\'s two moons. Irregular shape. Orbits closer to its planet than any other known moon. Slowly spiraling inward.',
    },
    'Deimos': {
        'parent': 'Mars',
        'dist_km': 23463,
        'period_days': 1.26,
        'radius_km': 6,
        'mass_kg': 1.476e15,
        'color': (180, 166, 152),
        'description': 'Smaller of Mars\'s moons. Smooth surface. Slowly drifting away from Mars.',
    },
    # ---- Jupiter (Galilean moons) ----
    'Io': {
        'parent': 'Jupiter',
        'dist_km': 421700,
        'period_days': 1.77,
        'radius_km': 1822,
        'mass_kg': 8.932e22,
        'color': (255, 200, 50),
        'description': 'Most volcanically active body in the solar system. Over 400 active volcanoes. Surface constantly reshaped by lava flows. Tidal heating from Jupiter.',
    },
    'Europa': {
        'parent': 'Jupiter',
        'dist_km': 671034,
        'period_days': 3.55,
        'radius_km': 1561,
        'mass_kg': 4.800e22,
        'color': (220, 210, 200),
        'description': 'Smoothest surface in the solar system. Ice shell covering a global subsurface ocean. Prime candidate for extraterrestrial life. NASA Europa Clipper mission en route.',
    },
    'Ganymede': {
        'parent': 'Jupiter',
        'dist_km': 1070412,
        'period_days': 7.15,
        'radius_km': 2634,
        'mass_kg': 1.482e23,
        'color': (160, 145, 130),
        'description': 'Largest moon in the solar system — bigger than Mercury. Only moon with its own magnetic field. Has a subsurface saltwater ocean.',
    },
    'Callisto': {
        'parent': 'Jupiter',
        'dist_km': 1882709,
        'period_days': 16.69,
        'radius_km': 2410,
        'mass_kg': 1.076e23,
        'color': (100, 100, 110),
        'description': 'Most heavily cratered body in the solar system. Ancient surface unchanged for 4 billion years. Possible subsurface ocean. Considered for a future human base.',
    },
    # ---- Saturn ----
    'Enceladus': {
        'parent': 'Saturn',
        'dist_km': 237948,
        'period_days': 1.37,
        'radius_km': 252,
        'mass_kg': 1.080e20,
        'color': (240, 245, 255),
        'description': 'Geysers at the south pole spray water ice into space, feeding Saturn\'s E ring. Subsurface ocean with hydrothermal vents. Top candidate for finding life.',
    },
    'Tethys': {
        'parent': 'Saturn',
        'dist_km': 294619,
        'period_days': 1.89,
        'radius_km': 531,
        'mass_kg': 6.175e20,
        'color': (200, 200, 210),
        'description': 'Almost entirely water ice. Massive Odysseus crater spans 2/5 of its diameter. Huge rift valley Ithaca Chasma stretches 2,000 km.',
    },
    'Dione': {
        'parent': 'Saturn',
        'dist_km': 377396,
        'period_days': 2.74,
        'radius_km': 561,
        'mass_kg': 1.095e21,
        'color': (200, 200, 210),
        'description': 'Ice cliffs and bright wispy terrain. Possible subsurface ocean. Shares its orbit with two small trojan moons.',
    },
    'Rhea': {
        'parent': 'Saturn',
        'dist_km': 527108,
        'period_days': 4.52,
        'radius_km': 764,
        'mass_kg': 2.307e21,
        'color': (200, 200, 210),
        'description': 'Saturn\'s second largest moon. May have a faint ring system — would be the first moon known to have rings. Heavily cratered icy surface.',
    },
    'Titan': {
        'parent': 'Saturn',
        'dist_km': 1221870,
        'period_days': 15.95,
        'radius_km': 2575,
        'mass_kg': 1.345e23,
        'color': (230, 190, 100),
        'description': 'Only moon with a thick atmosphere. Liquid methane lakes and rivers on the surface. Dragonfly rotorcraft mission planned for 2030s. Larger than Mercury.',
    },
    'Iapetus': {
        'parent': 'Saturn',
        'dist_km': 3560820,
        'period_days': 79.32,
        'radius_km': 735,
        'mass_kg': 1.806e21,
        'color': (200, 200, 210),
        'description': 'Two-toned surface: one hemisphere bright ice, other dark carbon. Massive equatorial ridge up to 20 km high. Walnut-shaped appearance.',
    },
    # ---- Uranus ----
    'Miranda': {
        'parent': 'Uranus',
        'dist_km': 129390,
        'period_days': 1.41,
        'radius_km': 236,
        'mass_kg': 6.59e19,
        'color': (180, 180, 190),
        'description': 'Most geologically diverse moon for its size. Verona Rupes — tallest known cliff in the solar system at 20 km. May have been shattered and reassembled.',
    },
    'Ariel': {
        'parent': 'Uranus',
        'dist_km': 190020,
        'period_days': 2.52,
        'radius_km': 579,
        'mass_kg': 1.251e21,
        'color': (180, 180, 190),
        'description': 'Brightest and youngest surface of Uranus\'s major moons. Extensive canyon systems. Evidence of relatively recent geological activity.',
    },
    'Umbriel': {
        'parent': 'Uranus',
        'dist_km': 266300,
        'period_days': 4.14,
        'radius_km': 585,
        'mass_kg': 1.172e21,
        'color': (180, 180, 190),
        'description': 'Darkest of Uranus\'s large moons. Ancient, heavily cratered surface. Mysterious bright ring on the floor of Wunda crater.',
    },
    'Titania': {
        'parent': 'Uranus',
        'dist_km': 435910,
        'period_days': 8.71,
        'radius_km': 788,
        'mass_kg': 3.527e21,
        'color': (180, 180, 190),
        'description': 'Largest moon of Uranus. Enormous canyon system Messina Chasmata. Evidence of past internal activity. Named after the queen of fairies in A Midsummer Night\'s Dream.',
    },
    'Oberon': {
        'parent': 'Uranus',
        'dist_km': 583520,
        'period_days': 13.46,
        'radius_km': 761,
        'mass_kg': 3.014e21,
        'color': (160, 155, 150),
        'description': 'Outermost major moon of Uranus. Heavily cratered. Some craters have dark material on their floors. Named after the king of fairies.',
    },
    # ---- Neptune ----
    'Proteus': {
        'parent': 'Neptune',
        'dist_km': 117647,
        'period_days': 1.12,
        'radius_km': 210,
        'mass_kg': 4.4e19,
        'color': (180, 180, 190),
        'description': 'Largest of Neptune\'s inner moons. Irregular shape — nearly as large as a body can be without being pulled into a sphere by its own gravity.',
    },
    'Triton': {
        'parent': 'Neptune',
        'dist_km': 354759,
        'period_days': -5.88,
        'radius_km': 1353,
        'mass_kg': 2.14e22,
        'color': (180, 200, 210),
        'description': 'Only large moon with a retrograde orbit — likely a captured Kuiper Belt object. Nitrogen geysers. Coldest measured surface in the solar system (-235°C).',
    },
    # ---- Pluto ----
    'Charon': {
        'parent': 'Pluto',
        'dist_km': 19591,
        'period_days': 6.39,
        'radius_km': 606,
        'mass_kg': 1.586e21,
        'color': (150, 150, 160),
        'description': 'Half the size of Pluto — sometimes called a binary system. Both are tidally locked facing each other. Red polar cap of tholins.',
    },
    'Nix': {
        'parent': 'Pluto',
        'dist_km': 48694,
        'period_days': 24.85,
        'radius_km': 23,
        'mass_kg': 4.5e16,
        'color': (180, 180, 180),
        'description': 'Small irregular moon. Chaotic rotation — tumbles unpredictably due to gravitational influence of Pluto and Charon.',
    },
    'Hydra': {
        'parent': 'Pluto',
        'dist_km': 64738,
        'period_days': 38.20,
        'radius_km': 25,
        'mass_kg': 4.8e16,
        'color': (180, 180, 180),
        'description': 'Outermost known moon of Pluto. Irregular shape. Also tumbles chaotically like Nix. Discovered in 2005 by Hubble.',
    },
    # ---- Eris ----
    'Dysnomia': {
        'parent': 'Eris',
        'dist_km': 37273,
        'period_days': 15.77,
        'radius_km': 350,
        'mass_kg': 8.2e19,
        'color': (160, 160, 170),
        'description': 'Only known moon of Eris. Named after the daughter of Eris (goddess of lawlessness). Used to calculate Eris\'s mass.',
    },
    # ---- Haumea ----
    "Hi'iaka": {
        'parent': 'Haumea',
        'dist_km': 49880,
        'period_days': 49.12,
        'radius_km': 155,
        'mass_kg': 1.79e19,
        'color': (200, 200, 210),
        'description': 'Larger of Haumea\'s two moons. Named after Hawaiian goddess of the island of Hawaii. Nearly circular orbit.',
    },
    'Namaka': {
        'parent': 'Haumea',
        'dist_km': 25657,
        'period_days': 18.28,
        'radius_km': 85,
        'mass_kg': 1.79e18,
        'color': (190, 190, 200),
        'description': 'Smaller inner moon of Haumea. Named after Hawaiian water spirit. Eccentric and inclined orbit.',
    },
}
  
sun_body = Planet("Sun", YELLOW, 1.989e30, 0, 0, 30)
sun_body.sun = True

mercury = Planet("Mercury", BROWN, 3.301e23, 0.387 * Planet.AU, 0, 8, 47360 )
venus    = Planet("Venus", GREEN, 4.867e24, 0.723 * Planet.AU, 0, 14, 35020)
earth    = Planet("Earth", BLUE, 5.972e24, 1.0 * Planet.AU, 0, 16, 29780)
mars     = Planet("Mars", RED, 6.417e23, 1.524 * Planet.AU, 0, 12, 24070)
jupiter  = Planet("Jupiter", ORANGE, 1.899e27, 5.203 * Planet.AU, 0, 28, 13070)
saturn   = Planet("Saturn", TAN, 5.685e26, 9.537 * Planet.AU, 0, 24, 9680)
uranus   = Planet("Uranus", LIGHT_BLUE, 8.681e25, 19.19 * Planet.AU, 0, 18, 6800)
neptune  = Planet("Neptune", DARK_BLUE, 1.024e26, 30.07 * Planet.AU, 0, 18, 5430)

ceres    = Planet("Ceres", (169, 169, 169), 9.39e20, 2.77 * Planet.AU, 0, 6, 17900)
pluto    = Planet("Pluto", (210, 180, 140), 1.303e22, 29.66 * Planet.AU, 0, 8, 6100)
haumea   = Planet("Haumea", (180, 160, 150), 4.006e21, 34.72 * Planet.AU, 0, 6, 5520)
makemake = Planet("Makemake", (160, 120, 100), 3.1e21, 38.59 * Planet.AU, 0, 6, 5240)
eris     = Planet("Eris", (200, 200, 210), 1.66e22, 37.91 * Planet.AU, 0, 8, 5580)

planets = [
    sun_body,
    mercury, venus, earth, mars, jupiter, saturn, uranus, neptune,
    ceres, pluto, haumea, makemake, eris,]


running = True

camera = Camera()

font_name = pygame.font.SysFont("Arial", 13)
font_hud_title = pygame.font.SysFont("Arial", 22, bold=True)

selected_planet = None


while running:

    for event in pygame.event.get():
        camera.handle_input(event)
        
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            for planet in planets:
                planet.hovered = planet.hit_test(mouse_x, mouse_y, camera)   
                    
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_x < PANEL_SPLIT:
                for planet in planets:
                    if planet.hit_test(mouse_x, mouse_y, camera):
                        select_planet(planet)
                        break
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                if selected_planet:
                    selected_planet.selected = False
                selected_planet = None
                system_paused = False     

    screen.fill(BLACK)
    screen.set_clip((0,0, PANEL_SPLIT, HEIGHT))
    
    for planet in planets:
        if planet == sun_body:
            continue
        
        if PLANET_DATA[planet.name]['eccentricity'] > 0.1:
            continue
        
        orbit_radius = PLANET_DATA[planet.name]['dist_au'] * Planet.AU * camera.base_scale * camera.zoom
        
        if orbit_radius > 2:
            sun_sx, sun_sy = camera.world_to_screen(0, 0)
            pygame.draw.circle(screen, (30, 30, 30), (sun_sx, sun_sy), int(orbit_radius), 1)
        
    
    forces = {}
    
    for planet in planets:
        if planet == sun_body:
            continue
        
        total_fx = 0
        total_fy = 0
        
        for other_planet in planets:
            if planet == other_planet:
                continue
            (fx, fy) = planet.attraction(other_planet)
            total_fx += fx
            total_fy += fy
        
        forces[planet.name] = (total_fx, total_fy)
    
    for planet in planets:
        if planet == sun_body:
            continue
        
        (fx, fy) = forces[planet.name]
        
        planet.x_vel += (fx / planet.mass) * planet.TIMESTEP
        planet.y_vel += (fy / planet.mass) * planet.TIMESTEP 
        
        planet.x += planet.x_vel * planet.TIMESTEP
        planet.y += planet.y_vel * planet.TIMESTEP
    
    for planet in planets:
        planet.draw(screen, camera)

    screen.set_clip(None)
    
    pygame.draw.line(screen, (60,60,60), (PANEL_SPLIT,0), (PANEL_SPLIT, HEIGHT), 1)
    

    if selected_planet:
        info = PLANET_DATA[selected_planet.name]
        hud_x = PANEL_SPLIT + 30
        y = 30
        
        # Title
        title = font_hud_title.render(selected_planet.name, True, selected_planet.color)
        screen.blit(title, (hud_x, y))
        y += 30
        
        # Type
        type_text = font_name.render(info['type'], True, (150, 150, 150))
        screen.blit(type_text, (hud_x, y))
        y += 30
        
        # Separator line
        pygame.draw.line(screen, (60, 60, 60), (hud_x, y), (WIDTH - 30, y), 1)
        y += 15
        
        # Info rows
        rows = [
            ('Distance', format_au(info['dist_au'])),
            ('Orbital Period', format_period(info['period_days'])),
            ('Mass', format_mass(info['mass_kg'])),
            ('Velocity', f"{info['velocity_km_s']} km/s"),
            ('Eccentricity', f"{info['eccentricity']}"),
            ('Radius', format_radius(info['radius_km'])),
            ('Surface Gravity', format_gravity(info['surface_gravity_m_s2'])),
            ('Temperature', format_temp(info['temperature'])),
            ('Moons', str(len(info['moons']))),
        ]
        
        for label, value in rows:
            label_text = font_name.render(f"{label}:", True, (120, 120, 120))
            value_text = font_name.render(value, True, (200, 200, 200))
            screen.blit(label_text, (hud_x, y))
            screen.blit(value_text, (hud_x + 150, y))
            y += 20
    
    pygame.display.update()

    clock.tick(60)

pygame.quit()