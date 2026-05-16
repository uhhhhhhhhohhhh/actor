
from tkinter import *
from winsound import *
from random import *

# Инициализация главного окна
window = Tk()
window.title("Игра")

# Глобальные переменные
actor_vx = 1
actor_vy = 1
animation_index = 0
end = False
speed = 5
score = 0
actor_size = 25
world_width = 400
world_height = 300
frame_time = 30
animation_frame_time = 600

# Переменные для меню
menu_active = True
menu_index = 0
menu_items = ['Начать игру', 'Сменить костюм', 'Выход']
menu_text_ids = []
selected_color = 'red'
normal_color = 'black'

# Переменные для подменю смены костюма
costume_menu_active = False
costume_menu_items = ['Костюм 1', 'Костюм 2']
costume_menu_index = 0
costume_menu_text_ids = []

# Переменные для костюмов
current_costume = 1  # 1 или 2
costumes = {
    1: [PhotoImage(file=f'anlo ({i}).png') for i in range(1, 11)],
    2: [PhotoImage(file=f'rocket ({i}).png') for i in range(1, 11)]
}

# Функция для обновления костюма
def update_costume():
    global actor_id, animation_index
    actor_id = costumes[current_costume][animation_index % 10]
    canvas.itemconfig(actor, image=actor_id)

# Функция для обработки кликов
def hit(event):
    global speed, score, end
    if collision_detection(mouse_x, mouse_y) and speed != 12 and not end:
        speed -= 1
        PlaySound(sound='punch_sound.wav', flags=SND_ASYNC)
        if 12 >= speed >= 7:
            score += 1
            canvas.itemconfig(score_text1, text=score)
        if speed <= 0:
            speed = 0
            end = True
            canvas.itemconfig(room, state='normal')
            canvas.itemconfig(win_text, state='normal')
            canvas.itemconfig(win_score_text, state='normal', text=f'Полученные очки: {score}')
            canvas.itemconfig(score_text, state='hidden')
            canvas.itemconfig(score_text1, state='hidden')
            canvas.itemconfig(text_ide, state='hidden')
    elif speed >= 12 or speed == 0:
        return
    else:
        PlaySound(sound='fail_punch.wav', flags=SND_ASYNC)

# Функция для отслеживания движения мыши
def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

# Функция для анимации
def animate():
    global animation_index
    if speed != 0 or speed <= 12:
        animation_index = (animation_index + 1) % 10
        update_costume()
        window.after(animation_frame_time, animate)

# Функция для проверки столкновений
def collision_detection(x, y):
    position = canvas.coords(actor)
    left = position[0] - actor_size
    top = position[1] - actor_size
    right = position[0] + actor_size
    bottom = position[1] + actor_size
    return left <= x <= right and top <= y <= bottom

# Функция для обработки нажатий клавиш
def handle_key(event):
    global menu_index, menu_active, costume_menu_active, costume_menu_index, current_costume

    if costume_menu_active:
        if event.keysym == 'Up':
            if costume_menu_index > 0:
                canvas.itemconfig(costume_menu_text_ids[costume_menu_index], fill=normal_color)
                costume_menu_index -= 1
                canvas.itemconfig(costume_menu_text_ids[costume_menu_index], fill=selected_color)
        elif event.keysym == 'Down':
            if costume_menu_index < len(costume_menu_items) - 1:
                canvas.itemconfig(costume_menu_text_ids[costume_menu_index], fill=normal_color)
                costume_menu_index += 1
                canvas.itemconfig(costume_menu_text_ids[costume_menu_index], fill=selected_color)
        elif event.keysym == 'Return':
            current_costume = costume_menu_index + 1
            for text_id in costume_menu_text_ids:
                canvas.itemconfig(text_id, state='hidden')
            costume_menu_active = False
            menu_active = True
            update_costume()
            for text_id in menu_text_ids:


                canvas.itemconfig(text_id, state='normal')
                canvas.itemconfig(menu_text_ids[menu_index], fill=selected_color)
        elif event.keysym == 'Escape':
            for text_id in costume_menu_text_ids:
                canvas.itemconfig(text_id, state='hidden')
            costume_menu_active = False
            menu_active = True
            for text_id in menu_text_ids:
                canvas.itemconfig(text_id, state='normal')
            canvas.itemconfig(menu_text_ids[menu_index], fill=selected_color)
    elif menu_active:
        if event.keysym == 'Up':
            if menu_index > 0:
                canvas.itemconfig(menu_text_ids[menu_index], fill=normal_color)
                menu_index -= 1
                canvas.itemconfig(menu_text_ids[menu_index], fill=selected_color)
        elif event.keysym == 'Down':
            if menu_index < len(menu_items) - 1:
                canvas.itemconfig(menu_text_ids[menu_index], fill=normal_color)
                menu_index += 1
                canvas.itemconfig(menu_text_ids[menu_index], fill=selected_color)
        elif event.keysym == 'Return':
            if menu_index == 0:
                menu_active = False
                for text_id in menu_text_ids:
                    canvas.itemconfig(text_id, state='hidden')
                start_game()
            elif menu_index == 1:
                menu_active = False
                for text_id in menu_text_ids:
                    canvas.itemconfig(text_id, state='hidden')
                costume_menu_active = True
                for text_id in costume_menu_text_ids:
                    canvas.itemconfig(text_id, state='normal')
                canvas.itemconfig(costume_menu_text_ids[costume_menu_index], fill=selected_color)
            elif menu_index == 2:
                exit()

