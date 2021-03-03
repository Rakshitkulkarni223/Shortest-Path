from collections import deque, namedtuple
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import pyttsx3

root = Tk()
engine=pyttsx3.init()
root.title("CITY MAP")
root.geometry("1000x1000")
canvas = Canvas(root, width=800, height=800)
canvas.pack(fill=BOTH,expand=True)
bgImg = PhotoImage(file="C:\\Users\\raksh\\OneDrive\\Desktop\\bg.png")
canvas.create_image(300,300,image=bgImg)
bgImg1= PhotoImage(file="C:\\Users\\raksh\\OneDrive\\Desktop\\bg.png")
canvas.create_image(1000,300,image=bgImg)

my_canvas=Canvas(canvas, width=600, height=900, bg="#26F0D0")
my_canvas.pack(pady=100,padx=100)

'''places is list.
Its each element is also a list of 2 elements.
The 1st element is x co-ordinate and 2nd is y co-ordinate of location'''
places=[]
'''roads is a list.
Its each element is also a list of 2 elements
The 2 elements are loactions joined by the road
'''

cities={}
roads=[]
distance={}
r=25
city_number=1

def rightClick(event):
    global city_number
    newPlace=[event.x,event.y]
    for existingPlaces in places:
        if pow((existingPlaces[0]-event.x),2)+pow((existingPlaces[1]-event.y),2)<=4*r*r:
            messagebox.showerror("Error", "Overlapping of Nodes not allowed")
            break
    else:
        places.append(newPlace)
        my_canvas.create_oval(event.x-r,event.y-r,event.x+r,event.y+r, fill="#6270EA")
        my_canvas.create_text(event.x,event.y,text="city {}".format(city_number),font=('Arial',15))
        cities[city_number]=newPlace
        city_number += 1

city_distances={}
g=[]
vertices=[]
edges=[]
def create_matrix(distance_):
    global distance,city_number,graph
    for i in range(1,city_number):
        l=[]
        for j in range(1,city_number):
            if distance_.get((i,j))!=None:
                l.append(1)
            else:
                l.append(0)
        edges.append(l)
    for i,j in distance_.items():
        g.append([i[0],i[1],int(j)])
        city_distances[i]=int(j)
    values=list(city_distances.values())
    k=city_number-1
    i=0
    while i<(len(values)):
        vertices.append(values[i:city_number-1+i])
        i=i+k


flag=0
tempRoad=[]
def click(event):
     global flag
     for existingPlaces in places:
        if pow((existingPlaces[0]-event.x),2)+pow((existingPlaces[1]-event.y),2)<=r*r:
            flag=1
            tempRoad.append(existingPlaces)
            break
        else:
            flag=0
