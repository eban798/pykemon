
import pygame, os, sys, time, random
from pygame.locals import *

           #R    G    B
BLUE =     (0,   0,   255)
GREEN =    (0,   128, 0)
PURPLE =   (128, 0,   128)
RED =      (255, 0,   0)
YELLOW =   (255, 255, 0)
NAVYBLUE = (0,   0,   128)
WHITE =    (255, 255, 255)
BLACK =    (0,   0,   0)

def PokemonStrip(targetFile):
  with open(targetFile, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    targetList = []
    while i<11:
      targetList.append(fileList[i])
      i += 1
    f.close()
  return targetList
  
def MoveStrip(pokemonList, moveNumber):
  moveName = pokemonList[moveNumber+3].lower() + '.txt' 
  with open(moveName, 'r') as f:
    fileString = f.read()
    fileList = fileString.split('\n')
    i = 0
    moveList = []
    while i<6:
      moveList.append(fileList[i])
      i += 1
    f.close()
  return moveList
  
def PlayerChoice(targetFile):
  pPokemon = []
  pPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  pAttackList = []
  while moveNumber<5:
    pAttackList.append(MoveStrip(pPokemon, moveNumber))
    moveNumber += 1
  return [pPokemon, pAttackList]

def ComputerChoice(choices):
  choice = random.randint(0,1)
  targetFile = choices[choice].lower() + '.txt'
  cPokemon = []
  cPokemon = PokemonStrip(targetFile)
  moveNumber = 1
  cAttackList = []
  while moveNumber<5:
    cAttackList.append(MoveStrip(cPokemon, moveNumber))
    moveNumber += 1
  return [cPokemon, cAttackList]

def Battle(pPokemon, pMoveList, cPokemon, cMoveList):
  pStats = [1, 1]
  cStats = [1, 1]
  fainted = False
  while fainted != True:
    pMove = pMoveSelect(pMoveList)
    cMove = cMoveSelect(cMoveList)
    ClearTerminal()
    if pPokemon[2] < cPokemon[2]:
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
      time.sleep(.5)
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
      time.sleep(.5)
    else:
      cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats)
      if pPokemon[1] <= 0:
        fainted = True
        winner = "Computer"
        break
      time.sleep(.5)
      pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats)
      if cPokemon[1] <= 0:
        fainted = True
        winner = "Player"
        break
      time.sleep(.5)
    print (pPokemon[0] + "'s health is:", pPokemon[1])
    print (cPokemon[0] + "'s health is:", cPokemon[1])
  print ("Ther winner is: ") + winner
  
def pAttackSequence(pPokemon, pMove, cPokemon, pStats, cStats):
  print (pPokemon[0] + " used " + pMove[5] + ".")
  print ("")
  mode = pMove[0]
  if mode == "1":
    cPokemon = DamageMod(pPokemon, pMove, cPokemon, pStats, cStats)
  elif mode == "21":
    pStats = StatMod(pMove, pStats, pStats)
  elif mode == "22":
    cStats = StatMod(pMove, pStats, cStats)

def cAttackSequence(cPokemon, cMove, pPokemon, cStats, pStats):
  print (cPokemon[0] + " used " + cMove[5] + ".")
  print ("")
  mode = cMove[0]
  if mode == "1":
    pPokemon = DamageMod(cPokemon, cMove, pPokemon, cStats, pStats)
  elif mode == "21":
    cStats = StatMod(cMove, cStats, cStats)
  elif mode == "22":
    pStats = StatMod(cMove, cStats, pStats)
    
def DamageMod(attacker, attack, target, attackerStats, targetStats):
  typeAdvantage = AdvantageCalc(attack, target)
  DMG = int(attack[2])
  aATK = StatIndex(attackerStats, "A")
  tDEF = StatIndex(targetStats, "D")
  effect = DMG*(aATK/tDEF)*typeAdvantage
  target[1] = int(target[1]) - effect
  print (attacker[0] + " dealt", effect, "damage!")
  print ("")
  return target
  
def StatMod(move, attackerStats, targetStats):
  targetStat = move[4]
  effect = move[3]
  if targetStat == "A":
    if effect == "-":
      targetStats[0] -= 1
      return targetStats
    else:
      targetStats[0] += 1
      return targetStats
  else:
    if effect == "-":
      targetStats[0] -= 1
      return targetStats
    else:
      targetStats[0] += 1
      return targetStats

def StatIndex(stats, statType):
  statIndex = [(1.0/4),(2.0/7),(1.0/3),(2.0/5),(1.0/2),(2.0/3), 1, 1.5, 2, 2.5, 3, 3.5, 4]
  if statType == "A":
    statInQuestion = stats[0]
  else:
    statInQuestion = stats[1]
  trueStat = statIndex[statInQuestion+5]
  return trueStat

def AdvantageCalc(attack, target):
  combo = attack[1] + target[3]
  if combo == "FG":
    typeAdvantage = 2
  elif combo == "FW":
    typeAdvantage = .5
  elif combo == "FN":
    typeAdvantage = 1
  elif combo == "WF":
    typeAdvantage = 2
  elif combo == "WG":
    typeAdvantage = .5
  elif combo == "WN":
    typeAdvantage = 1
  elif combo == "GF":
    typeAdvantage = .5
  elif combo == "GW":
    typeAdvantage = 2
  elif combo == "GN":
    typeAdvantage = 1
  elif combo == "NF":
    typeAdvantage = 1
  elif combo == "NW":
    typeAdvantage = 1
  elif combo == "NG":
    typeAdvantage = 1
  return typeAdvantage
  
