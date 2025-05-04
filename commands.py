import random
from tkinter import *
import textwrap as tw
from requests_oauthlib import *
import os
import time


def clean(file_name):
    open(file_name, 'w').close()


def end_window():
    w = Tk()
    w.title('')
    w.geometry('400x140')
    w.resizable(False, False)
    w.configure(bg='DodgerBlue4')
    w.attributes('-topmost', True)

    head_lab = Label(w, text='!!!ФИНИШ!!!', font=('Comic Sans MS', 54), fg='white', bg='DodgerBlue4')

    head_lab.place(relx=0.5, rely=0.5, anchor=CENTER)

    w.mainloop()


def upload_file(writings, file_name):
    client_id = "f2bc5aa04a184895b0712ce8b7d622fa"
    client_secret = "bd146cb950f6444bbcedbcf28bfe9c91"
    auth_url = "https://oauth.yandex.ru/authorize"
    token_url = "https://oauth.yandex.ru/token"

    oauth = OAuth2Session(client_id=client_id)
    authorization_url, state = oauth.authorization_url(auth_url, force_confirm="true")

    print("Перейдите по ссылке, авторизуйтесь и скопируйте код:", authorization_url)
    code = input("Вставьте одноразовый код: ")

    token = oauth.fetch_token(token_url=token_url,
                              code=code,
                              client_secret=client_secret)
    access_token = token["access_token"]

    headers = {"Authorization": f"OAuth {access_token}"}
    file_path = file_name

    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload?path=%s' % os.path.basename(file_path)

    r = requests.get(upload_url, headers=headers)
    r_json = r.json()
    for st in writings:
        write(st, file_name)
    f = open(f"{file_name}", "rb")
    response = requests.put(r_json['href'], files={'file': f})
    os.remove(file_name)
    print(response)


def openfile_window():
    ans = []

    def end(filename, name):
        nonlocal ans
        ans = [filename, name]

    w = Tk()
    w.title('Выбор файла')
    w.geometry('750x350')
    w.resizable(False, False)
    w.configure(bg='DodgerBlue4')

    head_lab = Label(w, text='ТЕСТ', font=('Comic Sans MS', 24), fg='white', bg='DodgerBlue4')
    filename_lab = Label(w, text='Название файла:', font=('Comic Sans MS', 16), fg='white', bg='DodgerBlue4')
    name_lab = Label(w, text='Имя ученика:', font=('Comic Sans MS', 16), fg='white', bg='DodgerBlue4')
    filename_ent = Entry(w, width=30)
    name_ent = Entry(w, width=30)
    warning_text = tw.fill('После нажатия кнопки "Начать" начнется тестирование на время', 45)
    warning_lab = Label(w, text=warning_text, font=('Comic Sans MS', 20), fg='white', bg='DodgerBlue4')
    start_but = Button(w, text='Начать', command=lambda: (end(filename_ent.get(), name_ent.get()), w.destroy()))

    head_lab.place(relx=0.5, y=30, anchor=CENTER)
    filename_ent.place(relx=0.6, y=100, anchor=CENTER)
    name_ent.place(relx=0.6, y=140, anchor=CENTER)
    filename_lab.place(relx=0.35, y=98, anchor=CENTER)
    name_lab.place(relx=0.37, y=138, anchor=CENTER)
    warning_lab.place(relx=0.5, y=240, anchor=CENTER)
    start_but.place(relx=0.5, y=300)

    w.mainloop()
    return ans


def download_window():
    ans = []

    def end(filename):
        nonlocal ans
        ans = filename

    w = Tk()
    w.title('Окно скачивания')
    w.geometry('400x140')
    w.resizable(False, False)
    w.configure(bg='DodgerBlue4')
    w.attributes('-topmost', True)

    head_lab = Label(w, text='Название файла для скачивания', font=('Comic Sans MS', 16), fg='white', bg='DodgerBlue4')
    filename_ent = Entry(w, width=30)
    download_but = Button(w, text='Скачать', command=lambda: (end(filename=filename_ent.get()), w.destroy()))

    head_lab.place(relx=0.5, y=30, anchor=CENTER)
    filename_ent.place(relx=0.5, y=70, anchor=CENTER)
    download_but.place(relx=0.5, y=110, anchor=CENTER)

    w.mainloop()
    return ans


