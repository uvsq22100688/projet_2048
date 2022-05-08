########################################
# projet_2048
# groupe MI TD04 
# Habib MABROUK
# Aissam BERRAHMANE
# Furkan YILMAZ
# Sylia OUAKLI
# https://github.com/uvsq22100688/projet_2048
#######################################
import tkinter as tk
from random import *
import ast

racine = tk.Tk()
racine.title("2048")


# Les Valeurs
H = 400 #Hauteur
L = 400 #Largeur


#####Les 13 fonctions########


def rgbtohex(r, g, b):
    """Cette fonction permet d'avoir des couleurs plus réalistes"""
    return f'#{r:02x}{g:02x}{b:02x}'


def fond():
    """Fonction créant le fond, en ajoutant 2 tuiles. """
    F = [[0 for i in range(0,4)] for j in range(0,4)]
    """La valeur 2 a 9fois plus de chance d'apparaitre que la valeur 4"""
    if randint(0,10) <= 9: 
        u = 2
    else: 
        u = 4
    if randint(0, 10) <= 9:
        v = 2
    else: 
        v = 4
    a = randint(0, 3)
    b = randint(0, 3)
    F[a][b] = u
    r = [randint(0, 3), randint(0, 3)]
    while a == r[0] and b == r[1]:
        r= [randint(0, 3), randint(0, 3)]
    F[r[0]][r[1]] = v
    return F

