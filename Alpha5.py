import pygame
import sys
import json

# Initialize Pygame
pygame.init()

# Set up the game window
window_size = (1800, 1000)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Game with Region Data')

# Load the main image with multiple colored regions (used for detection)
colored_regions_image = pygame.image.load('Emjata2.png').convert()

# Load the actual game map image (visible to the player)
game_map_image = pygame.image.load('Emjata.png').convert()

# Load resource data from JSON file
with open('resources.json') as f:
    resource_data = json.load(f)

class Region:
    def __init__(self, color, name, owner, resources, tpno, units):
        self.color = color  # The unique color representing this region
        self.name = name  # Name of the region
        self.owner = owner  # Current owner of the region
        self.resources = resources  # Resources produced by the region
        self.mask = None  # The mask for detecting mouseover; will be assigned later
        self.tpno = None # Number of Trade Posts
        self.units = None # Number of Units, assigned randomly at start of game

    def display_info(self):
        """Returns a string with information about the region."""
        return f"Region: {self.name}, Owner: {self.owner}, Resources: {self.resources}, TP #: {self.tpno}, Units: {self.units}"

#Define a variable to hold information about the selected region
selected_region_info = None

# Get the size of the image
image_width, image_height = colored_regions_image.get_size()

# Dictionary to hold regions indexed by their color
regions = {}

# Create the masks and assign resources to regions
for x in range(image_width):
    for y in range(image_height):
        # Get the color at the current pixel
        color = colored_regions_image.get_at((x, y))
        color_key = (color.r, color.g, color.b)  # Use RGB only for the unique key

        # Skip transparent pixels
        if color.a == 0:
            continue
        elif color_key == (0,0,0):
            continue

        # If the color is new, create a new Region object and a corresponding mask
        if color_key not in regions:
            # Create a new Region object
            new_region = Region(
                color=color_key,
                name="Unknown",  # Default value
                owner="Neutral",  # Default value
                resources="None",  # Default value
                tpno="None", # Default Value
                units="None" # Default Value
            )

            # Create the mask for this region
            mask = pygame.mask.Mask(colored_regions_image.get_size())
            color_surface = pygame.Surface(colored_regions_image.get_size(), pygame.SRCALPHA)

            # Store the mask in the region object
            new_region.mask = mask
            regions[color_key] = new_region

        # Set the mask bit at the current pixel
        regions[color_key].mask.set_at((x, y))

# Assign resources to regions based on the resource data
for color_key_str, data in resource_data.items():
    color_key = tuple(map(int, color_key_str.strip("()").split(", ")))
    if color_key in regions:
        region = regions[color_key]
        region.name = data.get("name", region.name)
        region.owner = data.get("owner", region.owner)
        region.resources = data.get("resources", region.resources)
        region.tpno = data.get("tpno", region.tpno)
        region.units = data.get("units", region.units)

# Set up font for text box
font = pygame.font.Font(None, 18)

# Game loop
while True:
    window.fill((0,0,0))
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            #Checking that mouse is in-bounds for mask layer
            if mouse_pos[0] < game_map_image.get_width() and mouse_pos[1] < game_map_image.get_height():
                for region in regions.values():
                    if region.mask.get_at((mouse_pos[0],mouse_pos[1])):
                        #Mouse is over the region
                        selected_region_info = region.display_info()

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Draw the colored regions image (not visible, used for detection)
    window.blit(colored_regions_image, (0, 0))

    # Variable to store the info of the region being hovered over
    region_info = None

    if mouse_pos[0] < game_map_image.get_width() and mouse_pos[1] < game_map_image.get_height():
        # Check which region the mouse is over
        for region in regions.values():
            if region.mask.get_at((mouse_pos[0], mouse_pos[1])):
                # Mouse is over this region
                region_info = region.display_info()
                break  # Stop checking after finding the matching region

    # Draw the actual game map
    window.blit(game_map_image, (0, 0))

    # Draw the region info text if a region is found
    if region_info:
        text_surface = font.render(region_info, True, (255, 255, 255))
        window.blit(text_surface, (20, 20))

    if selected_region_info:
        rendered_text = font.render(selected_region_info, True, (255, 255, 255))
        window.blit(rendered_text, (1025,50))

    # Update the display
    pygame.display.update() 
