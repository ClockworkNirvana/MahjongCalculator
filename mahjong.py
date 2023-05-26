# players is player names
# money is next gain/loss of each player
# scenarios is tai equivalent payout scenarios
class Mahjong():
  def __init__(self, tai, payout_scenarios=[2,1,1,2,1]):
    self.money = [0, 0, 0, 0]
    self.tai = tai
    self.scenarios = []
    for k in payout_scenarios:
      self.scenarios.append(int(k))
        
  # hu is for winning scenarios, takes in index of winning player, how many tai they won and who threw the winning tile
    
  def hu(self, winner, doubler, loser):
    self.money[winner] += 4*self.tai*(2**(doubler-1))
    for i in [x for x in range(0,4) if x != winner]:
      self.money[i] -= self.tai*(2**(doubler-1))
    if loser is True:
      for i in [x for x in range(0,4) if x != winner]:
        self.money[i] -= self.tai*(2**(doubler-1))
      self.money[winner] += 2*self.tai*(2**(doubler-1))
    else:
      self.money[loser] -= self.tai*(2**(doubler-1))
    
  # yaodao is for instant payout scenarios according to the following list with default values in brackets
  # 0: Gang, concealed ZiMo (2 tai eqi)
  # 1: Gang, from Pong (1 tai eqi, thrower x 2)
  # 2: Gang, exposed ZiMo (1 tai eqi)
  # 3: Flower (2 tai eqi)
  # 4: Animal (1 tai eqi)
    
  def yaodao(self, winner, type):
    self.money[winner] += 3*self.tai*(2**(self.scenarios[type]-1))
    for i in [x for x in range(0,4) if x != winner]:
      self.money[i] -= self.tai*(2**(self.scenarios[type]-1))
  def yaodao_1(self, winner, loser):
    self.money[winner] += 4*self.tai*(2**(self.scenarios[1]-1))
    for i in [x for x in range(0,4) if x != winner]:
      self.money[i] -= self.tai*(2**(self.scenarios[1]-1))
    self.money[loser] -= self.tai*(2**(self.scenarios[1]-1))

  # danger is when one party throws out a tile thats "dangerous"
  def danger(self, winner, doubler, loser):
    self.money[winner] += 4*self.tai*(2**(doubler-1))
    self.money[loser] -= 4*self.tai*(2**(doubler-1))