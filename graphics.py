#################################################
# TERM PROJECT --- TP3 #GRAPHICS
#
# Your name: BHARATHI  SRIDHAR
# Your andrew id: bsridha2
#################################################

import math, copy, os, random, string
from cmu_112_graphics import *
import nltk 
from nltk.util import ngrams

import mainfile as nlp

#################################################
# MAIN REFERENCES:
# CMU 15-112 Course notes:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
#################################################

##########################################
# Splash Screen Mode
##########################################

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#A6D0D1")
    font = 'Courier 26 bold'
    canvas.create_text(app.width/2, app.height/4, text='AUTOCOMPLETE', 
                                                    font="Courier 46 bold")
    canvas.create_text(app.width/2, 250, 
                        text='Press START!', font=font)
    x0, y0, x1, y1 = 0.4*app.width, 0.6*app.height, 0.6*app.width, 0.7*app.height
    #col = random.choice(app.colors)
    canvas.create_rectangle(x0, y0, x1, y1, fill = 'light green')
    canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'START', font = "Times 26 bold")

def splashScreenMode_keyPressed(app, event):
    pass

def splashScreenMode_mousePressed(app, event):
    if (0.45*app.width <= event.x <= 0.55*app.width) and (0.6*app.height<= event.y <= 0.7*app.height):
        app.mode = 'gameMode'

##########################################
# Game Mode
##########################################

def gameMode_redrawAll(app, canvas):
    #if app.isNewGame:
    #    drawNewGame(app, canvas)
    drawBG(app, canvas)
    for (x0,y0,col,size, label) in app.buttonList:
        drawButton(app,canvas,x0, y0, col, size, label)
    x0,y0, x1, y1 = app.boxCoords
    font = 'Courier 16 bold'
    canvas.create_text((x0+x1)/2, y1/2 + 20, text = app.brokenSen, 
                    font = font)
        #drawAutocomplete(app, canvas)
    drawOptions(app, canvas)
    
def gameMode_keyPressed(app, event):
    if (event.key == '0'):
        app.mode = 'helpMode'

def gameMode_mousePressed(app, event):
    x0, y0, x1, y1 = app.boxCoords
    if x0 <= event.x <= x1 and y0 <= event.y <= y1:
        app.inBox = True 
    else:
        app.inBox = False
    inButton(app, event.x, event.y)
    isInOption(app, event.x, event.y)
    if isInCheck(app, event.x, event.y):
        name = app.getUserInput('Are you Sure?')
        if (name == None):
            app.message = 'You canceled!'
        elif name.lower() == 'yes' or name.lower() == 'y':
            #app.showMessage('You entered: ' + name)
            if app.optionSelected != None:
                validateResult(app, app.answer, app.optionSelected) 
    
def gameMode_timerFired(app):
    if app.gameOver:
        app.mode = 'gameOver'
    t = app.timer//app.timerDelay - app.trackTime//app.timerDelay 
    if t <= 0:
        t = 0
        app.gameOver = True 
    if app.timer >= app.trackTime:
        app.trackTime += app.timerDelay 
    app.coltimer += 1

##########################################
# Help Mode
##########################################

def helpMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#639AE1")
    font = 'Courier 20 bold'
    canvas.create_text(app.width/2, 200, 
                            text='How to play the game:\n Easy mode: Guess which of the 4 options \n is the best word to complete the sentence.\n Hard mode: Guess the missing word before the \nautocomplete AI guesses it.', font=font)
    canvas.create_text(app.width/2, 550, 
                                text='Press 0 to return to game!', font=font)

def helpMode_keyPressed(app, event):
    if event.key.lower() == "0":
        app.mode = 'gameMode'
        app.score = 0

##########################################
# Main App
##########################################

