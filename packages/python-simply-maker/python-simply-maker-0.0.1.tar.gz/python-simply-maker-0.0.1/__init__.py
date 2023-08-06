
import os
import time
import random
from flask import Flask, render_template
print("Welcome to python-simply-maker !")
my_secret = os.environ['test']

class console:
    def dire(entree):
        print(entree)

    def effacer():
        clear = lambda: os.system('clear')
        clear()

class texte:
    file = ""
    def set_file(fichier):
        global file
        file = fichier

    def ecrire(entree):
        global file
        writing = open(file, "w")
        a_la_ligne = entree.replace('\in', '\n')
        writing.write(a_la_ligne)
        writing.close()

    def lire():
        global file
        writing = open(file, "r")
        return writing.read()
        writing.close()

    def lire_nb(entree):
        global file
        writing = open(file, "r")
        return writing.read(entree)
        writing.close()


def repeter(entree, nb):
    x = 0

    while x < nb:
        console.dire(entree)
        time.sleep(0.5)
        x += 1

def attendre(temps):
    time.sleep(temps) 

def nombre_random(*max, **min):
    try:
        return random.randint(max, min)
    except:
        return random.randint(1, 10)

class site:
    def creer_site(template):
        app = Flask(__name__)
        @app.route('/')
        def home():
            return render_template(template)
        while True:
            app.run()

def hello_world(*entree):
    if entree == 'python':
        console.dire('Hello World of python !')
    else:
        console.dire('Hello World')

class liamgen:
    def discord():
        return 'liamgen#1473'

    def github():
        return 'liam-gen'
    
    def site():
        return 'en-dev'

class dsm:
    def discord():
        npm = 'https://www.npmjs.com/package/'
        return f'{npm}discord-simply-maker'
    
    def insta():
        return 'https://www.npmjs.com/package/insta-simply-maker'