citynumber_and_edge={}
neighbours={}
def release(event):
    global flag,tempRoad,distance,citynumber_and_edge
    try:
        for existingPlaces in places:
            if pow((existingPlaces[0] - event.x), 2) + pow((existingPlaces[1] - event.y), 2) <= r * r:
                flag = 2
                tempRoad.append(existingPlaces)
                break
            else:
                flag = 0
        if flag == 2:

            x1 = tempRoad[0][0]
            x2 = tempRoad[1][0]
            y1 = tempRoad[0][1]
            y2 = tempRoad[1][1]

            city1, city2 = 0, 0
            for citynumber,coord in cities.items():
                if coord[0] == x1:
                    citynumber_and_edge[citynumber]=[x1,y1]
                    city1 = citynumber
                if coord[0] == x2:
                    citynumber_and_edge[citynumber] = [x2, y2]
                    city2 = citynumber
            neighbours.setdefault(city1,[]).append(city2)
            neighbours.setdefault(city2, []).append(city1)


            if city1 == city2:
                messagebox.showerror("Error", "Not Allowed to create self loop")
            else:
                my_canvas.create_line(x1, y1, x2, y2, fill="#F74C49", width=3, smooth=True)
                my_canvas.create_oval(x1 - 4, y1 - 4, x1 + 4, y1 + 4, fill="#16F50A")
                my_canvas.create_oval(x2 - 4, y2 - 4, x2 + 4, y2 + 4, fill="#16F50A")

                edge_weight = askstring('Input','Enter The distance between city {} and city {} in km : '.format(city1, city2))
                try:
                    if edge_weight==None or not edge_weight.isalnum():
                        messagebox.showinfo("Information", "By default distance between any two cities is 1")
                        edge_weight = "1"
                    while edge_weight.isalpha() == True:
                        messagebox.showerror("Error", "Distance between any two cities must be in numbers")
                        edge_weight = askstring('Input',
                                                'Enter The distance between city {} and city {} in km : '.format(city1,
                                                                                                                 city2))
                    flag = True
                    while flag:
                        if int(edge_weight) <= 0:
                            print("yes")
                            messagebox.showerror("Error", "Distance between any two cities must be Greater than 0")
                            flag = False

                        if flag == False:
                            edge_weight = askstring('Input',
                                                    'Enter The distance between city {} and city {} in km : '.format(
                                                        city1, city2))
                            flag = True
                        else:
                            break
                except:
                    pass

                finally:
                    x = (x1 + x2) // 2
                    y = (y1 + y2) // 2
                    if city1 != 0 and city2 != 0:
                        distance[(city1, city2)] = edge_weight
                    vertices.clear()
                    edges.clear()
                    create_matrix(distance)
                    my_canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="#FAA7E0")
                    my_canvas.create_text(x, y, text="{}km".format(edge_weight))
                    roads.append(tempRoad)

        flag = 0
        tempRoad.clear()
    except:
        pass

starting_points=[]
end_points=[]
previous_starting_point={}
previous_ending_point={}
start=0
end=0

def StartingPoint(event):
    global previous_starting_point,f,start
    f=True
    x_cord=event.x
    y_cord=event.y
    try:
        while f:
            for existingPlaces in places:
                if pow((existingPlaces[0] - x_cord), 2) + pow((existingPlaces[1] - y_cord), 2) <= 4 * r * r:
                    for citynumber, coord in cities.items():
                        if coord[0] == existingPlaces[0] and len(starting_points) == 0:
                            starting_points.extend(coord)
                            previous_starting_point[citynumber]=coord
                            my_canvas.create_oval(existingPlaces[0] - r, existingPlaces[1] - r, existingPlaces[0] + r, existingPlaces[1] + r, fill="orange")
                            my_canvas.create_text(existingPlaces[0], existingPlaces[1], text="city {}".format(citynumber), font=('Arial', 15))
                            messagebox.showinfo("Info", "Start Point is Defined")
                            start=citynumber
                            f=False
                        elif len(starting_points) != 0 and existingPlaces[0]!=starting_points[0]:
                            messagebox.showinfo("Info", "Starting Point is Already Defined")
                            p = messagebox.askquestion("Confirmation", "Do you want to change Starting point?")
                            if p == "yes":
                                my_canvas.create_oval(starting_points[0] - r,starting_points[1] - r,starting_points[0] + r, starting_points[1] + r, fill="#6270EA")
                                my_canvas.create_text(starting_points[0], starting_points[1],text="city {}".format(list(previous_starting_point.keys())[0]), font=('Arial', 15))
                                starting_points.clear()
                                messagebox.showinfo("Info", "Start Point is Changed")
                                f=True
                            else:
                                f=False
                                return
                        else:
                            f=False
            if f==False:
                break
    except:
        pass

