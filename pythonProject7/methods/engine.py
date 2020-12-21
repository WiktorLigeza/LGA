import numba
from numba import jit, njit
from PIL import Image, ImageTk
import numpy as np
import random
import tkinter as tk

@jit(nopython=True, parallel=True)
def set_grid(img_matrix, state_matrix, threshold = 60):
    b = 0
    for x in numba.prange(0, state_matrix.shape[0]):
        for y in numba.prange(0, state_matrix.shape[1]):
            state = state_matrix[x, y]

            #set walls
            if y == 1 or x == 1 or y == state_matrix.shape[1]-2 or x == state_matrix.shape[0]-2:
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]

            if y == 2 or x == 2 or y == state_matrix.shape[1]-3 or x == state_matrix.shape[0]-3:
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]

            if y == 3 or x == 3 or y == state_matrix.shape[1]-4 or x == state_matrix.shape[0]-4:
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]

            if y == 75 and (0 < x < (((state_matrix.shape[0])/2)-25) or ((state_matrix.shape[0])/2)+25 < x < state_matrix.shape[0]):
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]

            if y == 76 and (0 < x < (((state_matrix.shape[0])/2)-25) or ((state_matrix.shape[0])/2)+25 < x < state_matrix.shape[0]):
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]

            if y == 77 and (0 < x < (((state_matrix.shape[0])/2)-25) or ((state_matrix.shape[0])/2)+25 < x < state_matrix.shape[0]):
                state[0] = 1
                state_matrix[x, y] = state
                img_matrix[x, y] = [255, 0, 255]





            random_gen_1 = random.randint(0, 200)
            if 0 < y < 74 and 0 < x < (state_matrix.shape[0]-1) and random_gen_1 > threshold:
                random_gen_2 = random.randint(1, 4)
                if random_gen_2 == 1:
                    state[1] = 1
                elif random_gen_2 == 2:
                    state[2] = 1
                elif random_gen_2 == 3:
                    state[3] = 1
                elif random_gen_2 == 4:
                    state[4] = 1
                state_matrix[x, y] = state
                b += 1
                img_matrix[x, y] = [0, 255, 255]
    return img_matrix, state_matrix, b


def set_sim(canvas, img_matrix, state_matrix, master, frame):
    new_state_matrix = np.zeros([state_matrix.shape[0], state_matrix.shape[1], 5], dtype=np.uint8)

    # create new matrix
    new_img_matrix = np.zeros([img_matrix.shape[0], img_matrix.shape[1], 3], dtype=np.uint8)

    new_state_matrix, new_img_matrix = state_update(state_matrix, new_state_matrix, img_matrix, new_img_matrix)

    img = ImageTk.PhotoImage(image=Image.fromarray(new_img_matrix))

    canvas.image = img

    canvas.create_image(2, 2, anchor="nw", image=img)

    master.after(10, lambda: set_sim(canvas, new_img_matrix, new_state_matrix, master, frame))


@jit(nopython=True, parallel=True)
def state_update(state_matrix, new_state_matrix, img_matrix, new_img_matrix):
    b = 0
    for x in numba.prange(0, state_matrix.shape[0]-1):
        for y in numba.prange(0, state_matrix.shape[1]-1):
            state = state_matrix[x, y]
            if state[0] == 1:
                new_state_matrix[x, y] = [1, 0, 0, 0, 0]
                new_img_matrix[x, y] = [255, 0, 255]

            #state not solid
            elif state[0] == 0:
                #[type, dx, dy,]
                new_state = [0, 0, 0, 0, 0]

                #neighbours
                state_up = state_matrix[x - 1, y]
                state_right = state_matrix[x, y + 1]
                state_down = state_matrix[x + 1, y]
                state_left = state_matrix[x, y - 1]

                #impact detection
                if state[1] == 1 and state_up[0] == 1:
                    new_state[1] = 0
                    new_state[3] = 1
                elif state[2] == 1 and state_right[0] == 1:
                    new_state[2] = 0
                    new_state[4] = 1
                elif state[3] == 1 and state_down[0] == 1:
                    new_state[3] = 0
                    new_state[1] = 1
                elif state[4] == 1 and state_left[0] == 1:
                    new_state[4] = 0
                    new_state[2] = 1

                #fly with the vector
                else:
                    if state_up[3] == 1:
                        new_state[3] = 1
                        state_up[3] = 0
                    if state_right[4] == 1:
                        new_state[4] = 1
                        state_right[4] = 0
                    if state_down[1] == 1:
                        new_state[1] = 1
                        state_down[1] = 0
                    if state_left[2] == 1:
                        new_state[2] = 1
                        state_left[2] = 0

                    if new_state[1] == 1 and new_state[3] == 1:
                        new_state[1] = 0
                        new_state[2] = 1
                        new_state[3] = 0
                        new_state[4] = 1
                    elif new_state[2] == 1 and new_state[4] == 1:
                        new_state[1] = 1
                        new_state[2] = 0
                        new_state[3] = 1
                        new_state[4] = 0

                new_state_matrix[x, y] = new_state

                if new_state[1] == 1 or  new_state[2] == 1 or new_state[3] == 1 or new_state[4] == 1:
                    new_img_matrix[x, y] = [0, 255, 255]

    return new_state_matrix, new_img_matrix