def create_bg():
    """Creation graphique du background"""
    for i in range(0,4):
        for j in range(0,4):
            canvas.create_rectangle((j * L//4, i * H//4), ((j + 1) * L//4, (i + 1) * H//4), fill=rgbtohex(208, 193, 180),outline=rgbtohex(187, 173, 160),width=10)



def values(liste):
    """Apparition des valeurs"""
    x = L // 8
    y = H // 8
    for a in range(len(liste)):
        for b in range(len(liste[a])):
            if liste[a][b] != 0:
                canvas.create_text(x, y, fill=rgbtohex(120, 111, 102), text=liste[a][b],font=("arial black", 35))
                
            x += H//4
        y += L//4
        x = H//8

def add(liste):
    """Ajout des tuiles à chaque clique """
    print("Before : ", liste)
    if randint(0,10) <= 9:
        u = 2
    else:
        u = 4
    liste1 = []
    for i in range(0,4):
        for j in range(0,4):
            if liste[i][j] == 0:
                liste1 += [[i, j]]
    v = randint(0, len(liste1))
    print(liste1[v-1])
    liste[liste1[v-1][0]][liste1[v-1][1]] = u
    print("After : ", liste)
    create_bg()
    values(liste)
    return liste

canvas = tk.Canvas(racine, height=H, width=L)
canvas.grid(column=1, row=1)

liste = fond()
create_bg()
values(liste) 

def merger(fusion):
    "Fonction permettant les fusions des tuiles"
    #Prise en compte de tout les cas possibles
    for i in range(len(fusion)):
        for j in range(len(fusion[i])):
            if fusion[i][1] == 0 and fusion[i][2] == 0 and fusion[i][0] == fusion[i][3]:
                fusion[i][0] += fusion[i][3]
                fusion[i][3] = 0
                break
            if fusion[i][1] == 0 and fusion[i][0] == fusion[i][2]:
                fusion[i][0] += fusion[i][2]
                fusion[i][1] = fusion[i][3]
                fusion[i][2] = 0
                fusion[i][3] = 0
                break
            if fusion[i][2] == 0 and fusion[i][0] == fusion[i][1] == fusion[i][3]:
                fusion[i][0] += fusion[i][1]
                fusion[i][1] = fusion[i][3]
                fusion[i][2] = 0
                fusion[i][3] = 0
                break
            
            if fusion[i][2] == 0 and fusion[i][1] == fusion[i][3]:
                fusion[i][1] += fusion[i][3]
                fusion[i][2] = 0
                fusion[i][3] = 0
                if fusion[i][0] == 0:
                    fusion[i][0] = fusion[i][1]
                    fusion[i][1] = fusion[i][2]
                    fusion[i][2] = 0
                break
            if j < 3:
                if fusion[i][j] == fusion[i][j+1]:
                    fusion[i][j] += fusion[i][j]
                    fusion[i][j+1] = 0
            if j > 0 and fusion[i][j-1] == 0:
                fusion[i][j-1] = fusion[i][j]
                fusion[i][j] = 0
                
        for k in range(len(fusion[i])):
            if fusion[i][k] == 0 and k < 3:
                fusion[i][k] = fusion[i][k+1]
                fusion[i][k+1] = 0
    return fusion

def rotate(mat):
    " Fonction permetant un rotation de 90° vers la droite(Vu en  IN202). "
    R = []
    for i in range(4):
        A = []
        for j in range(4):
            A.append(mat[j][i])
        A.reverse()
        R.append(A)
    mat = R
    return mat

def changement_direction(mat, sens):
    " Les mouvement vers la droite,gauche,haut et bas "
    global liste
    l = []
    for i in range(len(liste)):
        l.append([])
        for j in range(len(liste)):
            l[i].append(liste[i][j])
    if sens == "Right":
        liste = rotate(rotate(merger(rotate(rotate(mat)))))
    elif sens == "Left":
        liste = merger(mat)
    elif sens == "Up":
        liste = rotate(merger(rotate(rotate(rotate(mat)))))
    elif sens == "Down":
        liste = rotate(rotate(rotate(merger(rotate(mat)))))
    create_bg()
    values(liste)
    if l == rotate(rotate(merger(rotate(rotate(mat))))) and l == merger(mat) and l == rotate(merger(rotate(rotate(rotate(mat))))) and l == rotate(rotate(rotate(merger(rotate(mat))))):
        canvas.create_text(150, 150, fill="red", text="GAME OVER", font=("Helvetica", 30))
    if l!= liste:
        add(liste)
    label["text"] = str(score())
    victoire(liste)
    return liste

def victoire(liste):
    """Fonction qui affiche lorque l'on gagne"""
    for i in range(4):
        for j in range(4):
            if (liste[i][j] == 2048):
                canvas.create_text(150, 150, fill="green", text="WIN", font=("helvetica", 30))

def clavier(event):
    global liste
    touche = event.keysym #correspond au caractère qui va s'afficher dans une zone de texte en appuyant sur cette touche.
    Button = ["Right", "Left", "Up", "Down"]#Utiliser les touches du clavier pour les mouvement haut,bas,gauche,droite.
    if touche in Button:
        changement_direction(liste, touche)

racine.bind('<Key>', clavier)# Les movements des tuiles via le Clavier


def Save(liste):
    """Cette fonction permet de sauvegarder la patie via son boutton.(Vu en IN202)"""
    u = liste
    sauvegarde = open("2048.txt", "a")
    sauvegarde.write(str(u) + "\n")
    sauvegarde.close()

def Load():
    """Cette fonction permet de charger une partie via son boutton(Vu en IN202)"""
    global liste
    fic = open("2048.txt","r")
    b = []
    for i in range(4):
        b.append([0]*4)
    for l in fic:
        for i in range(4):
            for j in range(4):
                b[i][j] = int(l)
                l = fic.readline()
    fic.close()
    liste = b
    print(liste, "Load")



def score():
    " Fonction affichant le score"
    score = 0
    for i in range(len(liste)):
        for j in range(len(liste[i])):
            score += liste[i][j]
    return score
label = tk.Label(text = str(score()),font =("helvetica",25),bg = "white")
label.grid(column=1, row=3)



# Les Boutons
Bouton_Exit = tk.Button(racine, text="quitter",command=racine.quit, borderwidth=6)
Bouton_Exit.grid(column=3, row=0)

Bouton_Play = tk.Button(racine, text='Play', command=fond, borderwidth=6)
Bouton_Play.grid(column= 0, row = 0)

Bouton_Save = tk.Button(racine, text="Sauvegarder", command=lambda: Save(liste),borderwidth=6)
Bouton_Save.grid(column=0, row=3)

Bouton_Load = tk.Button(racine, text="Charger",command=lambda: values(Load()), borderwidth=6)
Bouton_Load.grid(column=3, row=3)


racine.mainloop()