import pygame
import pygame_menu

pygame.init()
screen = pygame.display.set_mode((600, 400))


class Game:
	screen = None
	aliens = []
	rockets = []
	lost = False
	win = False

	def __init__(self, width, height, difficulty):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.fondo = pygame.image.load("Recursos/fondo.png")
		self.difficulty = difficulty
		done = False

		hero = Hero(self, width/2, height-50)
		generator = Generator(self, self.difficulty[0])

		while not done:
			if len(self.aliens) == 0:
				self.win = True
				self.displayText("¡VICTORIA!")

			pressed = pygame.key.get_pressed()
			if pressed[pygame.K_LEFT]:
				hero.x -= self.difficulty[2] if hero.x > 20 else 0
			elif pressed[pygame.K_RIGHT]:
				hero.x += self.difficulty[2] if hero.x < width-20 else 0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and
						not self.lost and not self.win and len(self.rockets) < self.difficulty[1]):
					self.rockets.append(Rocket(self, hero.x, hero.y))

			pygame.display.flip()
			self.clock.tick(60)
			# self.screen.fill((204,59,91))
			self.screen.blit(self.fondo, (0, 0))

			for alien in self.aliens:
				alien.draw()
				alien.checkCollision(self)
				if alien.y > height:
					self.lost = True
					self.displayText("GAME OVER")
			for rocket in self.rockets:
				rocket.draw()
				if rocket.y <= 0:
					self.rockets.remove(rocket)

			if not self.lost and not self.win: hero.draw()

	def displayText(self, text):
		pygame.font.init()
		font = pygame.font.SysFont("Arial", 50)
		textSurface = font.render(text, False, (67, 238, 10))
		self.screen.blit(textSurface, (180, 140))


class Alien:
	def __init__(self, game, x, y, velocity):
		self.game = game
		self.x = x
		self.y = y
		self.size = 30
		self.image = pygame.image.load("Recursos/alien.png")
		self.velocity = velocity

	def draw(self):
		# pygame.draw.rect(self.game.screen, (50, 168, 82), pygame.Rect(self.x, self.y, self.size, self.size))
		self.game.screen.blit(self.image, (self.x, self.y))
		self.y += self.velocity

	def checkCollision(self, game):
		for rocket in game.rockets:
			if (rocket.x < self.x + self.size and
					rocket.x > self.x - self.size and
					rocket.y < self.y + self.size and
					rocket.y > self.y - self.size):
				game.rockets.remove(rocket)
				game.aliens.remove(self)


class Hero:
	def __init__(self, game, x, y):
		self.game = game
		self.x = x
		self.y = y
		self.image = pygame.image.load("Recursos/nave.png")

	def draw(self):
		# pygame.draw.rect(self.game.screen, (39, 160, 166), pygame.Rect(self.x, self.y, 8, 5))
		self.game.screen.blit(self.image, (self.x, self.y))


class Rocket:
	def __init__(self, game, x, y):
		self.game = game
		self.x = x
		self.y = y
		self.image = pygame.image.load("Recursos/rocket.png")
		self.sound = pygame.mixer.Sound("Recursos/rocket_sound.wav")
		self.sound.play()

	def draw(self):
		# pygame.draw.rect(self.game.screen, (67, 238, 10), pygame.Rect(self.x, self.y, 4, 6))
		self.game.screen.blit(self.image, (self.x, self.y))
		self.y -= 2


class Generator:
	def __init__(self, game, velocity):
		margin = 30
		width = 50
		for x in range(margin, game.width - margin, width):
			for y in range(margin, game.height // 2, width):
				game.aliens.append(Alien(game, x, y, velocity))


def start_easy():
	Game(600, 400, (0.1, 4, 4))


def start_medium():
	Game(600, 400, (0.2, 3, 3))


def start_hard():
	Game(600, 400, (0.3, 3, 2))


def start_hell():
	Game(600, 400, (0.3, 2, 2))


def switch_music():
	if pygame.mixer.music.get_volume() != 0:
		pygame.mixer.music.set_volume(0)
	else:
		pygame.mixer.music.set_volume(1)


# Crear el menú, darle nombre y dimensiones
menu = pygame_menu.Menu(width=600, height=400, theme=pygame_menu.themes.THEME_DARK, title="Bienvenido")
# Crear el mixer e inicializar la musica
pygame.mixer.music.load("Recursos/song.wav")
pygame.mixer.music.play(-1)

menu.add.button("Easy", start_easy)	# Crear el botón easy
menu.add.button("Medium", start_medium)	# Crear el botón medium
menu.add.button("Hard", start_hard)	# Crear el botón hard
menu.add.button("Hell", start_hell)	# Crear el botón hell
menu.add.button("Mute/Unmute music", switch_music)	# Crear el botón mute/unmute
menu.add.button("Quit", pygame_menu.events.EXIT)	# Crear el botón quit

if __name__ == "__main__":
	menu.mainloop(screen)