def EndPoint(event):
    global previous_ending_point,end
    f=True
    try:
        while f:
            for existingPlaces in places:
                if pow((existingPlaces[0] - event.x), 2) + pow((existingPlaces[1] - event.y), 2) <= 4 * r * r:
                    for citynumber, coord in cities.items():
                        if coord[0] == existingPlaces[0] and len(end_points) == 0:
                            end_points.extend(coord)
                            previous_ending_point[citynumber]=coord
                            my_canvas.create_oval(existingPlaces[0] - r, existingPlaces[1] - r, existingPlaces[0] + r, existingPlaces[1] + r, fill="#CD45F4")
                            my_canvas.create_text(existingPlaces[0], existingPlaces[1], text="city {}".format(citynumber), font=('Arial', 15))
                            messagebox.showinfo("Info", "End Point is Defined")
                            end=citynumber
                            f=False
                            return
                        elif len(end_points) != 0 and existingPlaces[0]!=end_points[0]:
                            messagebox.showinfo("Info", "Ending Point is Already Defined")
                            p = messagebox.askquestion("Confirmation", "Do you want to change Ending point?")
                            if p == "yes":
                                my_canvas.create_oval(end_points[0] - r,end_points[1] - r,end_points[0] + r, end_points[1] + r, fill="#6270EA")
                                my_canvas.create_text(end_points[0], end_points[1],text="city {}".format(list(previous_ending_point.keys())[0]), font=('Arial', 15))
                                messagebox.showinfo("Info", "End Point is Changed")
                                end_points.clear()
                            else:
                                f=False
                                return
                        else:
                            f=False
            if f==False:
                break
    except:
        pass

def clear():
    global  my_canvas,places,city_number,distance
    my_canvas.delete("all")
    starting_points.clear()
    end_points.clear()
    previous_starting_point.clear()
    previous_ending_point.clear()
    cities.clear()
    roads.clear()
    places.clear()
    distance.clear()
    city_number=1
    return

