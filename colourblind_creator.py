import pygame
from random import randint, choice
import threading
from PIL import Image
from typing import Callable


class Dot:
    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour


class Dots:
    def __init__(
            self, cc: int, u: int, l: int, optn: int,
            func: Callable[[int, int], bool]=None, radius: int=350, img_name: str="read_img.bmp"
    ):
        """
        Constructor
        :param cc: The amount of circles to draw
        :param u: Highest radius of dot
        :param l: Lowest radius of dot
        :param optn: Type of blindness colours
        :param func: Graph function to run coords through - default if circles function
        :param radius: Radius of main circle or width of shape if not circle
        """
        self.circle_count = cc
        # Randomly generating each radius
        self.__radi = [randint(l, u) for _ in range(self.circle_count)]
        self.dots = []
        self.__radius = radius
        # Graph function
        self.__func = (lambda x1, y1: (x1 - 360) ** 2 + (y1 - 360) ** 2 <= self.__radius ** 2) if func is None else func
        assert isinstance(self.__func(0, 0), bool), "function didn't return boolean"
        # Loading image
        img = Image.open(img_name)
        pixels = img.load()
        # Creating pixel list
        self.__img_coords = [[pixels[i, j] for j in range(720)] for i in range(720)]
        self.percentage = 0
        self.__optn = optn
        # Starting make_dots thread to do task in background
        threading.Thread(target=self.make_dots, daemon=True).start()

    def make_dots(self) -> bool:
        """
        Threaded function to create colour dots
        :return: Bool to stop thread when done
        """
        # Colour dict for each blindness type
        colours = {
            "red-green": {
                "outer": [
                    (196, 118, 67), (230, 168, 115), (179, 114, 86), (211, 152, 119), (233, 150, 103), (197, 121, 71)
                ],
                "inner": [
                    (65, 171, 111), (191, 188, 109), (136, 146, 77), (193, 186, 109), (146, 186, 119), (170, 177, 115)
                ]
            },
            "green-red": {
                "outer": [
                    (65, 171, 111), (191, 188, 109), (136, 146, 77), (193, 186, 109), (146, 186, 119), (170, 177, 115)
                ],
                "inner": [
                    (196, 118, 67), (230, 168, 115), (179, 114, 86), (211, 152, 119), (233, 150, 103), (197, 121, 71)
                ]
            },
            "blue-yellow": {
                "outer": [
                    (147, 160, 140), (60, 74, 70), (101, 111, 103), (150, 162, 140), (107, 114, 107), (93, 100, 93)
                ],
                "inner": [
                    (216, 152, 127), (212, 131, 105), (216, 73, 77), (133, 86, 96), (196, 134, 130), (214, 155, 141)
                ]
            }
        }
        # Assigning which blindness option to use
        optn = [i[1] for i in enumerate(colours) if i[0] == self.__optn - 1][0]
        count = 0
        # Loop to randomly make circle fit inside bounds
        while True:
            # Allowed 10 pixels each side to adjust for bigger radii
            x = randint(10, (self.__radius * 2))
            y = randint(10, (self.__radius * 2))
            # If coords satisfy func
            if self.__func(x, y):
                # Checking circle collision
                n = pygame.Rect(0, 0, self.__radi[count] * 2, self.__radi[count] * 2)
                n.center = (x, y)
                able = []
                for p, i in enumerate(self.dots):
                    r = pygame.Rect(0, 0, self.__radi[p] * 2, self.__radi[p] * 2)
                    r.center = (i.x, i.y)
                    if r.colliderect(n):
                        able.append(False)
                    else:
                        able.append(True)
                # If circle doesnt collide with anything it is allowed
                if all(able):
                    col = choice(colours[optn]["inner"]) if self.__img_coords[x][y] == 0 else choice(colours[optn]["outer"])
                    self.dots.append(Dot(x, y, self.__radi[count], col))
                    count += 1
                    self.percentage = len(self.dots) / self.circle_count
            # If all circles are placed the break
            if count == self.circle_count:
                return False
