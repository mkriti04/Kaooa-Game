import turtle
import time
class Kaoo:
    def __init__(self):
        self.vulture_pos = -1
        self.die_crow = 0
        self.end = 0
        self.coords = []
        self.buttons = {}
        self.clicks = 0
        self.prev = -1
        self.prev_c = -1
        self.neighbours = { 
            0: [6, 7], 
            1: [8, 9], 
            2: [5, 6], 
            3: [7, 8], 
            4: [5, 9],
            5: [2, 4, 6, 9],
            6: [0, 2, 7, 5],
            7: [0, 3, 6, 8],
            8: [1, 3, 7, 9],
            9: [1, 4, 5, 8]
        }
        self.lines = [
            [4,5,6,0],
            [0,7,8,1],
            [1,9,5,2],
            [2,6,7,3],
            [3,8,9,4]
        ]
    def draw_star(self, size, line_size):
        turtle.pensize(line_size)
        for _ in range(5):
            turtle.forward(size)
            turtle.right(144)
            x, y = turtle.pos()
            self.coords.append((x,y))

    def place_button(self):
        j = 0
        for i in self.coords:
            x = i[0]
            y = i[1]
            self.move_pen(x, y)
            turtle.dot(45, "beige") 
            x, y = turtle.pos()
            self.buttons[j] = {'x': x, 'y': y, 'clicked': False, 'crow': False, 'vulture': False}
            j += 1

    def move_pen(self, x, y):
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()

    def on_dot_click(self,x, y):
        flag_1 = -1
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            if abs(x - button['x']) < 22.5 and abs(y - button['y']) < 22.5 and self.end == 0:
                if self.clicks > 1 and self.check_if_blocked():
                    self.show_winner('Crow')
                    break
                if (button['crow'] or button['vulture']) and button['clicked']:
                    if button['crow']:
                        if self.clicks % 2 != 0:
                            self.move_pen(0,0)
                            turtle.write("Invalid move it's vulture's turn", align="center", font=("Arial", 14, "bold"))
                            time.sleep(1)
                            turtle.undo()
                            continue
                        elif self.clicks > 13 :
                            self.prev_c = i
                            self.show_empty(self.prev_c)
                    elif button['vulture']:
                        if self.clicks % 2 == 0:
                            self.move_pen(0,0)
                            turtle.write("Invalid move it's crow's turn", align="center", font=("Arial", 14, "bold"))
                            time.sleep(1)
                            turtle.undo()
                            continue
                        else:
                            self.prev = i
                            self.show_empty(self.prev)
                elif not button['clicked']:
                    if self.prev >= 0 or self.prev_c >= 0:
                        if self.prev >= 0 and self.clicks % 2 != 0:
                            flag_1 = 1
                            if self.check_if_neighbours(self.prev, i) != 1:
                                kill = self.check_empty(self.prev, i)
                                if kill >= 0:
                                    self.move_vulture_kill(kill,i,self.prev)
                                    self.die_crow += 1
                                    if self.die_crow == 4:
                                        self.show_winner('Vulture')
                                        self.end = 1
                                        break
                                    self.show_player()       
                                    continue
                            else:
                                self.buttons[i]['clicked'] = True
                                self.clicks += 1
                        elif self.prev_c >= 0 and self.clicks % 2 == 0:
                            flag_1 = 0
                            if self.check_if_neighbours(self.prev_c, i) == 1:
                                self.buttons[i]['clicked'] = True
                                self.clicks += 1
                    if self.clicks == 1:
                        self.buttons[i]['clicked'] = True
                        self.clicks += 1
                    elif self.prev_c < 0 and flag_1 != 1 and self.clicks % 2 == 0:
                        self.buttons[i]['clicked'] = True
                        self.clicks += 1
                    if self.clicks % 2 != 0 and flag_1 != 1:
                        self.move_crow(i,self.prev_c)
                    elif self.clicks % 2 == 0:
                        self.move_vulture(i)
                    self.show_player()
                if self.clicks > 1 and self.check_if_blocked():
                    self.show_winner('Crow')
                    break

    def check_if_blocked(self):
        count = 1
        flag = 1
        for i in self.neighbours[self.vulture_pos]:
            if not self.buttons[i]['clicked']:
                return False
        for i in self.neighbours[self.vulture_pos]:
            l = self.find_line(i, self.vulture_pos)
            for k in range(4):
                if self.buttons[l[k]]['vulture']:
                    if (k > 0 and k < 3 and (not self.buttons[l[k - 1]]['crow'] or not self.buttons[l[k + 1]]['crow'])
                        or (k == 1 and not self.buttons[l[k + 2]]['crow']) or (k == 2 and not self.buttons[l[k - 2]]['crow'])):
                            count = 0
                    elif k == 0 and (not self.buttons[l[k + 1]]['crow'] or not self.buttons[l[k + 2]]['crow']):
                        count = 0
                    elif k == 3 and (not self.buttons[l[k - 1]]['crow'] or not self.buttons[l[k - 2]]['crow']):
                        count = 0
                    else:
                        count = 1
            if count == 0:
                flag = 0
                break
        if flag == 1:
            return True

    def find_line(self,a, b):
        for i in self.lines:
            for j in range(len(i)):
                if j != 3 and ((i[j] == a and i[j + 1] == b) or (i[j + 1] == a and i[j] == b)):
                    return i
        return 0

    def show_winner(self,person):
        self.move_pen(0, 0)
        turtle.write(f"{person} is the Winner", align="center", font=("Arial", 16, "bold"))
        time.sleep(2)
        turtle.undo()
        turtle.write("GAME ENDED", align="center", font=("Arial", 16, "bold"))
        turtle.done()

    def show_player(self):
        self.move_pen(0, 0)
        if self.clicks % 2 != 0:
            if self.clicks > 1:
                person = "Move Vulture"
            elif self.clicks == 1:
                person = "Place the Vulture"
        else:
            if self.clicks < 13:
                person = "Place a Crow"
            elif self.clicks >= 13:
                person = "Move Crow"
        turtle.write(f"{person}", align="center", font=("Arial", 15, "bold"))
        time.sleep(1)
        turtle.undo()

    def show_start(self):
        turtle.write("START GAME", align="center", font=("Arial", 16, "bold"))
        time.sleep(1)
        turtle.undo()
        turtle.write("Place a Crow", align="center", font=("Arial", 16, "bold"))
        time.sleep(1)
        turtle.undo()

    def move_crow(self,index_c, previous):
        if previous >= 0 and self.buttons[previous]['crow']:
            self.move_pen(self.buttons[previous]['x'], self.buttons[previous]['y'])
            turtle.dot(45, "beige")  
            self.buttons[previous]['crow'] = False
            self.buttons[previous]['vulture'] = False
            self.buttons[previous]['clicked'] = False
        self.move_pen(self.buttons[index_c]['x'], self.buttons[index_c]['y'])
        turtle.dot(45, "#EB455F")  # pink
        self.buttons[index_c]['crow'] = True

    def move_vulture_kill(self, middle,index,previous):
        self.buttons[index]['clicked'] = True
        self.clicks += 1
        if previous >= 0 and self.buttons[previous]['vulture']:
            turtle.undo()
            self.move_pen(self.buttons[previous]['x'], self.buttons[previous]['y'])
            turtle.dot(45, "beige")
            self.buttons[previous]['vulture'] = False
            self.buttons[previous]['clicked'] = False
            self.buttons[previous]['crow'] = False
        self.move_pen(self.buttons[index]['x'], self.buttons[index]['y'])
        turtle.dot(45, "#0C356A")  # darkblue
        self.buttons[previous]['crow'] = False
        self.buttons[index]['vulture'] = True
        self.buttons[index]['clicked'] = True
        self.vulture_pos = index
        self.move_pen(self.buttons[middle]['x'], self.buttons[middle]['y'])
        turtle.dot(45, "beige") 
        self.buttons[middle]['vulture'] = False
        self.buttons[middle]['crow'] = False
        self.buttons[middle]['clicked'] = False

    def move_vulture(self,k):
        if self.prev >= 0 and self.buttons[self.prev]['vulture']:
            turtle.undo()
            self.move_pen(self.buttons[self.prev]['x'], self.buttons[self.prev]['y'])
            turtle.dot(45, "beige")
            self.buttons[self.prev]['vulture'] = False
            self.buttons[self.prev]['clicked'] = False
        self.move_pen(self.buttons[k]['x'], self.buttons[k]['y'])
        turtle.dot(45, "#0C356A")  # darkblue
        self.vulture_pos = k
        self.buttons[k]['vulture'] = True

    def check_empty(self,p, i):
        for k in self.lines:
            if ((k[0] == p and k[2] == i) or (k[0] == i and k[2] == p)) and self.buttons[k[1]]['clicked']:
                return k[1]
            elif ((k[1] == p and k[3] == i) or (k[1] == i and k[3] == p)) and self.buttons[k[2]]['clicked']:
                return k[2]
        return -1

    def show_empty(self, index):
        for i in self.neighbours[index]:
            if not self.buttons[i]['clicked']:
                self.move_pen(self.buttons[i]['x'], self.buttons[i]['y'])
                turtle.write("Empty", align="center", font=("Arial", 12, "bold"))
                time.sleep(0.5)
                turtle.undo()

    def check_if_neighbours(self,index, neighbour):
        for i in self.neighbours[index]:
            if i == neighbour:
                return 1
        return -1

    def find_intersecpoints(self):
        c = [[0,4,1,2],[0,4,2,3],[0,1,2,3],[0,1,3,4],[1,2,3,4]]
        for i in c:
            m1 = (self.coords[i[0]][1] - self.coords[i[1]][1]) / (self.coords[i[0]][0] - self.coords[i[1]][0])
            m1 = (self.coords[i[0]][1] - self.coords[i[1]][1]) / (self.coords[i[0]][0] - self.coords[i[1]][0])
            b1 = self.coords[i[1]][1] - m1 * self.coords[i[1]][0]
            m2 = (self.coords[i[2]][1] - self.coords[i[3]][1]) / (self.coords[i[2]][0] - self.coords[i[3]][0])
            b2 = self.coords[i[3]][1] - m2 * self.coords[i[3]][0]
            x = (b2 - b1) / (m1 - m2)
            y = m1 * x + b1
            self.coords.append((x,y))

    def indicate_buttons(self):
        self.move_pen(240,370)
        turtle.dot(30, "beige") 
        self.move_pen(290, 360)
        turtle.write("Empty", align="center", font=("Arial", 12, "bold"))
        self.move_pen(240,330)
        turtle.dot(30, "#EB455F") 
        self.move_pen(285,320)
        turtle.write("Crow", align="center", font=("Arial", 12, "bold"))
        self.move_pen(240,290)
        turtle.dot(30, "#0C356A") 
        self.move_pen(290,280)
        turtle.write("Vulture", align="center", font=("Arial", 12, "bold"))


    def main(self):
        turtle.title("KAOOA GAME")
        turtle.speed(10)
        turtle.bgcolor("#BAD7E9")
        turtle.hideturtle()
        self.move_pen(-350, 100)
        star_size = 700
        line_size = 5
        self.draw_star(star_size, line_size)
        self.find_intersecpoints()
        self.place_button()
        self.indicate_buttons()
        self.move_pen(0, 0)
        self.show_start()
        turtle.onscreenclick(self.on_dot_click)
        turtle.done()

game = Kaoo()
game.main()