def appStarted(app):
    app.mode = 'splashScreenMode'
    app.score = 0
    app.inBox = False
    app.i = 0
    app.boxWidth, app.boxHeight = 0.8*app.width, 0.1*app.height
    app.boxCoords = (app.width/2 -app.boxWidth/2,app.height/2 -app.boxHeight, 
                app.width/2 + app.boxWidth/2, app.height/2 + app.boxHeight)
    app.enteredText = ""
    #app.randomSen = nlp.pseudoRandomSentenceGenerator(nlp.dispSentence)
    #app.brokenSen = nlp.makeBrokenSentence(app.randomSen, 1)
    app.randomSen = app.brokenSen = "Press NEW to start!"
    app.dictionary = nlp.engWords
    app.suggestions = set()
    app.buttonList = []
    app.buttonList.append((20, 20, "light green", 40, "New"))
    app.buttonList.append((70, 20, "light blue", 40, "Hint"))
    app.buttonList.append((120, 20, "light pink", 40, "Skip"))
    app.buttonList.append((170, 20, "cyan", 40, "Hard\nMode"))
    app.buttonList.append((220, 20, "pink", 40, "Easy\nMode"))
    app.buttonList.append((270, 20, "blue", 40, "Dictionary"))
    app.suggestion = ["suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4"]
    app.options = []
    app.colors = ['light blue','cyan','light green','pink','#c48ee0',
                'beige','#cd757c','#cd8199','#c0cbff','#d76fb0',
                '#F78B74','#D0EDB4','#EDE9B4','#FF6F6F']
    app.autoCoords = (app.width/2-app.boxWidth/2,app.height/1.5-app.boxHeight, 
                app.width/2 + app.boxWidth/2, app.height/1.5 + app.boxHeight)
    app.gameOver, app.isNewGame = False, True
    app.timerDelay = 1000
    app.sptimer,app.timer, app.trackTime, app.startTimer = 0,60*app.timerDelay,0, False
    app.coltimer = 0
    app.answer = 'answer'
    app.optionSelected = None 
    app.guesses = []
    app.guess = None
    app.isHint = False
    app.hint = ''

    app.playAgain = False

    
def drawBG(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#639AE1")
    x0,y0,x1,y1 = 0.43*app.width, 20, 0.57*app.width, 60
    canvas.create_rectangle(x0,y0,x1,y1, fill = 'light green', width = 3)
    canvas.create_text((x0+x1)/2,(y0+y1)/2,text = f'Score: {app.score}')
    drawTimer(app, canvas)

def drawButton(app,canvas,x0, y0, col, size, label):
    x1, y1 = x0 + size, y0 + size 
    canvas.create_rectangle(x0-5,y0-5,x1-5,y1-5,fill = col)
    canvas.create_rectangle(x0,y0,x0 + size,y0+ size,fill = col)
    canvas.create_text((x0+x1)/2,(y0+y1)/2,text = label)

def inButton(app, x, y):
    for (x0,y0,col,size, label) in app.buttonList:
        if x0 <= x <= x0 + size and y0<= y <= y0 + size:
            if label == "New":
                app.isNewGame = True
                new(app)
                app.isNewGame = False
            elif label == "Hint":
                hint(app)
                app.isHint =  True
            elif label == "Hard\nMode":
                app.mode = 'hardMode'
                app.score = 0
                app.gameOver, app.isNewGame = False, True
                app.sptimer, app.timer = 0,60*app.timerDelay 
                app.trackTime, app.startTimer = 0, False
                new(app)
                app.randomSen = app.brokenSen = "Press NEW to start!"
            elif label == "Dictionary":
                helperDictionary(app)
            elif label == 'Easy\nMode':
                app.mode = 'gameMode'
                app.score = 0
                app.gameOver, app.isNewGame = False, True
                app.sptimer, app.timer = 0,60*app.timerDelay 
                app.trackTime, app.startTimer = 0, False
                new(app)
                app.randomSen = app.brokenSen = "Press NEW to start!"
            elif label == 'Skip':
                generateNewQ(app)

    return False

def drawAutocomplete(app, canvas):
    x0,y0, x1, y1 = app.autoCoords
    canvas.create_rectangle(x0,y0, x1, y1, fill = "White")
    for i in range(len(app.suggestion)):
        dy = abs(y0 - y1)/len(app.suggestion)
        newy0 = y0 + dy*i 
        newy1 = y0 + dy*(i+1)
        canvas.create_rectangle(x0,newy0, x1, newy1)
        canvas.create_text((x0+x1)/2, (newy0 + newy1)/2, text = app.suggestion[i],
                font = "Times 12")

def drawOptions(app, canvas):
    x, y, width, height = 0.1*app.width, 0.4*app.height, 0.4*app.width, 0.2*app.height
    k = -1
    getOptions(app, seed=9)
    for i in range(2):
        for j in range(2):
            font = "Times 14"
            k += 1
            w = 4
            x0, y0, x1, y1 = x + i*width, y + j*height, x + (i+1)*width, y + (j+1)*height
            col = random.choice(app.colors)
            col2 = 'black'
            font = "Times 14"
            if app.hint == app.suggestion[k] and app.isHint:
                col = 'black'
            canvas.create_rectangle(x0, y0, x1, y1, fill = col, width = w, outline = col2)
            canvas.create_text((x0+x1)/2,(y0+y1)/2, text = app.suggestion[k], font = font)
            if app.suggestion[k] == app.optionSelected:
                col2 = 'black'
                font = "Times 22 bold"
                w = 4
                canvas.create_rectangle(x0, y0, x1, y1, fill = col, width = w, outline = col2)
                canvas.create_text((x0+x1)/2,(y0+y1)/2, text = app.suggestion[k], font = font)
    x,y,r = app.width/2, 0.9*app.height, 20
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = "green")
    canvas.create_text(x,y, text = "✓", font = "Times 18")

