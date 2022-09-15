from tkinter import *
import time
import random
from threading import Thread
from threading import Event
from turtle import update

mainWindow = Tk()
rootFrame = Frame(mainWindow)
rootFrame['borderwidth'] = 5
rootFrame['relief'] = 'sunken'

def createWindow():
    mainWindow.title("Spelling Bee Generator")
    mainWindow.geometry("800x600")

def createMainMenu():
    print("Generating Main Menu...")
    # Text variables:
    mainMenuTitleText = "Spelling Bee Generator"
    mainMenuAuthorText = "Gateau, 2022 GateauDaze@GitHub.com"

    # Row 0:
    mainMenuTitleButtonFrame = Frame(rootFrame)
    mainMenuTitleLabel = Label(mainMenuTitleButtonFrame, text=mainMenuTitleText, font=('Helvetica', 24))
    mainMenuNextButton = Button(mainMenuTitleButtonFrame, text="Start", font=('Helvetica', 14), command=mainMenuStartButtonCallback)
    # display Title and Button underneath...
    mainMenuTitleLabel.pack()
    mainMenuNextButton.pack()
    mainMenuTitleButtonFrame.pack()

    # Row 1:
    # Author information...
    mainMenuAuthorLabel = Label(rootFrame, text=mainMenuAuthorText)
    mainMenuAuthorLabel.pack()

    # Pack widgets
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)


def createGameMenu():
    print("Creating a game window...")
    global currentTeam
    currentTeam = 'none'
    global maximumScore
    maximumScore = IntVar()

    # Row 0:
    gameMenuTeamWordCountFrame = Frame(rootFrame)
    gameMenuTeamText = "Select the starting team"
    gameMenuTeamLabel = Label(gameMenuTeamWordCountFrame, text=gameMenuTeamText, font=('Helvetica', 24))
    gameMenuTeamLabel.grid(column=0, row=0)
    gameMenuWordCountScaleFrame = Frame(gameMenuTeamWordCountFrame)
    gameMenuWordCountLabel = Label(gameMenuWordCountScaleFrame, text="Word count: ", font=('Helvetica', 14))
    gameMenuWordCountScale = Scale(gameMenuWordCountScaleFrame, from_=1, to=100, variable = maximumScore, orient=HORIZONTAL, length=200)
    gameMenuWordCountLabel.grid(column=0, row=0)
    gameMenuWordCountScale.grid(column=1, row=0)
    gameMenuWordCountScaleFrame.grid(column=0, row=1)
    gameMenuTeamWordCountFrame.pack()

    # Row 1:
    gameMenuTeamButtonFrame = Frame(rootFrame)
    gameMenuTeamAButton = Button(gameMenuTeamButtonFrame, text="Team A", font=('Helvetica', 14), command=gameMenuTeamAButtonCallback)
    gameMenuTeamBButton = Button(gameMenuTeamButtonFrame, text="Team B", font=('Helvetica', 14), command=gameMenuTeamBButtonCallback)
    gameMenuMainMenuButton = Button(gameMenuTeamButtonFrame, text="Main Menu", font=('Helvetica', 14), command=gameMenuMainMenuButtonCallback)
    gameMenuTeamAButton.grid(column=0, row=0)
    gameMenuMainMenuButton.grid(column=1, row=0)
    gameMenuTeamBButton.grid(column=2, row=0)
    gameMenuTeamButtonFrame.pack()

    # Pack widgets
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)

def createTeamMenu():
    tkTeamMenuTimer = Frame()

    global gameTimer
    gameTimer = 3
    # Row 0:
    teamAMenuAlertCountdownFrame = Frame(rootFrame)
    teamAMenuAlertText = "Team " +currentTeam +"'s Turn starts in..."
    teamAMenuAlertLabel = Label(teamAMenuAlertCountdownFrame, text=teamAMenuAlertText, font=('Helvetica', 14))
    teamAMenuCountdownLabel = Label(teamAMenuAlertCountdownFrame, text=str(gameTimer), font=('Helvetica', 48))
    teamAMenuAlertLabel.grid(column=0, row=0)
    teamAMenuCountdownLabel.grid(column=0, row=1)
    teamAMenuAlertCountdownFrame.pack()

    # Pack widgets
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)

    # reset score...
    global teamAScore
    teamAScore = 0
    global teamBScore
    teamBScore = 0
    
    # create word list
    filenameA = "testWordList1.txt"
    global wordList
    wordList = open(filenameA).read().splitlines()
    random.shuffle(wordList) # shuffle the words
    # number of words iterated so far...
    
    global wordCounter
    wordCounter = 0
    
    global maximumScore # number of words to iterate up to...
    if len(wordList) < maximumScore.get(): # if current word list is smaller than the maximum point specified in game setup menu...
        maximumScore.set(len(wordList)) # adjust the maximum score to the length of the available number of words

    # countdown before game starts...
    countdownLabel(tkTeamMenuTimer, gameTimer, teamAMenuCountdownLabel)
    tkTeamMenuTimer.after(gameTimer*1000, destroyMainWindowWidgets)
    tkTeamMenuTimer.after(gameTimer*1000, createInGameMenu)
    

