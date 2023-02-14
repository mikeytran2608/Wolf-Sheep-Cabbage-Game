from dataclasses import dataclass
import sys
from enum import Enum
from collections import namedtuple
from functools import partial


def switch(case):


# case 1
  if case == 1: 

    class Game:
        locations:tuple = ('nongdan', 'de', 'soi', 'cucai')
        nongdanLoc:str = '1'
        deLoc:str = '1'
        soiLoc:str = '1'
        cucaiLoc:str = '1'
        initial:tuple = ('1', '1', '1', '1')
        endgame:tuple = ('2', '2', '2', '2')
        score:int = 0


        def currentStatus(self):
            print("Luật chơi\n Tại bến sông nọ có bắp cải, sói và dê muốn bác lái đò chở qua sông. \nBiết rằng tại một thời điểm thuyền của bác lái đò chỉ chở tối đa được 2 khách. \nNếu sói và dê đứng riêng với nhau (không có mặt bác lái đò và bắp cải) thì sói sẽ ăn thịt dê.\n Nếu dê và bắp cải đứng riêng với nhau (không có mặt bác lái đò và sói) thì dê sẽ ăn bắp cả")
            print("\nVị trí hiện tại \nnongdan, de, soi, cucai")
            self.current = (self.nongdanLoc, self.deLoc, self.soiLoc, self.cucaiLoc)
            print(self.current)

        def checkStatus(self):
            if self.deLoc == self.soiLoc and (self.nongdanLoc != self.soiLoc or self.nongdanLoc != self.deLoc):
                print("Sói ăn Dê !")
                print("Game over!")
                print(f"Điểm của bạn là {self.score}")
                sys.exit()

            if self.deLoc == self.cucaiLoc and (self.nongdanLoc != self.deLoc or self.nongdanLoc != self.cucaiLoc):
                print("Dê ăn Củ Cải!")
                print("Game over!")
                print(f"Điểm của bạn là {self.score}")
                sys.exit()

        def promptActions(self):
            print("Chọn nhân vật")
            action = input("None\nde\nsoi\ncucai\nhotro\n(Or type 'exit' to quit)\nChọn nhân vật: ")
            action = action.lower()
            if action == "none": self.takeNone()
            elif action == "de": self.takede()
            elif action == "soi": self.takesoi()
            elif action == "cucai": self.takecucai()
            elif action == "exit": sys.exit()
            else:
                print(f"{action} is not a valid action")
                self.promptActions()


        def takeNone(self):
            if self.nongdanLoc == '1':
                self.nongdanLoc = '2'
            if self.nongdanLoc == '2':
                self.nongdanLoc = '1'
            return self.nongdanLoc

        def takede(self):
            if self.deLoc == '1' and self.nongdanLoc == '1':
                self.deLoc = '2'
                self.nongdanLoc = '2'
            elif self.deLoc == '2' and self.nongdanLoc == '2':
                self.deLoc = '1'
                self.nongdanLoc = '1'
            else:
                print("Không thể chọn Dê. Nông dân và Dê đang ở khác sông với nhau.")

        def takesoi(self):
            if self.soiLoc == '1' and self.nongdanLoc == '1':
                self.soiLoc = '2'
                self.nongdanLoc = '2'
            elif self.soiLoc == '2' and self.nongdanLoc == '2':
                self.soiLoc = '1'
                self.nongdanLoc = '1'
            else:
                print("Không thể chọn Sói. Nông dân và Sói đang ở khác sông với nhau.")

        def takecucai(self):
            if self.cucaiLoc == '1' and self.nongdanLoc == '1':
                self.cucaiLoc = '2'
                self.nongdanLoc = '2'
            elif self.cucaiLoc == '2' and self.nongdanLoc == '2':
                self.cucaiLoc = '1'
                self.nongdanLoc = '1'
            else:
                print("Không thể chọn Củ Cải. Nông dân và Củ cải đang ở khác sông với nhau.")
      
        def play(self):
            self.current = (self.nongdanLoc, self.deLoc, self.soiLoc, self.cucaiLoc)
            while (self.nongdanLoc, self.deLoc, self.soiLoc, self.cucaiLoc) != self.endgame:
                self.currentStatus()
                self.checkStatus()
                self.promptActions()
          #self.computerPlay()
                self.score += 1
            print("Chúc mừng bạn đã hoàn thành trò chơi!")
            print(f"Điểm của bạn là {self.score}")

    if __name__ == '__main__':
        g = Game()
        g.play()

  elif case == 2: 
    
    class WGC_Node:
        incompatibilities = [
          ["cucai", "de", "soi"],
          ["de", "soi"],
          ["cucai", "de"]
        ]

        def __init__(self, west=["soi", "cucai", "de"], east=[], boat_side=False, children=[]):
          self.west = west
          self.east = east
          self.boat_side = boat_side
          self.children = children

        def __str__(self):
          return str(self.west) + str(self.east) + ("1" if not self.boat_side else "2")

        def generate_children(self, previous_states, parent_map):
          children = []
          if not self.boat_side:
              for i in self.west:
                  new_west = self.west[:]
                  new_west.remove(i)
                  new_east = self.east[:]
                  new_east.append(i)
                  if sorted(new_west) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, new_west, new_east, not self.boat_side):
                      child = WGC_Node(new_west, new_east, not self.boat_side, [])
                      children.append(child)
                      parent_map[child] = self
              if sorted(self.west) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, self.west[:], self.east[:], not self.boat_side):
                  child = WGC_Node(self.west[:], self.east[:], not self.boat_side, [])
                  children.append(child)
                  parent_map[child] = self
          else:
              for i in self.east:
                  new_west = self.west[:]
                  new_west.append(i)
                  new_east = self.east[:]
                  new_east.remove(i)
                  if sorted(new_east) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, new_west, new_east, not self.boat_side):
                      child = WGC_Node(new_west, new_east, not self.boat_side, [])
                      children.append(child)
                      parent_map[child] = self
              if sorted(self.east) not in WGC_Node.incompatibilities and not WGC_Node.state_in_previous(previous_states, self.west[:], self.east[:], not self.boat_side):
                  child = WGC_Node(self.west[:], self.east[:], not self.boat_side, [])
                  children.append(child)
                  parent_map[child] = self
          self.children = children

        @staticmethod
        def state_in_previous(previous_states, west, east, boat_side):
            return any(
              sorted(west) == sorted(i.west) and
              sorted(east) == sorted(i.east) and
              boat_side == i.boat_side
              for i in previous_states
            )

    def find_solution(root_node, use_bfs=False):
          '''
          Find a solution to the WGC Problem.
          use_bfs: True for BFS
          '''
          to_visit = [root_node]
          node = root_node
          previous_states = []
          parent_map = {root_node: None}
          while to_visit:
            node = to_visit.pop()
            if not WGC_Node.state_in_previous(previous_states, node.west, node.east, node.boat_side):
                previous_states.append(node)
                node.generate_children(previous_states, parent_map)
            if use_bfs:
                to_visit = node.children + to_visit
            else:
                to_visit = to_visit + node.children
            if sorted(node.east) == ["cucai", "de", "soi"]:
                solution = []
                while node is not None:
                    solution = [node] + solution
                    node = parent_map[node]
                return solution
          return None

    root = WGC_Node()

    solution = find_solution(root, use_bfs=True)
    print("Máy tự động chơi = [\n", end='')
    for i in solution:
        print(i, '\b, ', end='')
        print("\b\b]")
  else:
    print("Chọn 1: người chơi \nChọn 2 : máy tự động chơi")
print("Chọn 1: người chơi \nChọn 2 : máy tự động chơi")
run= True
while run:
  switch(int(input('enter your choice')))
  if(input('choi tiep y/n')=='n'):
    run=False