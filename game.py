import pygame
import json

# Pre-load the constants and the assets
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LENGTH = 80
TOP_LEFT = (160, 60)
BOTTOM_RIGHT = (640, 540)
TOTAL_LEVELS = 3
BACKGROUND, BACKGROUND_2 = pygame.image.load("assets/bg.png"), pygame.image.load("assets/bg2.png")
LOGO = pygame.image.load("assets/logo.png")
GREEN_TICK = pygame.image.load("assets/greentick.png")
ABSTRACT_BG = pygame.image.load("assets/abstract.png")
BUTTONS = [pygame.image.load("assets/button%d.png" % k) for k in range(1, 8)]
BLOCKS = [pygame.image.load("assets/block%d.png" % k) for k in range(1, 8)]
MAIN_BLOCK = pygame.image.load("assets/main.png")
LEVEL_DATA = json.load(open("levels.json", "r"))


def get_blocks(level):
    level = str(level)
    vertical = [[], []]
    # Get relative positions of blocks of sizes 1x2 and 1x3
    for x in LEVEL_DATA[level]["1x2"]:
        vertical[0] += [[int(k) for k in x.split(",")]]
    for x in LEVEL_DATA[level]["1x3"]:
        vertical[1] += [[int(k) for k in x.split(",")]]

    horizontal = [[], []]
    # Get relative positions of blocks of sizes 2x1 and 3x1
    for x in LEVEL_DATA[level]["2x1"]:
        horizontal[0] += [[int(k) for k in x.split(",")]]
    for x in LEVEL_DATA[level]["3x1"]:
        horizontal[1] += [[int(k) for k in x.split(",")]]

    main_block = [int(k) for k in LEVEL_DATA[level]["main"].split(",")]  # Get relative position of the main block

    # Now create a Rect object for each block with their proper positions
    vertical_blocks = []
    horizontal_blocks = []
    for i in range(len(vertical)):
        size = i+2
        for x, y in vertical[i]:
            block = pygame.Rect(TOP_LEFT[0]+LENGTH*(y-1),
                                TOP_LEFT[1]+LENGTH*(x-1),
                                LENGTH, LENGTH*size)
            vertical_blocks.append(block)

        for x, y in horizontal[i]:
            block = pygame.Rect(TOP_LEFT[0] + LENGTH * (y - 1),
                                TOP_LEFT[1] + LENGTH * (x - 1),
                                LENGTH*size, LENGTH)
            horizontal_blocks.append(block)

    main_block = pygame.Rect(TOP_LEFT[0] + LENGTH * (main_block[1] - 1),
                             TOP_LEFT[1] + LENGTH * (main_block[0] - 1),
                             LENGTH*2, LENGTH)

    return horizontal_blocks, vertical_blocks, main_block


def get_current_level():
    # Gets the current level of the user
    with open("levels.json", "r") as f:
        data = json.load(f)
        f.close()
    for i in range(1, TOTAL_LEVELS+1):
        if data[str(i)]["completed"] == 0:
            return i
    return TOTAL_LEVELS


def check_if_completed(level):
    # Checks if user has already completed the particular level
    with open("levels.json", "r") as f:
        data = json.load(f)
        f.close()
    return data[str(level)]["completed"] == 1


def update_data(level):
    # Updates the data file when user completes the level
    with open("levels.json", "r+") as f:
        data = json.load(f)
        data[str(level)]["completed"] = 1
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()


def collides(blocks, original, top, left, main_block):
    # Function to check if a block overlaps with another block or not
    for group in blocks:
        for block in group:
            if block == original:
                continue
            if block.colliderect(pygame.Rect(left, top, original.width, original.height)):
                return True
    if original == main_block:
        return False

    return main_block.colliderect(pygame.Rect(left, top, original.width, original.height))