def cMoveSelect(cMoveList):
  cMove = cMoveList[random.randint(0,3)]
  return cMove
  
def pMoveSelect(pMoveList):
  print ("What will " + pPokemon[0] + " do?")
  time.sleep(1)
  print ("Your choices are... ")
  PrintMoves(pMoveList)
  pMoveChoice = raw_input("")
  tracker = 0
  for x in pMoveList:
    if x[5] == pMoveChoice:
      pMove = pMoveList[tracker]
      break
    else:
      tracker += 1
  return pMove

def PrintMoves(moveList):
  for x in moveList:
    print (x[5])
  print ("")

def PrintChoices(choices):
  for x in choices:
    print (x)
  print ("")

def ClearTerminal():
  os.system('cls' if os.name=='nt' else 'clear')

def drawText(text, font, surface, x, y):
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  i = 0
  for char in textLine1:
    realLine1 = textLine1[:i]
    textobj1 = font.render(realLine1,1,WHITE)
    textrect1 = textobj1.get_rect()
    textrect1.topleft = (x,y)
    surface.blit(textobj1,textrect1)
    pygame.display.update()
    i += 1
    time.sleep(0.1)
  j = 0
  for char in textLine2:
    realLine2 = textLine2[:j]
    textobj2 = font.render(textLine2,1,WHITE)
    textrect2 = textobj2.get_rect()
    textrect2.topleft = (x,y+10)
    surface.blit(textobj2,textrect2)
    pygame.display.update()
    j += 1
    time.sleep(0.1)
  
class Button():
  def assignImage(self, picture):
    self.rect = picture.get_rect()
  def setCoords(self, x,y):
    self.rect.topleft = x,y
  def drawButton(self, picture):
    DISPLAYSURF.blit(picture, self.rect()
  def pressed(self,mouse):
    if self.rect.collidepoint(mouse) == True:
      return True

class HealthBar():
  def init(self,x,y):
    self.position = x,y
    self.height = 10
    self.negWidth = 75
    self.poswidth = 75
  def drawRects(self):
    #(x,y,width,height)
    pygame.draw.rect(DISPLAYSURF, RED, (self.position[0], self.position[1], self.height, self.width)
    pygame.draw.rect(DISPLAYSURF, GREEN, (self.position[0], self.position[1], self.height, self.width)
    pygame.display.update()
  def.updateButton(self, pokemonList)
    maxHealth = pokemonList[8]
    currentHealth = pokemonList[1]
    
    
def BulbImages():
  fileNames = ["bulbasaurFront.png","bulbasaurBack.png"]
  bulbArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    bulbArray.append(newImg)
  return bulbArray
  
def CharImages():
  fileNames = ["charmanderFront.png","charmanderBack.png"]
  charArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    charArray.append(newImg)
  return charArray
  
def SquirtImages():
  fileNames = ["squirtleFront.png","squirtleBack.png"]
  squirtArray = []
  for x in fileNames:
    newImg = pygame.image.load(x)
    squirtArray.append(newImg)
  return squirtArray

if __name__ == '__main__':
  pygame.init()
  fpsClock = pygame.time.Clock()
  DISPLAYSURF = pygame.display.set_mode((400, 600))
  pygame.display.set_caption('Pykemon')
  FPS = 15
  font = pygame.font.SysFont(None, 20)
  
  bulbImages = BulbImages()
  bulbFront = bulbImages[0]
  bulbBack = bulbImages[1]
  squirtImages = SquirtImages()
  squirtFront = squirtImages[0]
  squirtBack = squirtImages[1]
  charImages = CharImages()
  charFront = charImages[0]
  charBack = charImages[1]
  
  message = "Choose your Pokemon!"
  drawText(message, font, DISPLAYSURF, int(100), int(100))
  
  charButton = Button()
  charButton.assignImage(charFront)
  charButton.setCoords(0, 200)
  squirtButton = Button()
  squirtButton.assignImage(squirtFront)
  squirtButton.setCoords(200, 200)
  bulbButton = Button()
  bulbButton.assignImage(bulbFront)
  bulbButton.setCoords(100, 400)
  
  herp = 1
  while herp == 1:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      elif event.type == MOUSEBUTTONDOWN:
        mouse = pygame.mouse.get_pos()
        if charButton.pressed(mouse) == True:
          choice = "Charmander"
          herp = 0
        if squirtButton.pressed(mouse) == True:
          choice = "Squirtle"
          herp = 0
        if bulbButton.pressed(mouse) == True:
          choice = "Bulbasaur"
          herp = 0
          
    charButton.drawButton(charFront)
    squirtButton.drawButton(squirtFront)
    bulbButton.drawButton(bulbFront)
    pygame.display.update()
  
  choices = ['Charmander', 'Squirtle', 'Bulbasaur']
#  print 'Your choices are: '
#  PrintChoices(choices)
#  choice = raw_input('Which Pokemon will you choose?... ')
  targetFile = choice.lower() + '.txt'
  choices.remove(choice)
 
  playerChoice = PlayerChoice(targetFile)
  pPokemon = playerChoice[0]
  pMoveList = playerChoice[1]
  ClearTerminal()
  print pPokemon[0].upper() + "! I choose you!"
  print ""
  time.sleep(.5)
  computerChoice = ComputerChoice(choices)
  cPokemon = computerChoice[0]
  cMoveList = computerChoice[1]
  print "Computer sent out " + cPokemon[0]
  print ""
  
  Battle(pPokemon, pMoveList, cPokemon, cMoveList)

  
  