def info():
    information='''Right click :- To create city\n\nDouble-Click and Release or Left-Click and Release :- To create path between two cities\n\nShift and Right Click(shift + Right-Click) :- To create Starting Point\n\nControl and Right Click(ctrl + Right-Click) :- To create End Point'''
    messagebox.showinfo("INFORMATION",information)

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges), []))

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))
            neighbours[edge.end].add((edge.start, edge.cost))
        return neighbours

    def dijkstra(self, source, dest):
        try:
            assert source in self.vertices, 'Such source node doesn\'t exist'
            distances = {vertex: inf for vertex in self.vertices}
            previous_vertices = { vertex: None for vertex in self.vertices }
            distances[source] = 0
            vertices = self.vertices.copy()

            while vertices:
                current_vertex = min(vertices, key=lambda vertex: distances[vertex])
                vertices.remove(current_vertex)
                if distances[current_vertex] == inf:
                    break
                for neighbour, cost in self.neighbours[current_vertex]:
                    alternative_route = distances[current_vertex] + cost
                    if alternative_route < distances[neighbour]:
                        distances[neighbour] = alternative_route
                        previous_vertices[neighbour] = current_vertex

            path, current_vertex = deque(), dest
            while previous_vertices[current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            if path:
                path.appendleft(current_vertex)
            return path
        except:
            return [0]
shortest=[]
def shortest_path():
    global start,end,distance,shortest
    if len(starting_points)==0 or len(end_points)==0:
        if len(starting_points)==0:
            messagebox.showerror("Error","Staring Point is not defined")
        else:
            messagebox.showerror("Error","End Point is not defined")
    else:
        if len(shortest)!=0:
            for i in range(len(shortest) - 1):
                a = shortest[i]
                b = shortest[i + 1]
                X = citynumber_and_edge[a]
                Y = citynumber_and_edge[b]
                my_canvas.create_line(X[0], X[1], Y[0], Y[1], fill="#F74C49", width=3, smooth=True)
                my_canvas.create_oval(X[0] - 4, X[1] - 4, X[0] + 4, X[1] + 4, fill="#EEF80A")
                my_canvas.create_oval(Y[0] - 4, Y[1] - 4, Y[0] + 4, Y[1] + 4, fill="#EEF80A")
                x = (X[0] + Y[0]) // 2
                y = (X[1] + Y[1]) // 2
                my_canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="#FAA7E0")
                if distance.get((a, b)) == None:
                    edge_weight = distance[(b, a)]
                else:
                    edge_weight = distance[(a, b)]
                my_canvas.create_text(x, y, text="{}km".format(edge_weight))
        path = Graph(g)
        shortest = list(path.dijkstra(start, end))
        if len(shortest)==1 and shortest[0]==0:
            messagebox.showinfo("Info","Path Between City {}  and City {} Does not Exist".format(start,end))
        else:
            try:
                total_distance=[]
                for i in range(len(shortest) - 1):
                    a = shortest[i]
                    b = shortest[i + 1]
                    X = citynumber_and_edge[a]
                    Y = citynumber_and_edge[b]
                    my_canvas.create_line(X[0], X[1], Y[0], Y[1], fill="#04FA03", width=3, smooth=True)
                    my_canvas.create_oval(X[0] - 4, X[1] - 4, X[0] + 4, X[1] + 4, fill="#EEF80A")
                    my_canvas.create_oval(Y[0] - 4, Y[1] - 4, Y[0] + 4, Y[1] + 4, fill="#EEF80A")
                    x = (X[0] + Y[0]) // 2
                    y = (X[1] + Y[1]) // 2
                    my_canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="#FAA7E0")
                    if distance.get((a, b)) == None:
                        edge_weight = distance[(b, a)]
                    else:
                        edge_weight = distance[(a, b)]
                    total_distance.append(int(edge_weight))
                    my_canvas.create_text(x, y, text="{}km".format(edge_weight))
                p="->".join(map(str,shortest))
                messagebox.showinfo("Info","SHORTEST PATH BETWEEN CITY {} AND CITY {} IS {}\nTotal Distance = {} km (kilometer) ".format(shortest[0],shortest[len(shortest)-1],p,sum(total_distance)))
                s="Starting with City Number {}!!and ".format(shortest[0])
                dist=total_distance[0]
                for i in range(1,len(shortest)-1):
                    s+="!!Then Go to !!city number {} which is !!{} kilometer from city {} ".format(shortest[i],dist,shortest[0])
                    dist+=total_distance[i]
                s+="!!Next is your destination that is city number {}!!which is !!{} kilometer from city {}!!You need to travel!!total !{} kilo meter to reach !!your destination!! This is nothing but !the shortest path from city {} to city {}".format(shortest[len(shortest)-1],dist,shortest[0],sum(total_distance),shortest[0],shortest[len(shortest)-1])
                content="Hello!!Welcome to city map!! To Reach the city {} !!from city {} !!within a short period of time !!follow this path !!that is {} , Thank you!!Happy and Safe Jouney!!".format(shortest[len(shortest)-1],shortest[0],s)
                engine.setProperty('rate', 150)
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.say(content)
                engine.runAndWait()
                return
            except:
                messagebox.showinfo("Info", "Path Between City {}  and City {} Does not Exist".format(start, end))

l1 = Label(canvas, text="WELCOME TO SHORTEST PATH BETWEEN TWO CITIES INTERFACE",fg="#8000ff",font="Times 20 bold",bg="#F573A2")
l1.place(x=220,y=30)

my_canvas.bind("<Button-3>",rightClick)

my_canvas.bind("<ButtonPress-1>", click)
my_canvas.bind('<ButtonRelease-1>', release)

my_canvas.bind("<Shift-Button-3>",StartingPoint)

my_canvas.bind("<Control-Button-3>",EndPoint)


control_frame=LabelFrame(root,text="User Controls",bg="#F4A5A5")
control_frame.place(x=80,y=200)

clear_btn=Button(control_frame,text="CLEAR",command=clear,bg="#A5D3F4")
clear_btn.pack(pady=10)

info_btn=Button(control_frame,text="INFO",command=info,bg="#D2A5F4")
info_btn.pack(pady=10)

get_btn=Button(control_frame,text="SHORTEST PATH",command=shortest_path,bg="#E6F4A5")
get_btn.pack(pady=10)

root.mainloop()