def write(answer, file_name):
    f = open(file_name, 'a', encoding='utf-8')
    f.write(f'{answer}\n')
    f.close()


def time_list(t, n):
    d = int(t / n - 300)
    s = [0] * n
    for i in range(n):
        task_time = random.randint(i * (d + 300), d + i * (d + 300))
        s[i] = task_time
    return s


def task_window(inf, i, start_time):
    ans = ''

    def end(ans_t):
        nonlocal ans
        ans = f'Ответ на задание №{i}: {ans_t}'

    w = Tk()
    w.geometry('750x350')
    w.resizable(False, False)
    w.configure(bg='DodgerBlue4')
    w.attributes('-topmost', True)
    current_time = time.time()
    task_text = tw.fill(inf[f'{i}_text'], 45)   # 315 символов в тексте задания максимум
    task_time = f"{(int(inf[f'{i}_time'] * 60) - round(current_time - start_time)) // 60:02d}:{(int(inf[f'{i}_time'] * 60) - round(current_time - start_time)) % 60:02d}"
    task_numer = Label(w, text=f"Задание №{i}", font=('Comic Sans MS', 24), fg='white', bg='DodgerBlue4')
    task_text_lab = Label(w, text=f"{task_text}", font=('Comic Sans MS', 16), fg='white', bg='DodgerBlue4')
    task_time_lab = Label(w, text=f"{task_time}", font=('Comic Sans MS', 16), fg='white', bg='DodgerBlue4')
    answer_lab = Label(w, text=f"Ответ:", font=('Comic Sans MS', 18), fg='white', bg='DodgerBlue4')
    answer = Entry(w)
    answer_but = Button(w, text="Дать ответ", command=lambda: (end(answer.get()),
                                                               w.destroy()), width=20)
    task_numer.place(relx=0.5, y=30, anchor=CENTER)
    task_text_lab.place(relx=0.5, y=160, anchor=CENTER)
    task_time_lab.place(relx=0.9, y=30, anchor=CENTER)
    answer.place(relx=0.5, y=310, anchor=CENTER)
    answer_lab.place(relx=0.35, y=308, anchor=CENTER)
    answer_but.place(relx=0.7, y=310, anchor=CENTER)

    def update():
        current_time = time.time()
        task_time = f"{(int(inf[f'{i}_time'] * 60) - round(current_time - start_time)) // 60:02d}:{(int(inf[f'{i}_time'] * 60) - round(current_time - start_time)) % 60:02d}"
        if int(inf[f'{i}_time'] * 60) - round(current_time - start_time) < 0:
            task_time = '00:00'
        task_time_lab.config(text=task_time)
        w.after(1000, update)

    update()

    w.mainloop()
    return ans


def shifr(s, d, m, y):
    sn = ''
    for i in range(len(s)):
        sn = sn + chr(ord(s[i]) + (d * (i % 3) + m * ((i + 1) % 3) + y * ((i + 2) % 3)) % 100)
    return sn


def deshifr(s, d, m, y):
    sn = ''
    for i in range(len(s)):
        sn = sn + chr(ord(s[i]) - (d * (i % 3) + m * ((i + 1) % 3) + y * ((i + 2) % 3)) % 100)
    return sn


def parse_in(file_name):
    f = open(f'{file_name}', encoding='utf-8')
    s = f.readline()[12:-1]
    inf = dict()

    d, m, y = s.split('.')
    inf['d'] = int(d)
    inf['m'] = int(m)
    inf['y'] = int(y)

    n = f.readline()[17:-1]
    inf['n'] = int(n)

    t = f.readline()[17:-1]
    inf['t'] = int(t) * 60

    s = f.readline()
    while s[0] != '0':
        i = int(s[13:-1])
        i_text = f.readline()[11:-1]
        i_time = f.readline()[11:-1]
        inf[f'{i}_text'] = deshifr(i_text, inf['d'], inf['m'], inf['y'])
        inf[f'{i}_time'] = float(i_time)
        s = f.readline()
    return inf

