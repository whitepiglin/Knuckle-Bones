import os
import pygame

def load_image(path):
    image = pygame.image.load(path).convert_alpha()
    return image

def load_images(path):
    images = []
    for image_name in os.listdir(path):
        images.append(load_image(path + '/' + image_name))
    return images