def createInGameMenu():
    print("Team "+currentTeam+"'s turn...")
    tkIngameTimer = Frame()
    global wordTimer
    wordTimer = 10

    global inGameMenuFrame
    inGameMenuFrame = Frame(rootFrame)

    # Row 0:
    inGameMenuWordFrame = Frame(inGameMenuFrame)
    inGameMenuWordGuideText = "Team "+ currentTeam +"'s word is..."
    inGameMenuWordGuideLabel = Label(inGameMenuWordFrame, text=inGameMenuWordGuideText, font=('Helvetica', 14))
    inGameMenuWordToGuessText = "Sample"
    global inGameMenuWordToGuessLabel
    inGameMenuWordToGuessLabel = Label(inGameMenuWordFrame, text=inGameMenuWordToGuessText, font=('Helvetica', 48))
    inGameMenuTimerFrame = Frame(inGameMenuFrame)
    inGameMenuRemainingTimeLabel = Label(inGameMenuTimerFrame, text="Remaining Time: ", font=('Helvetica', 14))
    global inGameMenuWordTimerLabel
    inGameMenuWordTimerLabel = Label(inGameMenuTimerFrame, text=str(wordTimer), font=('Helvetica', 14))
    inGameMenuRemainingTimeLabel.grid(column=0, row=0)
    inGameMenuWordTimerLabel.grid(column=1,row=0)
    inGameMenuWordGuideLabel.grid(column=0, row=0)
    inGameMenuWordToGuessLabel.grid(column=0, row=1)
    inGameMenuTimerFrame.grid(column=0, row=1)
    inGameMenuWordFrame.grid(column=0, row=0)

    # Row 1:

    inGameMenuButtonFrame = Frame(inGameMenuFrame)
    inGameMenuCorrectButton = Button(inGameMenuButtonFrame, text="Correct!", font=('Helvetica', 14), command=lambda:inGameMenuCorrectButtonCallback(tkIngameTimer))
    inGameMenuCorrectButton.grid(column=0, row=0)
    inGameMenuButtonFrame.grid(column=0, row=2)

    inGameMenuFrame.pack()
    
    # Pack widgets
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)

    # start game logic here
    countdownLabel(tkIngameTimer, wordTimer, inGameMenuWordTimerLabel)
    tkIngameTimer.after(wordTimer*1000, ingameCountdownComplete)

def createSwitchSideMenu():
    tkSwitchSideTimer = Frame()
    switchTeamTimer = 3
    switchSideMenuFrame = Frame(rootFrame)
    switchSideText = "Team " +currentTeam +"'s Turn starts in..."
    switchSideTeamLabel = Label(switchSideMenuFrame, text=switchSideText, font=('Helvetica', 14))
    switchSideCountdownLabel = Label(switchSideMenuFrame, text=str(switchTeamTimer), font=('Helvetica', 48))
    switchSideTeamLabel.grid(column=0, row=0)
    switchSideCountdownLabel.grid(column=0, row=1)
    switchSideMenuFrame.pack()
  
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)

    # countdown before game starts...
    print("Switch team countdown in: " +str(switchTeamTimer))
    countdownLabel(tkSwitchSideTimer, switchTeamTimer, switchSideCountdownLabel)
    tkSwitchSideTimer.after(switchTeamTimer*1000, destroyMainWindowWidgets)
    tkSwitchSideTimer.after(switchTeamTimer*1000, createInGameMenu)

