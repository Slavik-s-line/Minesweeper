import tkinter, tkinter.ttk, random, os, tkinter.messagebox, tkinter.simpledialog, tkinter.font as font
from operator import add, sub
import urllib

root = tkinter.Tk()
root.resizable(width=False, height=False)
root.title("Сапер")

# Инициализация глобальных переменных
rows = 9
columns = 9
mines = 10
field = []
buttons = []
isGameOver = False
# Цвета, которые будут назначаться клеткам в соответствии с их значениями
colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
# Шрифт
myFont = font.Font(family='Arial', weight="bold")
# Путь к директории, в которой хранятся сохранения игрока
saveDir = os.path.dirname(os.path.abspath(__file__)) + r'\Saves\\'
if not os.path.exists(saveDir): os.makedirs(saveDir)

root.protocol("WM_DELETE_WINDOW", lambda: saveAndQuit())
# Назначение функции сохранения поля для кнопки закрытия окна

#-------------------------------------------------------------------------
def saveAndQuit():
    if not isGameOver:
        File.saveGameField(File)
    root.destroy()

#-------------------------------------------------------------------------
def createMenu():
    """Эта функция создаёт выпадающие списки меню"""

    menuField = tkinter.Menu(root, tearoff=0)
    menuField.add_command(label="Новачок", command=lambda: setSize(9, 9, 10))
    menuField.add_command(label="Любитель", command=lambda: setSize(16, 16, 40))
    menuField.add_command(label="Професіонал", command=lambda: setSize(16, 30, 99))

    menuBar = tkinter.Menu(root)
    menuBar.add_cascade(label="Рівні складності", menu=menuField)
    menuBar.add_command(label="Рейтинг гравців", command=lambda: showRating())
    menuBar.add_command(label="Закрити гру", command=lambda: saveAndQuit())
    root.config(menu=menuBar)


#-------------------------------------------------------------------------
def composeRating(lineNumber):
    """Эта функция делает список из всех рейтингов всех игроков,
    чтобы затем составить общий рейтинг"""

    textFiles = [f for f in os.listdir(saveDir) if f.endswith('_save.txt')]
    ratingArr = []
    for file in textFiles:
        with open(saveDir + str(file), "r") as playerSave:
            playerSave.seek(0)
            lines = playerSave.readlines()
            try: ratingArr.append(lines[lineNumber].replace('[', '').replace(']', '').replace('\n', '').split(' '))
            except IndexError: pass
    return ratingArr

#-------------------------------------------------------------------------
def showRating():
    """Эта функция вызывает новое окно, в котором показывается рейтинг
    игроков на каждом уровне сложности"""

    ratingWindow = tkinter.Toplevel(root)
    ratingWindow.resizable(width=False, height=False)
    ratingWindow.title("Рейтинг гравців")
    tabs = tkinter.ttk.Notebook(ratingWindow)
    beginner = tkinter.ttk.Frame(tabs)
    intermediate = tkinter.ttk.Frame(tabs)
    expert = tkinter.ttk.Frame(tabs)
    tabs.add(beginner, text="Новачок")
    tabs.add(intermediate, text="Любитель")
    tabs.add(expert, text="Професіонал")

    tkinter.Label(beginner, text=recordRating(composeRating(2), beginner, 5)).grid(column=2, row=0)
    tkinter.Label(intermediate, text=recordRating(composeRating(3), intermediate, 6)).grid(column=2, row=0)
    tkinter.Label(expert, text=recordRating(composeRating(4), expert, 7)).grid(column=2, row=0)
    tabs.pack(expand=1, fill="both")

