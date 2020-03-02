import pygame
from colourblind_creator import Dots
from tkinter import *
pygame.init()


class SettingsWindow(Frame):
    def __init__(self, master: Tk):
        """
        Constructor
        :param master: Tk for which window is created on
        """
        # Creating window and calling create_widgets func
        super().__init__(master)
        self.master = master
        self.pack()
        self.iv = IntVar()
        self.create_widgets()

    def get_radio(self) -> None:
        """
        Called when start button is pressed
        :return: None
        """
        # Only quits if a radio button has been pressed
        if self.iv.get():
            self.master.destroy()

    def create_widgets(self) -> None:
        """
        Creates radio buttons and start button
        :return: None
        """
        label = Label(self, text="Choose type: ")
        label.pack()
        # Loops to create radio buttons
        for txt, v in [("red-green", 1), ("green-red", 2), ("blue-yellow", 3)]:
            r = Radiobutton(self, text=txt, variable=self.iv, value=v)
            r.pack()
        button = Button(self, text="START", command=self.get_radio)
        button.pack()


def settings():
    root = Tk()
    root.title("Settings")
    app = SettingsWindow(root)
    app.mainloop()
    return app.iv.get()


# Called to choose which blindness option
choice = settings()

# Creating main window and misc variables
width, height = 820, 720
display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
load_bar_outer = pygame.Rect(780, 10, 30, 700)

# Initiates Dots class to start making dots to be drawn
dots = Dots(2000, 7, 2, choice)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    display.fill((255, 255, 255))

    # Draws dots
    for p, dot in enumerate(dots.dots):
        pygame.draw.circle(display, dot.colour, (dot.x, dot.y), dot.radius)

    # Draws loading bar
    pygame.draw.rect(display, (0, 0, 0), load_bar_outer)
    pygame.draw.rect(display, (0, 255, 0), pygame.Rect(785, 15, 20, 690 * dots.percentage))

    pygame.display.update()
    clock.tick(60)

pygame.image.save(display, "colour_dots.bmp")

pygame.quit()
