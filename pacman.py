import pygame
import sys
import random

# Variables
operadores = ['+', '-', '*', '/']
visitadas = []

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Game")
clock = pygame.time.Clock()

# Initialize game state
pacman = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = random.choice([UP, DOWN, LEFT, RIGHT])
total_score = 0  # Inicializa la puntuación total
foods_eaten = []  # Inicializa la lista de alimentos comidos


# Inicializa la dirección del pacman y la variable de movimiento
direction = None
moving = False

# Generate food
foods = [random.randint(1, 100)]  # el primer item será un numero random del 0-100

def random_food_position(pacman, food_positions):
    while True:
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if position not in pacman and position not in food_positions:
            return position
food_positions = [random_food_position(pacman, [])]

food_positions = [random_food_position(pacman, food_positions)]

# Functions
def draw_pacman(pacman):
    for segment in pacman:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
def draw_food(food, position):
    font = pygame.font.Font(None, 36)
    text = font.render(food, True, WHITE)
    screen.blit(text, (position[0] * GRID_SIZE + 5, position[1] * GRID_SIZE + 5))

def move_pacman(pacman, direction):
    head = pacman[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    if new_head in food_positions:
        food_index = food_positions.index(new_head)
        
        if food_index == len(foods) - 1: 
            #next_letter = chr(ord(foods[-1]) + 1)
            if isinstance(foods[-1], (int)): # si el elemento es un número, debemos agregar un operador
                next_item = random.choice(operadores)
                
            else:
                next_item = random.randint(1, 100)
                
            # Agrega lo comido
            foods_eaten.append(foods[-1])
            print("Foods Eaten:", foods_eaten)
            
            
            if len(foods_eaten) < 5:
                foods.append(next_item)
                food_positions.append(random_food_position(pacman, food_positions))
                
            else: # si se come 9 elementos, gana
                print("You Win!")
                print("This is your score!:: " + str(calcular_operacion(foods_eaten)))
                pygame.quit()
                sys.exit()
        else:
            foods.pop(food_index)
            food_positions.pop(food_index)
            None
    else:
        pacman.insert(0, new_head)
        pacman.pop()
    return False

def check_collision(pacman):
    head = pacman[0]
    if head in pacman[1:]:
        return True
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    return False


# Función para realizar una operación binaria
def realizar_operacion(operador, numeros):
    if operador == '+':
        return numeros[0] + numeros[1]
    elif operador == '-':
        return numeros[0] - numeros[1]
    elif operador == '*':
        return numeros[0] * numeros[1]
    elif operador == '/':
        return numeros[0] / numeros[1]
            
def calcular_operacion(food_eaten):
    lista_numeros = []
    lista_operadores = []

    for elemento in food_eaten:
        if isinstance(elemento, (int, float)): # si es un numero
            lista_numeros.append(elemento)
        else: # si es un operador
            lista_operadores.append(elemento)
            
        # Realizar cálculos cuando sea posible
        while len(lista_operadores) >= 1 and len(lista_numeros) >= 2:
            operador = lista_operadores.pop()
            operando2 = lista_numeros.pop()
            operando1 = lista_numeros.pop()
            total_score = realizar_operacion(operador, [operando1, operando2])
            lista_numeros.append(total_score)
            
    if len(lista_numeros) == 1 and len(lista_operadores) == 0:
        return lista_numeros[0]
            
    return total_score



# Game loop
running = True
while running:
    moving = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = UP
                moving = True
            elif event.key == pygame.K_DOWN:
                direction = DOWN
                moving = True
            elif event.key == pygame.K_LEFT:
                direction = LEFT
                moving = True
            elif event.key == pygame.K_RIGHT:
                direction = RIGHT
                moving = True

    # Mueve el pacman solo si la variable de movimiento está establecida en True
    if moving:
        food_eaten = move_pacman(pacman, direction)
        if check_collision(pacman):
            print("Fin del juego!")
            pygame.quit()
            sys.exit()
            

    screen.fill(BLACK)
    draw_pacman(pacman)
    for food, position in zip(foods, food_positions):
        draw_food(str(food), position)
    pygame.display.flip()
        
        
    clock.tick(10)
    
    print(foods_eaten)

pygame.quit()
sys.exit()