#-------------------------------------------------------------------------
def recordRating(resultsArr, tab, lastResLineNumber):
    """Эта функция создаёт в меню общего рейтинга н-ное количество
    строчек, которые имеют вид "Имя игрока -- рейтинг %"
    Имя игрока представлено кнопкой, рейтинг - надписью.
    Эта функция вызываетс функцию calculateRating, чтобы
    заново пересчитать рейтинг игрока, на случай изменений в нём"""

    namesArr = []
    lastResArr = []
    rating = []

    textFiles = [f for f in os.listdir(saveDir) if f.endswith('_save.txt')]
    for file in textFiles:
        with open(saveDir + str(file), "r") as playerSave:
            playerSave.seek(0)
            lines = playerSave.readlines()
            name = lines[0].replace("Имя: ", '').replace("\n", '')
            try: lastResArr.append(float(lines[lastResLineNumber].replace("\n", '')))
            except IndexError: lastResArr.append(0.0)
            namesArr.append(name)

    for i, result in enumerate(resultsArr):
        resultPercentage = File.calculateRating(File, result, lastResArr[i])
        rating.append(namesArr[i] + " : " + str(resultPercentage) + "%")
    for n, row in enumerate(rating):
        tkinter.Button(tab, text=row.split(':', 1)[0], command=lambda row=row:specifyRating(row)).grid(column=0, row=n, ipadx=30, sticky="ew")
        tkinter.Label(tab, text=row.split(':', 1)[1]).grid(column=1, row=n, sticky='ew')

#-------------------------------------------------------------------------
def specifyRating(name):
    """Эта функция выводит рейтинг конкретно взятого игрока
    Она созадёт дочернее окно и выводит на нём результаты игрока
    на всех уровнях сложности"""

    userName = name.split(' :', 1)[0]
    userRating = tkinter.Toplevel(root)
    userRating.resizable(width=False, height=False)
    userRating.title(userName)

    with open((saveDir + userName + "_save.txt"), "r+") as playerSave:
        lines = playerSave.readlines()
        try: bLastResult = lines[5].replace('\n', '')
        except IndexError: bLastResult = 0.0
        try: iLastResult = lines[6].replace('\n', '')
        except IndexError: iLastResult = 0.0
        try: eLastResult = lines[7].replace('\n', '')
        except IndexError: eLastResult = 0.0
    try:
        bResults = lines[2].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        bResults = []
    try:
        iResults = lines[3].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        iResults = []
    try:
        eResults = lines[4].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
    except IndexError:
        eResults = []

    tkinter.Label(userRating, text='Результати гравця ' + userName + ': ').grid(column=0, row=0, ipadx=50)
    tkinter.Label(userRating, text='Новачок: ' + str(File.calculateRating(File, bResults, float(bLastResult)))+'%').grid(column=0, row=1, ipadx=50)
    tkinter.Label(userRating, text='Любитель: ' + str(File.calculateRating(File, iResults, float(iLastResult)))+'%').grid(column=0, row=2, ipadx=50)
    tkinter.Label(userRating, text='Професіонал: ' + str(File.calculateRating(File, eResults, float(eLastResult)))+'%').grid(column=0, row=3, ipadx=50)

#-------------------------------------------------------------------------
def setSize(r, c, m):
    """Эта функция перезагружает поле с новыми размерами, которые игрок выбирает в меню"""

    global rows, columns, mines
    rows = r
    columns = c
    mines = m
    restartGame()

#-------------------------------------------------------------------------
def prepareGame():
    """Эта функция создаёт поле, заполняет его клетками и генерирует случайное
    положение мин на нём. Соответственно количеству мин вокруг клетки, ей даётся
    числовое значение"""

    global rows, columns, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, columns):
            # Добавление на поле клеток с изначальным значением 0
            field[x].append(0)
    # Генерация местоположения мин
    for _ in range(0, mines):
        x = random.randint(0, rows - 1)
        y = random.randint(0, columns - 1)
        # Предотвращение случая, при котором мина может появиться на клетке, занятой другой миной
        while field[x][y] == 9:
            x = random.randint(0, rows - 1)
            y = random.randint(0, columns - 1)
        field[x][y] = 9
        # Определение значения клетки в зависимости от присутствия мин на соседних ей клетках
        valueGeneration(x, y, add)

#-------------------------------------------------------------------------
def valueGeneration(x, y, op):
    """Эта функция занимается расстановкой значений клетки
    в зависимости от того, расположены ли мины
    на соседних ей клетках"""

    if x != 0:
        if y != 0:
            if field[x - 1][y - 1] != 9:
                field[x - 1][y - 1] = op(int(field[x - 1][y - 1]), 1)
        if field[x - 1][y] != 9:
            field[x - 1][y] = op(int(field[x - 1][y]), 1)
        if y != columns - 1:
            if field[x - 1][y + 1] != 9:
                field[x - 1][y + 1] = op(int(field[x - 1][y + 1]), 1)
    if y != 0:
        if field[x][y - 1] != 9:
            field[x][y - 1] = op(int(field[x][y - 1]), 1)
    if y != columns - 1:
        if field[x][y + 1] != 9:
            field[x][y + 1] = op(int(field[x][y + 1]), 1)
    if x != rows - 1:
        if y != 0:
            if field[x + 1][y - 1] != 9:
                field[x + 1][y - 1] = op(int(field[x + 1][y - 1]), 1)
        if field[x + 1][y] != 9:
            field[x + 1][y] = op(int(field[x + 1][y]), 1)
        if y != columns - 1:
            if field[x + 1][y + 1] != 9:
                field[x + 1][y + 1] = op(int(field[x + 1][y + 1]), 1)