def getOptions(app, seed):
    app.options = []
    for s in app.suggestions:
        col = random.choice(app.colors)
        app.options.append([s, col])

def new(app):
    generateNewQ(app)
    app.startTimer = True 
    app.timer = 60*app.timerDelay
    app.trackTime = 0
    app.isNewGame = False
    app.score = 0

def generateNewQ(app):
    app.randomSen = nlp.pseudoRandomSentenceGenerator(nlp.dispSentence)
    app.brokenSen, app.answer = nlp.makeBrokenSentence(app.randomSen, 1)
    app.answer = nlp.reformatWord(app.answer)
    temp = app.brokenSen.split(' ')
    new = ''
    for i in range(len(temp)):
        if i%6 == 0:
            new += '\n' + temp[i] + ' '
        else:
            new += temp[i] + ' '
    app.brokenSen = new.strip()
    #app.brokenSen = app.randomSen = "new random sentence"
    #app.answer = 'answer'
    app.optionSelected = None 
    app.isHint = False
    #app.guesses = nlp.autocomplete(app.brokenSen, 25)
    app.guesses = nlp.ezAutocomplete(app.brokenSen)
    #random.shuffle(app.guesses)
    app.guess = None
    #app.suggestion = nlp.optionAutocomplete(app.brokenSen, 20) 
    app.suggestion = nlp.ezAutocomplete(app.brokenSen)
    #random.shuffle(app.suggestion)
    while (app.answer.lower() in app.suggestion):
        app.suggestion.remove(app.answer)
    while len(app.suggestion) < 3:
        l = list(nlp.probDist.keys())
        app.suggestion.append(random.choice(l))
    app.suggestion = app.suggestion[0:3]
    app.suggestion += [app.answer]
    random.shuffle(app.suggestion)
    app.enteredText = ''

def hint(app):
    #removes one of the incorrect options
    if app.mode == 'hardMode':
        app.isHint = True 
        app.hint = app.answer[0]
    else:
        temp = "" 
        while temp == app.answer or temp == '':
            temp = random.choice(app.suggestion)
        app.isHint = True 
        app.hint = temp

def saveGameInfo(app):
    print("Saved!")

def helperDictionary(app):
    partial = app.getUserInput('Enter the first letter or first few letters!')
    L = []
    temp = set(app.dictionary.split(' '))
    for x in temp:
        if partial in x:
            if x.index(partial) == 0:
                L.append(x)
    L = L[:10]
    new = 'Here are some possibilities: \n'
    for x in L:
        new += x
        new += '\t'
    new = new.strip()
    app.showMessage(new)

   
def validateResult(app, answer, result):

    if app.mode == 'gameMode':
        answer = nlp.reformatWord(answer)
        if answer.lower() == result:
            app.showMessage('You win!')
            app.score += 1*len(app.brokenSen)//10
            generateNewQ(app)
        else:
            app.showMessage('The AI got you! Try again...')
    elif app.mode == 'hardMode':
        app.answer = nlp.reformatWord(app.answer)
        if app.answer.lower() in app.guess:
            app.showMessage('AI wins!')
            app.score -= 1*(len(app.brokenSen)//2)
            generateNewQ(app)
            app.enteredText = ''
        elif app.enteredText == app.answer.lower():
            app.showMessage('Perfect!')
            app.score += 1*len(app.brokenSen)
            generateNewQ(app)
            app.enteredText = ''
        else:
            app.showMessage('Try again...')
    if app.trackTime == 0:
        app.gameOver = True 
        #new(app) 
        app.showMessage('Play again!')

def isInOption(app, ex, ey):
    k = -1
    x, y, width, height = 0.1*app.width, 0.4*app.height, 0.4*app.width, 0.2*app.height
    for i in range(2):
        for j in range(2):
            k += 1
            x0, y0, x1, y1 = x + i*width, y + j*height, x + (i+1)*width, y + (j+1)*height
            if (x0<= ex<= x1) and (y0<= ey<=y1):
                app.optionSelected = app.suggestion[k]
                print(app.suggestion[k])
                return True 
    return False

def isInCheck(app, x, y):
    x0,y0,r = app.width/2, 0.9*app.height, 20
    return (x0-r<= x <= x0+r) and (y0-r <= y <= y0+r)

def drawTimer(app, canvas):
    r = 30
    x, y = app.width - 1.5*r, 1.5*r 
    canvas.create_oval(x-r,y-r, x+r, y+r, fill = "Blue")
    canvas.create_oval(x-r+1,y-r+1, x+r-1, y+r-1, fill = "White")
    t = app.timer//app.timerDelay - app.trackTime//app.timerDelay 
    if t <= 0:
        t = 0
        #app.gameOver = True 
    elif not app.startTimer:
        t = 0
    canvas.create_text(x,y, text = f"{t}", font = "Times 20") 

def drawNewGame(app, canvas):
    #draw pop up box that takes in user input regarding level of game etc 
    #draw 3,2,1 start
    for i in range(3,0,-1):
        x0, y0, x1, y1 = 0.4*app.width, 0.4*app.height, 0.6*app.width, 0.6*app.height
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'White', width = 5)
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = f'{i}')

