import pygame
from typing import Optional, Union


class ImageSprite:
    def __init__(
        self,
        x: int,
        y: int,
        image: Union[str, pygame.Surface],
        width: Optional[int] = None,
        height: Optional[int] = None,
        rotation: float = 0,
        alpha: Optional[int] = None,
    ) -> None:
        if isinstance(image, str):
            self.original_image = pygame.image.load(image).convert_alpha()
        else:
            self.original_image = image

        if width and not height:
            height = int(
                (self.original_image.get_height() / self.original_image.get_width())
                * width
            )
        elif height and not width:
            width = int(
                (self.original_image.get_width() / self.original_image.get_height())
                * height
            )

        if width and height:
            self.image = pygame.transform.scale(self.original_image, (width, height))
        else:
            self.image = self.original_image.copy()

        self.rotation = rotation
        self.alpha = alpha

        if self.alpha is not None:
            self.image.set_alpha(self.alpha)

        if self.rotation != 0:
            self.image = pygame.transform.rotate(self.image, self.rotation)

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