#-------------------------------------------------------------------------
def prepareWindow():
    """Эта функция заполняет поле активными кнопками, которые
    дают игроку взаимодейстовать с клетками"""

    global rows, columns, buttons
    buttons = []
    firstClickHappened = False
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, columns):
            b = tkinter.Button(root, text=" ", bg="green", pady=0, padx=0, width=2, font=myFont, command=lambda x=x, y=y: Cell.clickOn(Cell, x, y)) #clickOn(x, y)
            b.bind("<Button-3>", lambda e, x=x, y=y: Cell.onRightClick(Cell, x, y))
            b.grid(row=x + 1, column=y, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
            buttons[x].append(b)



#-------------------------------------------------------------------------
def restartGame():
    """Эта функция уничтожает текущее поле
    и запускает игру заново"""

    global isGameOver
    isGameOver = False
    for x in root.winfo_children():
        if type(x) != tkinter.Menu and x != Player.p:
            x.destroy()
    Player.p.config(text=Player.faces[0])
    Player.p.grid(row=0, column=0, columnspan=columns, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
    Cell.firstClickHappened = False
    prepareWindow()
    prepareGame()

#-------------------------------------------------------------------------
def checkWin():
    """Эта функция проверяет, обошёл ли игрок все мины,
    и если это так - удаляет файлы конфигурации поля и
    сообщает игроку о победе"""

    global buttons, field, rows, columns, isGameOver
    win = True
    for x in range(0, rows):
        for y in range(0, columns):
            if field[x][y] != 9 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        File.saveResults(File, True)
        isGameOver = True
        os.remove(saveDir + File.playerName + "_game.bin")
        os.remove(saveDir + File.playerName + "_cells.bin")
        Player.p.config(text=Player.faces[2])
        tkinter.messagebox.showinfo("Вітаю!", "Ви виграли!!")


# КЛАССЫ:

class File:
    playerName = ''     # Имя игрока
    playerPass = ''     # Пароль
    resultCount = 0     # Счётчик игр
    bResults = []       # Массив, где хранятся 10 последних результатов игр на уровне "Новичок"
    iResults = []       # Массив, где хранятся 10 последних результатов игр на уровне "Любитель"
    eResults = []       # Массив, где хранятся 10 последних результатов игр на уровне "Эксперт"
    bLastRating = 0     # Рейтинг, составленный на основе 10 последних игр "Новичок"
    iLastRating = 0     # Рейтинг, составленный на основе 10 последних игр "Любитель"
    eLastRating = 0     # Рейтинг, составленный на основе 10 последних игр "Эксперт"
    mode = 'Новачок'    # Текущий уровень сложности
    authWindow = tkinter.Toplevel(root, pady=20, padx=20)

#-------------------------------------------------------------------------
    def deterMode(self):
        """Эта функция переопределяет уровень сложности"""

        if mines == 99: self.mode = 'Професіонал'
        elif mines == 40: self.mode = 'Любитель'
        else: self.mode = 'Новачок'
        return self.mode

#-------------------------------------------------------------------------
    def playerAuth(self):
        """Эта функция занимается регистрацией и входом"""

        authWindow = self.authWindow
        authWindow.grab_set()
        authWindow.lift(root)
        authWindow.resizable(width=False, height=False)
        authWindow.title("Авторизация")
        authWindow["bg"] = "blue"
        authWindow.protocol("WM_DELETE_WINDOW", lambda: "pass")

        tkinter.Label(authWindow, bg="red", text="Ім'я: ").pack()
        playerName = tkinter.Entry(authWindow)
        playerName.pack()
        tkinter.Label(authWindow, bg="red", text="Пароль: ").pack()
        playerPass = tkinter.Entry(authWindow)
        playerPass.pack()
        a = tkinter.Button(authWindow, text="Грати", bg='green', command=lambda: File.closeAuth(self, playerName, playerPass))

        a.pack(side="left", pady=10, padx=60)


#-------------------------------------------------------------------------
    def closeAuth(self, playerName, playerPass):
        """Эта функция проверяет, существует ли файл сохранения с именем игрока
        Если такого файла нет - функция создаёт его
        Если файл есть - сверяет введённый пароль с паролем в файле, и если они
        совпадают - игрок может продолжить свою последнюю игру"""

        name = str(playerName.get())
        passw = str(playerPass.get())
        self.playerPass = passw
        self.playerName = name

        if os.path.exists(saveDir + name + "_save.txt"):
            with open((saveDir + name + "_save.txt"), "r+") as playerSave:
                playerSave.seek(0)
                lines = playerSave.readlines()
                try:
                    self.bResults = lines[2].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.bResults = []
                try:
                    self.iResults = lines[3].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.iResults = []
                try:
                    self.eResults = lines[4].replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace('\n', '').split(' ')
                except IndexError:
                    self.eResults = []

                try: self.bLastRating = lines[5].replace('\n', '')
                except IndexError: self.bLastRating = 0.0
                try: self.iLastRating = lines[6].replace('\n', '')
                except IndexError: self.iLastRating = 0.0
                try:self.eLastRating = lines[7].replace('\n', '')
                except IndexError: self.eLastRating = 0.0
        else:
            self.bResults = []
            self.iResults = []
            self.eResults = []

        if os.path.exists(saveDir + name + "_save.txt"):
            with open((saveDir + name + "_save.txt"), "r+") as playerSave:
                content = playerSave.readlines()
                password = content[1]
                if passw in password:
                    File.loadGameField(File)
                    self.authWindow.destroy()
                else: tkinter.messagebox.showinfo("Помилка", "Хибний пароль!")
        else:
            with open((saveDir + name + "_save.txt"), "w+") as playerSave:
                playerSave.write("Ім'я: " + name + '\n')
                playerSave.write("Пароль: " + passw + '\n')
                self.authWindow.destroy()

#-------------------------------------------------------------------------
    def saveResults(self, didPlayerWin):
        """Эта функция контроллирует количество сохранённых результатов
        игры"""

        self.mode = File.deterMode(self)
        if self.mode == "Новачок": resultsArr = self.bResults
        elif self.mode == "Любитель": resultsArr = self.iResults
        else: resultsArr = self.eResults

        if didPlayerWin: resultsArr.append("1")
        else: resultsArr.append("0")
        if len(resultsArr) >= 10:
            self.shiftLeft(self, resultsArr)
        with open((saveDir + self.playerName + "_save.txt"), "w+") as playerSave:
            playerSave.write("Ім'я: " + self.playerName + '\n')
            playerSave.write("Пароль: " + self.playerPass + '\n')
            playerSave.write(str(self.bResults) + '\n')
            playerSave.write(str(self.iResults) + '\n')
            playerSave.write(str(self.eResults) + '\n')
            playerSave.write(str(self.bLastRating) + '\n')
            playerSave.write(str(self.iLastRating) + '\n')
            playerSave.write(str(self.eLastRating) + '\n')

#-------------------------------------------------------------------------
    def shiftLeft(self, lst):
        """Эта функция помогает функции saveResults"""
        res = self.calculateRating(File, lst, 0.0)
        if self.mode == 'Новачок': self.bLastRating = res
        elif self.mode == 'Любитель': self.iLastRating = res
        else: self.eLastRating = res
        lst.clear()

#-------------------------------------------------------------------------
    @staticmethod
    def calculateRating(self, resultsArr, lastResult):
        """Эта функция производит вычисления процентного рейтинга игрока:
        берёт данные из последних сыгранных игр и находит среди них
        выигранные, после чего вычисляет процент"""

        quantity = len(resultsArr)
        totalWins = resultsArr.count("'1',") + resultsArr.count("'1'") + resultsArr.count('1')
        if lastResult == 0.0:
            if quantity != 0: calcResult = (totalWins * 100) / quantity
            else: calcResult = 0
        else:
            if quantity != 0: calcResult = (lastResult+((totalWins * 100) / quantity))/2
            else: calcResult = lastResult
        return round(calcResult, 2)

#-------------------------------------------------------------------------
    def saveGameField(self):
        """Эта функция создаёт два файла: в одном хранится информация об открытых
        клетках, во втором - о значениях клеток поля. Данные сохраняются в бинарном
        формате"""

        if not isGameOver:
            global field, buttons
            openedCells = []

            for buttonRow in buttons:
                for b in buttonRow:
                    if b['state'] == 'disabled':
                        if b['text'] == "⚑": openedCells.append(2)
                        elif b['text'] == "?": openedCells.append(3)
                        else: openedCells.append(0)
                    else:
                        if b['text'] == " ": openedCells.append(1)

            with open((saveDir + self.playerName + "_cells.bin"), "w+b") as cellSheet:
                binCells = bytearray(openedCells)
                cellSheet.write(binCells)

            with open((saveDir + self.playerName + "_game.bin"), "w+b") as binaryField:
                for cellRow in field:
                    binField = bytearray(cellRow)
                    binaryField.write(binField)

#-------------------------------------------------------------------------
    def loadGameField(self):
        """Эта функция переводит бинарные файлы сохранений поля обратно в численный формат
        и восстанавливает поле в соответствии с значениями, полученными из файлов"""

        if os.path.exists(saveDir + self.playerName + "_game.bin"):
            global field, buttons
            response = tkinter.messagebox.askyesno("Загрузка гри",
                                                   message='Існує незавершена гра. \n'
                                                           'Хочете загрузить її?')
            if response:
                intCellsRow = []
                Cells = []

                with open((saveDir + self.playerName + "_cells.bin"), "r+b") as cellSheet:
                    cells = cellSheet.readlines()
                    for row in cells:
                        for c in row: Cells.append(int(c))

                if len(Cells) == 81: cellColumns = 9
                elif len(Cells) == 256: cellColumns = 16
                else: cellColumns = 30

                if cellColumns == 9: setSize(9, 9, 10)
                elif cellColumns == 16: setSize(16, 16, 40)
                else: setSize(16, 30, 99)

                openedCells = [Cells[i:i + cellColumns] for i in range(0, len(Cells), cellColumns)]

                if os.path.exists(saveDir + self.playerName + "_game.bin"):
                    with open((saveDir + self.playerName + "_game.bin"), "r+b") as binaryField:
                        binData = binaryField.readlines()
                        for cellRow in binData:
                            for c in cellRow:
                                intCellsRow.append(int(c))
                intCells = [intCellsRow[i:i + columns] for i in range(0, len(intCellsRow), columns)]

                # Коррекция игрового поля под загруженные из файлов значения
                field = intCells

                for n, row in enumerate(openedCells):
                    for nn, c in enumerate(row):
                        if c == 1:
                            buttons[n][nn]['state'] = 'normal'
                            buttons[n][nn]['relief'] = 'raised'
                        elif c == 2:
                            buttons[n][nn]["text"] = "⚑"

                            buttons[n][nn]["state"] = "disabled"
                        elif c == 3:
                            buttons[n][nn]["text"] = "?"
                            buttons[n][nn]["state"] = "disabled"
                        else:
                            Cell.clickOn(Cell, n, nn)

class Cell:
    firstClickHappened = False

#-------------------------------------------------------------------------
    def clickOn(self, x, y):
        """Эта функция контроллирует события, которые происходят
        по клику левой кнопкой мыши на клетку поля"""

        global field, buttons, colors, isGameOver, rows, columns
        if not self.firstClickHappened:
            # Обработка случая, когда игрок первым кликом попадает на мину
            if field[x][y] == 9:
                field[x][y] = 0
                valueGeneration(x, y, sub)

                # Замена уничтоженной мины на случайном месте - чтобы сохранить изначальное количество мин
                xx = random.randint(0, rows - 1)
                yy = random.randint(0, columns - 1)
                if buttons[xx][yy]['state'] != 'disabled':
                    field[xx][yy] = 9
                    valueGeneration(xx, yy, add)
                else:
                    xx = random.randint(0, rows - 1)
                    yy = random.randint(0, columns - 1)
                    # Переопределение значений соседних клеток
                    valueGeneration(x, y, sub)
                    valueGeneration(xx, yy, add)
            self.firstClickHappened = True

        if isGameOver: return
        buttons[x][y]["text"] = str(field[x][y])

        if field[x][y] == 9:  # Если игрок кликнул на мину
            buttons[x][y]["text"] = "✱"
            buttons[x][y].config(bg='red', disabledforeground='red')
            isGameOver = True
            Player.frown(Player)
            File.saveResults(File, False)
            os.remove(saveDir + File.playerName + "_game.bin")
            os.remove(saveDir + File.playerName + "_cells.bin")

            # После проигрыша отобразить все оставшиеся мины:
            for _x in range(0, rows):
                for _y in range(columns):
                    if field[_x][_y] == 9:
                        buttons[_x][_y]["text"] = "✱"
        else:  # Если клетка - обычное число, отобразить его с цветом и деактивировать кнопку
            buttons[x][y].config(disabledforeground=colors[field[x][y]])
        if field[x][y] == 0:  # если клетка пустая - запустить функцию автоклика
            buttons[x][y]["text"] = " "
            self.autoClickOn(self, x, y)
        buttons[x][y]['state'] = 'disabled'
        buttons[x][y].config(bg='white')
        buttons[x][y].config(relief=tkinter.GROOVE)
        File.saveGameField(File)
        checkWin()

#-------------------------------------------------------------------------
    def autoClickOn(self, x, y):
        """Эта функция контроллирует события, которые происходят,
        если клетка по которой кликнул игрок пуста - эта клетка
        и все соседние, которые также пусты, открываются автоматически"""
        global field, buttons, colors, rows, columns

        if field[x][y] != 9:

            if buttons[x][y]["state"] == "disabled":  # Если клетка уже открыта - пропускаем её
                return
            if field[x][y] != 0:  # Если клетка не пуста - отображаем её значение
                buttons[x][y]["text"] = str(field[x][y])
            else:  # Если клетка пуста - открываем и деактивируем её и повторяем проверку с соседними
                buttons[x][y]["text"] = " "
            buttons[x][y].config(disabledforeground=colors[field[x][y]])
            buttons[x][y].config(relief=tkinter.GROOVE)
            buttons[x][y]['state'] = 'disabled'
            buttons[x][y].config(bg='white')
            if field[x][y] == 0:
                if x != 0 and y != 0:
                    self.autoClickOn(self, x - 1, y - 1)
                if x != 0:
                    self.autoClickOn(self, x - 1, y)
                if x != 0 and y != columns - 1:
                    self.autoClickOn(self, x - 1, y + 1)
                if y != 0:
                    self.autoClickOn(self, x, y - 1)
                if y != columns - 1:
                    self.autoClickOn(self, x, y + 1)
                if x != rows - 1 and y != 0:
                    self.autoClickOn(self, x + 1, y - 1)
                if x != rows - 1:
                    self.autoClickOn(self, x + 1, y)
                if x != rows - 1 and y != columns - 1:
                    self.autoClickOn(self, x + 1, y + 1)

#-------------------------------------------------------------------------
    def onRightClick(self, x, y):
        """Эта функция контроллирует события, которые происходят
        по клику правой кнопкой мыши по клетке.
        По одинарному клику выставляется флажок (точно есть мина)
        По двойному клику - вопросительный знак (возможно есть мина)"""
        global buttons
        if isGameOver: return
        if buttons[x][y]["relief"] != tkinter.GROOVE:
            if buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
                buttons[x][y]["text"] = "⚑"
                buttons[x][y]["state"] = "disabled"
                File.saveGameField(File)
            elif buttons[x][y]["text"] == "⚑":
                buttons[x][y]["text"] = "?"
                File.saveGameField(File)
            else:
                buttons[x][y]["text"] = " "
                buttons[x][y]["state"] = "normal"
                File.saveGameField(File)

#-------------------------------------------------------------------------
class Player:
    faces = ["Гра іде", "Ви програли", "Ви виграли"]
    p = tkinter.Button(root, text=faces[0], font=('Helvetica', '30'), command=restartGame)

    def __init__(self, f=faces, p=p):
        self.f = f

    def frown(self):
        self.p.config(text=self.faces[1])
        pass

    def smile(self):
        self.p.config(text=self.faces[2])
        pass


File.playerAuth(File)
Player.p.grid(row=0, column=0, columnspan=columns, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
createMenu()
prepareWindow()
prepareGame()
root.mainloop()