def drawGameOver(app, canvas):
    #draw game over - display score
    canvas.create_rectangle(0.2*app.width, 0.2*app.height,0.8*app.width, 0.8*app.height, fill = 'grey')
    canvas.create_text(app.width/2, app.height/2, text = f'Your score was: {app.score}')
    #draw want to save game?
    #ask if want to play again
        #if yes, call drawNewGame(app, canvas)
    

def drawAreYouSure(app, canvas, message):
    x0, y0, x1, y1 = 0.4*app.width, 0.4*app.height, 0.6*app.width, 0.6*app.height
    canvas.create_rectangle(x0, y0, x1, y1, fill = "white", width = 5)
    canvas.create_text((x0+x1)/2, (y0 + 1.5*y1)/2, text = message)
    yx0, yy0, yx1, yy1 = (9/8)*x0, y0 + 0.4*(y1-y0), (11/8)*x0, y0 + 0.6*(y1-y0)
    canvas.create_rectangle(yx0, yy0, yx1, yy1, fill = "green", width = 3)
    canvas.create_text((yx0+yx1)/2, (yy0 + yy1)/2, text = 'YES')
    nx0, ny0, nx1, ny1 = (13/8)*x0, y0 + 0.4*(y1-y0), (15/8)*x0, y0 + 0.6*(y1-y0)
    canvas.create_rectangle(nx0, ny0, nx1, ny1, fill = 'red', width = 3)
    canvas.create_text((nx0+nx1)/2, (ny0+ny1)/2, text = 'NO')

def drawBox(app, canvas):
    x0,y0, x1, y1 = app.boxCoords
    canvas.create_rectangle(x0,y0, x1, y1, fill = "light blue")
    font = 'Courier 20 bold'
    canvas.create_text((x0+x1)/2, y0/2 + 20, text = app.brokenSen, 
                font = font)
    if not app.inBox:
        canvas.create_text((x0+x1)/2,(y1+y0)/2, text="Type here...", 
                    fill = "Blue", font = 'Courier 12 italic')
    else:
        canvas.create_text((x0+x1)/2,(y1+y0)/2, text= app.enteredText, 
                    fill = "black", font = 'Courier 14 bold')

################################################################
#GAMEOVER
################################################################

def gameOver_redrawAll(app, canvas):
    #drawGameOver(app, canvas)
    canvas.create_rectangle(0,0, app.width, app.height, fill = 'light blue')
    #canvas.create_rectangle(0.2*app.width, 0.2*app.height,0.8*app.width, 0.8*app.height, fill = 'light blue')
    font = 'Courier 18 bold'
    canvas.create_text(app.width/2, app.height/3, text = f'Your score was: {app.score}', font = font)
    if not app.playAgain:
        x0, y0, x1, y1 = 0.4*app.width, 0.45*app.height, 0.6*app.width, 0.55*app.height
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'light green', width = 3)
        font = 'Courier 16 italic'
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Play Again?')
    else:
        #easy mode
        x0, y0, x1, y1 = 0.35*app.width, 0.55*app.height, 0.45*app.width, 0.65*app.height
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'light green', width = 3)
        font = 'Courier 14 italic'
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Easy Mode?')
        #hard mode
        x0, y0, x1, y1 = 0.55*app.width, 0.55*app.height, 0.65*app.width, 0.65*app.height
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'light green', width = 3)
        font = 'Courier 14 italic'
        canvas.create_text((x0+x1)/2, (y0+y1)/2, text = 'Hard Mode?')