# Функция для начала игры
def start_game():
    global speed, score, end
    speed = 5
    score = 0
    end = False
    canvas.itemconfig(room2, state='normal')
    canvas.itemconfig(actor, state='normal')
    canvas.itemconfig(text_ide, state='normal')
    canvas.itemconfig(score_text, state='normal')
    canvas.itemconfig(score_text1, state='normal')
    canvas.coords(actor, actor_size, actor_size)
    update()
    animate()

# Функция для обновления игрового состояния
def update():
    global speed
    if speed != 12 and not end:
        global actor_vx, actor_vy
        if speed >= 8:
            canvas.itemconfig(text_ide, text=speed, fill='red')
        else:
            canvas.itemconfig(text_ide, text=speed, fill='black')

        canvas.move(actor, actor_vx * speed, actor_vy * speed)
        coors = canvas.coords(actor)
        x_left = coors[0]
        y_top = coors[1]

        if x_left + actor_size > world_width:
            x_left = world_width - actor_size
            actor_vx = -actor_vx
            PlaySound(sound='rndsound.wav',flags=SND_ASYNC)
        elif x_left - actor_size < 0:
            x_left = actor_size
            actor_vx = -actor_vx
            PlaySound(sound='rndsound.wav', flags=SND_ASYNC)

        if y_top + actor_size > world_height:
            y_top = world_height - actor_size
            actor_vy = -actor_vy
            speed += 1
            PlaySound(sound='rndsound.wav', flags=SND_ASYNC)
        elif y_top - actor_size < 0:
            y_top = actor_size
            actor_vy = -actor_vy
            PlaySound(sound='rndsound.wav', flags=SND_ASYNC)

        canvas.coords(actor, x_left, y_top)
        window.after(frame_time, update)
    elif speed == 12:
        canvas.itemconfig(text_ide, text='Вы проиграли', fill='red')
        canvas.itemconfig(room1, state='normal')
        return

# Создание Canvas
canvas = Canvas(window, width=world_width, height=world_height, bg='white')

# Создание игровых объектов (изначально скрыты)
room_id2 = PhotoImage(file='space.png')
room2 = canvas.create_image(200, 150, image=room_id2, state='hidden')

actor_id = PhotoImage(file='anlo (1).png')
actor = canvas.create_image(actor_size, actor_size, image=actor_id, state='hidden')

room_id = PhotoImage(file='happy_end.png')
room = canvas.create_image(200, 150, image=room_id, state='hidden')

room_id1 = PhotoImage(file='sad.png')
room1 = canvas.create_image(200, 150, image=room_id1, state='hidden')


text_ide = canvas.create_text(200, 150, text=speed, font='Times 20 bold', fill='black', state='hidden')
win_text = canvas.create_text(200, 150, text='Вы выиграли', font='Times 20 bold', fill='red', state='hidden')
win_score_text = canvas.create_text(200, 100, text=f'Полученные очки: {score}', state='hidden')
score_text = canvas.create_text(200, 50, text='Очки:', fill='black', state='hidden')
score_text1 = canvas.create_text(200, 100, text=score, fill='black', state='hidden')

# Создание элементов главного меню
for i in range(len(menu_items)):
    item = menu_items[i]
    text_id = canvas.create_text(world_width / 2, 100 + i * 50, text=item,
                               font='Times 20', fill=normal_color)
    menu_text_ids.append(text_id)
canvas.itemconfig(menu_text_ids[0], fill=selected_color)

# Создание элементов подменю смены костюма
for i in range(len(costume_menu_items)):
    item = costume_menu_items[i]
    text_id = canvas.create_text(world_width / 2, 100 + i * 50, text=item,
                               font='Times 20', fill=normal_color, state='hidden')
    costume_menu_text_ids.append(text_id)
canvas.itemconfig(costume_menu_text_ids[0], fill=selected_color)

# Привязка событий
window.bind('<KeyPress>', handle_key)
canvas.bind('<ButtonPress>', hit)
canvas.bind('<Motion>', mouse_motion)
canvas.pack()

# Запуск главного цикла
window.mainloop()