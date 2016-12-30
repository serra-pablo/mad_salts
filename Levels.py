from Game_components import *
from Graphics import controller as graphics_handler
CAMERA_WIDTH = graphics_handler.CAMERA_WIDTH
CAMERA_HEIGHT = graphics_handler.CAMERA_HEIGHT

# make an Object file, and add all needed resources (based on folder position and file names)

class Level():
    """A class with level resources, and helper functions"""

    def __init__(self, level_name, player, static_world_components, dynamic_world_components, background=None, level_size=None):
        if level_size == None:
            level_size = background.size
        self.level_size = level_size
        self.level_name = level_name
        # a dictionary with all level related game components
        self.player = player
        self.playing_entities = []  # starts empty; is filled by monsters, and other NPC
        self.npcs = pygame.sprite.Group()
        self.static_components = static_world_components  # level parts (e.g. background, ground)
        self.dynamic_components = dynamic_world_components  # level parts (e.g. swings, moving objects, bullets)
        self.components = [] + self.static_components + self.dynamic_components  # redundant list; fast requesting level component
        # build the game depth:
        self.level = pygame.Surface(level_size)
        self.level_rect = self.level.get_rect()
        if background is not None:
            self.level.blit(background.sprite, background.rect)
        for component in static_world_components:
            if type(component) == Background:
                self.level.blit(component.sprite, component.rect)
            if type(component) == Ground:
                self.level.blit(component.sprite, component.rect)
            if type(component) == ForeGround:
                self.level.blit(component.sprite, component.rect)

        # todo: revise graphics handler camera setting
        self.camera = None # Camera(complex_camera, player.rect, level_size)  # the screen view
        #graphics_handler.set_camera(self.camera)  # makes it possible to blit directly to the graphics handler

        print("[+] level '{}' loaded".format(level_name))

    def __getattr__(self, name):
        try:
            return self.components[name]
        except ValueError: pass  # requested name isn't a game component, do default behaviour
        except TypeError: pass
        return self.__getattribute__(name)

    # find player ground
    def find_player_ground(self):
        pass #x = self.player.rect.x

    # game component management
    def add_NPC(self, npc):
        self.add_game_component('NPC', npc)

    def add_world_component(self, world_component):
        self.add_game_component('world_component', world_component)

    # when adding a component to a level, this methid should be used exclusively
    def add_game_component(self, component):
        self.components.append(component)

    def del_game_component(self, component_type, component):
        del self.dynamic_components[component_type][component]  # component should have __eq__ overridden
        del self.components[component]

    def get_dynamic_components(self):
        """builds a (flat) list with all dynamic game component"""
        return [x for x in self.dynamic_components]

    def get_game_components(self):
        """Builds a new list with all static and dynamic components"""
        # first get the static components, as these will be blitted over by the dynamic ones
        return [x for x in self.components]

    def update(self, dt):
        """update all level components in the current level"""
        for component in self.dynamic_components:
            component.update(dt)
        if self.camera:
            self.camera.update(self.player.rect)
        self.player.update(dt)

    # displays all level components from back- to foreground
    def display(self):
        """calls display on every component; blitting them, and adding their rectangle to a dirty rectangles list"""
        graphics_controller.blit(self.level, self.level_rect)
        for component in self.static_components:
            component.display(self.camera)
        self.player.display()
        for dynamic_component in self.dynamic_components:
            dynamic_component.display(self.camera)

    def __del__(self):
        graphics_handler.unset_camera()
        print("[LL] level '{}' unloaded".format(self.level_name))


# level parts handling
class StaticLevelComponent(GraphicsComponent):
    """Base class for all level building blocks"""

    def __init__(self, resource_name, pos, size=None):
        # if the size is None; it will be determined by the sprite resolution
        if size is not None and len(size) != 2:
            raise ValueError("Size has to be a tuple of length 2!")
        self.TYPE = resource_name  # A correct name is needed for (sprite) init
        super(StaticLevelComponent, self).__init__(pos, size)

    def init_sprite(self):
        self.sprite = pygame.transform.smoothscale(self.sprite, self.size).convert()


class Background(StaticLevelComponent):
    """Background"""
    TYPE = 'Background'
    def scale_background_to_camera(self, size):
        if size is not None:  # if the size is smaller than the camera, it will scale the to the camera size
            if size[0] <= CAMERA_WIDTH:
                size = (CAMERA_WIDTH, size[1])
            if size[1] <= CAMERA_HEIGHT:
                size = (size[0], CAMERA_HEIGHT)

            return size # do something with this

class ForeGround(StaticLevelComponent):
    """ForeGround"""
    TYPE = 'Foreground'

class Ground(StaticLevelComponent):
    """ground"""
    TYPE = 'ground'

    def __init__(self, resource_name, pos, size=None):
        super(Ground, self).__init__(resource_name, pos, size=None)


# level builder; calls level init
# component order matters!
def level_builder(level_number):
    world_component_types = ['Background', 'Foreground', 'Ground']
    # any component that is part of the world should be added to world_components list
    static_level_components = []  # additional dynamic blocks and other level_number components
    dynamic_level_components = []

    if level_number == 0:
        level_name = 'forest'
        level_size = (CAMERA_WIDTH*2, CAMERA_HEIGHT)
        player = Player((50, 50))  # player and it's starting position in the level_number
        background = Background('background3', level_size)

        static_level_components.append(Ground('forest_ground_p0', (0, level_size[1] / 2)))

        # dynamic_level_components
    elif level_number == 1:
        raise NotImplementedError("Level value hasn't been implemented!")
        level_name = ''
        player = Player((0, 0))

        # static_level_components
        # dynamic_level_components
    else:
        raise NotImplementedError("Level value hasn't been implemented!")

    return Level(level_name, player, static_level_components, dynamic_level_components, background=background)