def main():
    """ Main Menu """
    pygame.init()
    done = False
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    buttons = [pygame.Rect(350, 380, 64, 64),
               pygame.Rect(600, 380, 64, 64),
               pygame.Rect(100, 380, 64, 64)]
    font = pygame.font.SysFont("Verdana", 16, bold=True)
    help_text = font.render('Move the blocks so that the red block can move left to right without any obstruction.',
                            False, (255, 255, 255))
    help_text2 = font.render('Some blocks can only move horizontally, while others only move vertically.',
                             False, (255, 255, 255))
    help_text3 = font.render('To move any block, place your mouse over it and drag it to where you want it to go.',
                             False, (255, 255, 255))
    help_text4 = font.render('Created by manish',
                             False, (255, 255, 255))

    show_help = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons[0].collidepoint(event.pos[0], event.pos[1]):
                        # When play button is clicked
                        done = True
                        game()
                    if buttons[1].collidepoint(event.pos[0], event.pos[1]):
                        # When quit button is clicked
                        done = True
                    if buttons[2].collidepoint(event.pos[0], event.pos[1]):
                        # When help button is clicked
                        show_help = not show_help

        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(ABSTRACT_BG, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        screen.blit(MAIN_BLOCK, (60, 20))
        screen.blit(BLOCKS[0], (60, 84))
        screen.blit(BLOCKS[3], (60, 148))
        screen.blit(BLOCKS[2], (124, 148))
        screen.blit(BLOCKS[5], (188, 148))
        screen.blit(BLOCKS[6], (188, 84))
        screen.blit(BLOCKS[1], (188, 20))
        screen.blit(BLOCKS[2], (292, 20))
        screen.blit(BLOCKS[3], (292, 84))
        screen.blit(BLOCKS[0], (292, 148))
        screen.blit(BLOCKS[6], (356, 20))
        screen.blit(BLOCKS[4], (420, 20))
        screen.blit(BLOCKS[5], (420, 84))
        screen.blit(BLOCKS[6], (420, 148))
        screen.blit(LOGO, (524, 20))

        if show_help:
            screen.blit(help_text, (30, 240))
            screen.blit(help_text2, (30, 270))
            screen.blit(help_text3, (30, 300))
            screen.blit(help_text4, (300, 500))

        for i in range(3):
            screen.blit(pygame.transform.scale(BUTTONS[i], (64, 64)), buttons[i])

        pygame.display.flip()
        clock.tick(60)


def game(current_level=None):
    """ Main Program """
    pygame.init()
    pygame.font.init()

    done = False
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    if not current_level:
        current_level = get_current_level()
    font = pygame.font.SysFont("Tahoma", 32, bold=True)
    level_text = font.render('Level %d' % current_level, False, (255, 255, 255))
    level_loaded = False
    level_completed = check_if_completed(current_level)
    main_block = None
    left_button, right_button = None, None
    menu_button = pygame.Rect(20, 550, 44, 44)
    restart_button = pygame.Rect(700, 550, 44, 44)
    blocks = []

    vertical_drag, horizontal_drag = False, False

    while not done:
        # Game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # When the left mouse button is pressed
                    for i in range(len(blocks[0])):
                        # Check if a horizontally draggable block is clicked
                        if blocks[0][i].collidepoint(event.pos[0], event.pos[1]):
                            # Get the block that is being dragged
                            horizontal_drag = i+1

                    for i in range(len(blocks[1])):
                        # Check if a vertically draggable block is clicked
                        if blocks[1][i].collidepoint(event.pos[0], event.pos[1]):
                            # Get the block that is being dragged
                            vertical_drag = i+1

                    if main_block.collidepoint(event.pos[0], event.pos[1]):
                        # Check if main block is clicked
                        horizontal_drag = -1

                    if menu_button.collidepoint(event.pos[0], event.pos[1]):
                        # Menu button is clicked, go back to main menu
                        done = True
                        main()

                    level_change = False

                    if restart_button.collidepoint(event.pos[0], event.pos[1]):
                        # Restart button is clicked, reload level
                        level_change = True

                    # Check if right button or left button is pressed - if yes, go to next/previous level
                    if right_button and right_button.collidepoint(event.pos[0], event.pos[1]):
                        level_change = True
                        current_level += 1
                    if left_button and left_button.collidepoint(event.pos[0], event.pos[1]):
                        level_change = True
                        current_level -= 1

                    if level_change:
                        # Reset variables for the new level
                        level_loaded = False
                        level_completed = check_if_completed(current_level)
                        right_button = None
                        left_button = None
                        blocks = []
                        level_text = font.render('Level %d' % current_level, False, (255, 255, 255))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    # If blocks are no longer being dragged
                    vertical_drag = False
                    horizontal_drag = False

            elif event.type == pygame.MOUSEMOTION:
                if horizontal_drag:
                    # when the block is being dragged horizontally
                    mouse_x, mouse_y = event.pos
                    original = blocks[0][horizontal_drag - 1] if horizontal_drag != -1 else main_block
                    width = original.width
                    new_left = min(BOTTOM_RIGHT[0]-width, max(mouse_x, TOP_LEFT[0]))
                    if new_left >= original.left:
                        # if block is being moved left
                        for left in range(original.left, new_left+1):
                            if collides(blocks, original, original.top, left, main_block):
                                break
                            else:
                                new_left = left
                    else:
                        # if block is being moved right
                        for left in range(original.left, new_left-1, -1):
                            if collides(blocks, original, original.top, left, main_block):
                                break
                            else:
                                new_left = left

                    if horizontal_drag != -1:
                        blocks[0][horizontal_drag - 1].x = new_left  # position of block after being moved left/right
                    else:
                        # main block is being dragged
                        main_block.x = new_left
                        if main_block.x >= TOP_LEFT[0] + LENGTH*4:
                            if not level_completed:
                                level_completed = True
                                update_data(current_level)

                elif vertical_drag:
                    # when the block is being dragged vertically
                    mouse_x, mouse_y = event.pos
                    original = blocks[1][vertical_drag-1]
                    height = original.height
                    new_top = min(BOTTOM_RIGHT[1] - height, max(mouse_y, TOP_LEFT[1]))
                    if new_top > original.top:
                        # if block is being moved down
                        for top in range(original.top, new_top+1):
                            if collides(blocks, original, top, original.left, main_block):
                                break
                            else:
                                new_top = top
                    else:
                        # if block is being moved up
                        for top in range(original.top, new_top-1, -1):
                            if collides(blocks, original, top, original.left, main_block):
                                break
                            else:
                                new_top = top
                    blocks[1][vertical_drag - 1].y = new_top  # position of the block after being moved up/down

        screen.fill((0, 0, 0))
        screen.blit(BACKGROUND if not level_completed else BACKGROUND_2, (0, 0))
        screen.blit(level_text, (364, 10))

        if not level_loaded:
            # Get the positions of the blocks in the current level
            horizontal_blocks, vertical_blocks, main_block = get_blocks(current_level)
            blocks.append(horizontal_blocks)
            blocks.append(vertical_blocks)
            level_loaded = True

        count = 0
        for group in blocks:
            for block in group:
                # Display each block with a particular color
                screen.blit(pygame.transform.scale(BLOCKS[count % 7], (block.width, block.height)), block)
                count += 1

        screen.blit(pygame.transform.scale(MAIN_BLOCK, (2*LENGTH, LENGTH)), main_block)  # Display the main block

        if level_completed:
            screen.blit(pygame.transform.scale(GREEN_TICK, (48, 48)), (310, 6))
            if current_level != TOTAL_LEVELS:
                if not right_button:
                    right_button = pygame.Rect(600, 10, 44, 44)
                screen.blit(pygame.transform.scale(BUTTONS[4], (44, 44)), right_button)

        if current_level != 1:
            if not left_button:
                left_button = pygame.Rect(150, 10, 44, 44)
            screen.blit(pygame.transform.scale(BUTTONS[3], (44, 44)), left_button)

        screen.blit(pygame.transform.scale(BUTTONS[5], (44, 44)), menu_button)
        screen.blit(pygame.transform.scale(BUTTONS[6], (44, 44)), restart_button)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()