def createResultMenu():
    print("Creating results page...")
    resultMenuFrame = Frame(rootFrame)

    # Row 0:
    resultMenuScoreFrame = Frame(resultMenuFrame)
    resultMenuTeamAScoreText = "Team A Score: " + str(teamAScore) +"/"+str(wordCounter)
    resultMenuTeamAScoreLabel = Label(resultMenuScoreFrame, text=resultMenuTeamAScoreText, font=('Helvetica', 14))
    resultMenuTeamBScoreText = "Team B Score: " + str(teamBScore) + "/" + str(wordCounter)
    resultMenuTeamBScoreLabel = Label(resultMenuScoreFrame, text=resultMenuTeamBScoreText, font=('Helvetica', 14))

    resultMenuTeamAScoreLabel.grid(column=0, row=0)
    resultMenuTeamBScoreLabel.grid(column=0, row=1)
    resultMenuScoreFrame.grid(column=0, row=0)
    # Row 1:
    # Return to Main Menu
    resultMenuToMainMenuFrame = Frame(resultMenuFrame)
    resultMenuToMainMenuButton = Button(resultMenuToMainMenuFrame, text="To Main Menu", font=('Helvetica', 14), command=gameMenuMainMenuButtonCallback)
    resultMenuToMainMenuButton.pack()
    resultMenuToMainMenuFrame.grid(column=0, row=1)
    resultMenuFrame.pack()

    # Pack widgets
    rootFrame.pack(ipadx=5, ipady=5, anchor=CENTER, expand=True)
    

# Functions for window control
def destroyMainWindowWidgets():
    print("Destroying all widgets in screen...")
    widgetList = rootFrame.pack_slaves()
    for widgets in widgetList:
        widgets.pack_forget()

def countdownLabel(timerObject, remainingTime, updateLabel):
    print("Remaining time: " + str(remainingTime))
    updateLabel.configure(text=str(remainingTime))
    updateLabel.update()
    if remainingTime != 0:
        print("Countdown Remaining Time: " + str(remainingTime))
        remainingTime -=1
        timerObject.after(1000, lambda:countdownLabel(timerObject, remainingTime, updateLabel))
    else:
        print("Countdown complete")
        timerObject.destroy()

def switchTeam():
    global currentTeam
    if currentTeam == 'A':
        currentTeam = 'B'
    elif currentTeam == 'B':
        currentTeam = 'A'

def ingameCountdownComplete():
    switchTeam()
    destroyMainWindowWidgets()
    createSwitchSideMenu()

def inGameWordCountdown(remainingTime, wordLabel):
    print("do something")

def checkGameOver():
    if teamAScore == maximumScore.get() or wordCounter == len(wordList) or teamBScore == maximumScore.get():
        print("Game Over")
        return True
    else:
        print("Keep going")
        return False

# Callback for Main Menu:
def mainMenuStartButtonCallback():
    print("Main menu start button pressed...")
    destroyMainWindowWidgets()
    createGameMenu()

# Callback for Team A Button in Game Menu:
def gameMenuTeamAButtonCallback():
    print("Team A Button pressed...")
    destroyMainWindowWidgets()
    global currentTeam
    currentTeam = 'A'
    createTeamMenu()

# Callback for Team B Button in Game Menu:
def gameMenuTeamBButtonCallback():
    print("Team B Button pressed...")
    destroyMainWindowWidgets()
    global currentTeam
    currentTeam = 'B'
    createTeamMenu()

# Callback for 'To Main Menu' Button in Game Menu: 
def gameMenuMainMenuButtonCallback():
    print("Going back to main menu...")
    destroyMainWindowWidgets()
    createMainMenu()

# Callback for 'Correct Button' in 'inGameMenu':
def inGameMenuCorrectButtonCallback(timerObject):
    print("Team " + currentTeam + " correctly guessed the word")
    timerObject.destroy()
    global inGameMenuWordToGuessLabel
    global teamAScore
    global teamBScore
    if currentTeam == 'A':
        teamAScore += 1
    elif currentTeam == 'B':
        teamBScore += 1
    global wordCounter
    wordCounter += 1
    print("Current word count: " +str(wordCounter))
    print("Current Team A score: " + str(teamAScore))
    print("Current Team B score: " + str(teamBScore))
    gameOverState = checkGameOver()
    if gameOverState == True:
        destroyMainWindowWidgets()
        createResultMenu()
    elif gameOverState == False:
        destroyMainWindowWidgets()
        createInGameMenu()

# Below is main...
print("Generating Window...")
createWindow() # generate window
createMainMenu() # generate the main menu
mainWindow.mainloop()