def gameOver_mousePressed(app, event):
    ex, ey = event.x, event.y 
    if app.playAgain:
        if (0.35*app.width <= ex <= 0.45*app.width) and (0.55*app.height <= ey <= 0.65*app.height):
            app.mode = 'gameMode'
            app.score = 0
            app.gameOver, app.isNewGame = False, True
            app.sptimer, app.timer = 0,30*app.timerDelay 
            app.trackTime, app.startTimer = 0, False
            new(app)
            app.randomSen = app.brokenSen = "Press NEW to start!"
            generateNewQ(app)
        elif (0.55*app.width <= ex <= 0.65*app.width) and (0.55*app.height <= ey <= 0.65*app.height):
            app.mode = 'hardMode'
            app.score = 0
            app.gameOver, app.isNewGame = False, True
            app.sptimer, app.timer = 0,60*app.timerDelay 
            app.trackTime, app.startTimer = 0, False
            new(app)
            app.randomSen = app.brokenSen = "Press NEW to start!"
            generateNewQ(app)
        app.playAgain = False
        app.gameOver = False
    else:
        if (0.4*app.width <= ex <= 0.6*app.width) and (0.45*app.height <= ey <= 0.55*app.height):
            app.playAgain = True 
    

################################################################
#HARDMODE
################################################################


def hardMode_redrawAll(app, canvas):
    drawBG(app, canvas)
    for (x0,y0,col,size, label) in app.buttonList:
        drawButton(app,canvas,x0, y0, col, size, label)
    #drawAutocomplete(app, canvas)
    drawBox(app, canvas)
    #drawOptions(app, canvas) 
    x,y,r = app.width/2, 0.9*app.height, 20
    canvas.create_oval(x-r,y-r,x+r,y+r, fill = "green")
    canvas.create_text(x,y, text = "✓", font = "Times 16")
    x0, y0, x1, y1 = app.boxCoords
    if app.guess != None:
        #canvas.create_rectangle(x0, y0+200, x1, y1+200, fill = random.choice(app.colors))
        new = ''
        for x in app.guess:
            new += x + ' , '
        new = new.strip()
        new = new[:len(new)-1]
        canvas.create_text(app.width/2,(y0+y1+200)/2, text = f'AI\'s guesses: {new}',font = "Times 20")

def hardMode_keyPressed(app, event):
    if (event.key == '0'):
        app.mode = 'helpMode'
    if app.inBox:
        if event.key == "Backspace":
            app.enteredText = app.enteredText[:len(app.enteredText) - 1]
        elif event.key == "Space":
            if app.enteredText != "" and app.enteredText[-1] != " ":
                app.enteredText += " "
        elif event.key == "Enter":
            app.inBox = False
            app.enteredText = ""
            saveGameInfo(app)
        elif event.key.isalpha():
            app.enteredText += event.key

def hardMode_mousePressed(app, event):
    x0, y0, x1, y1 = app.boxCoords
    
    if x0 <= event.x <= x1 and y0 <= event.y <= y1:
        app.inBox = True 
    else:
        app.inBox = False
    inButton(app, event.x, event.y)
    if isInCheck(app, event.x, event.y):
        name = app.getUserInput('Are you Sure?')
        if (name == None):
            app.message = 'You canceled!'
        elif name.lower() == 'yes' or name.lower() == 'y':
            #app.showMessage('You entered: ' + name)
            if app.enteredText != "":
                app.guess = app.guesses[:3]
                app.guesses = app.guesses[3:]
                print("guess is", app.guess, app.guesses)
                validateResult(app, app.guess, app.enteredText)
                if len(app.guesses) == 0:
                    app.showMessage(f'Round TIED!\n The answer was {app.answer}')
                    generateNewQ(app)
                    app.enteredText = ''

def hardMode_timerFired(app):
    if app.isHint and app.hint != None:
        L = []
        L.append(f'The word has {len(app.answer)} letters.')
        L.append(f'The word starts with {app.answer[0].upper()}.')
        temp = nlp.getTags([app.answer])[0][1]
        if temp in nlp.tagDict:
            t = nlp.tagDict[temp]
            L.append(f'The word is a {t.upper()}.')
        app.hint = random.choice(L)
        app.showMessage(app.hint)
        app.hint = None
        app.isHint = False
    if app.gameOver:
        app.mode = 'gameOver'
    t = app.timer//app.timerDelay - app.trackTime//app.timerDelay 
    if t <= 0:
        t = 0
        app.gameOver = True 
    if app.timer >= app.trackTime:
        app.trackTime += app.timerDelay 
    app.coltimer += 1


runApp(width=800, height=600) 