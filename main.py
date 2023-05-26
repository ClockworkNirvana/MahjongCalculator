import kivy
from mahjong import Mahjong
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import functools
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)
def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))
  
class SettingsScreen(Screen):
  def submit(self):
    for k in range(0,4):
      a = 'n'+str(k)+'.text'
      b = 'name'+str(k)+'.text'
      rsetattr(self.manager.get_screen('MahjongGrid'), a, rgetattr(self, b))
      a = 'w'+str(k)+'.text'
      rsetattr(self.manager.get_screen('MahjongGrid'), a, rgetattr(self, b))
    for k in range(0,5):
      a = 's'+str(k)+'.text'
      b = 'scenario'+str(k)+'.text'
      rsetattr(self.manager.get_screen('MahjongGrid'), a, rgetattr(self, b))
    self.manager.get_screen('MahjongGrid').tai_value.text = str(self.tai_value.text)
    self.manager.transition = SlideTransition(direction='left', duration=0.25)
    self.manager.current = 'MahjongGrid'

class MahjongGrid(Screen):
  def startup(self):
    self.m = Mahjong(int(self.tai_value.text), [int(self.s0.text), int(self.s1.text), int(self.s2.text), int(self.s3.text), int(self.s4.text)])
    self.names = [self.n0.text, self.n1.text, self.n2.text, self.n3.text]
    self.w = None
    self.l = None
    self.t = None
    self.tai = None
  def winner(self, w):
    self.w = int(w)
    for k in range(0,3):
      a = 'l' + str(k) + '.text'
      if k < w:
        rsetattr(self, a, self.names[k])
      if k >= w:
        rsetattr(self, a, self.names[k+1])
    self.l3.text = "All"
  def loser(self, l):
    if l is not True:
      if l >= self.w:
        l+=1
      self.l = int(l)
    else:
      self.l = l
  def type(self, t):
    self.t = int(t)
    if t in [1, 3, 4, 5]:
      for k in range(0,4):
        a = 'l'+str(k)+'.state'
        rsetattr(self, a, 'normal')
      self.l3.state = 'down'
      self.l = True
      if t in [1, 4]:
        self.tai2.state = 'down'
        self.tai = 2
      else:
        self.tai1.state = 'down'
        self.tai = 1
    if t == 2:
      self.tai1.state = 'down'
      self.tai = 1
  def tai_set(self, t):
    self.tai = int(t)
  def confirm(self):
    match self.t:
      case 0:
        self.m.hu(self.w, self.tai, self.l)
      case 1 | 3 | 4 | 5:
        self.m.yaodao(self.w, self.t-1)
      case 2:
        self.m.yaodao_1(self.w, self.l)
      case 6:
        self.m.danger(self.w, self.tai, self.l)
    for k in range(0,4):
      a = 'm'+str(k)+'.text'
      rsetattr(self, a, str(self.m.money[k]))
      a = 'w'+str(k)+'.state'
      rsetattr(self, a, 'normal')
      a = 'l'+str(k)+'.state'
      rsetattr(self, a, 'normal')
      a = 'l'+str(k)+'.text'
      rsetattr(self, a, '')
    for k in range(0,7):
      a = 't'+str(k)+'.state'
      rsetattr(self, a, 'normal')
    for k in range(1,6):
      a = 'tai'+str(k)+'.state'
      rsetattr(self, a, 'normal')   
    self.w = None
    self.l = None
    self.tai = None
    self.t = None
    
class MahjongApp(App): # <- Main Class
  def build(self):
    
    self.screen_manager = ScreenManager()
    self.screen_manager.add_widget(SettingsScreen(name='SettingsScreen'))
    self.screen_manager.add_widget(MahjongGrid(name='MahjongGrid'))
    
    return self.screen_manager


if __name__ == "__main__":
    MahjongApp().run()