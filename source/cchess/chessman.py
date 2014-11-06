# -*- coding: utf-8 -*-

'''
Copyright (C) 2014  walker li <walker8088@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys

from common import *

#-----------------------------------------------------#
KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN, NONE = range(8)

h_level_index = ((u"九",u"八",u"七",u"六",u"五",u"四",u"三",u"二",u"一"), 
                (u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９") )

v_change_index = ( (u"错", ""u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"), 
                (u"误", ""u"１", u"２", u"３", u"４", u"５", u"６", u"７", u"８", u"９") )


advisor_pos = (((3, 9), (5, 9), (4, 8), (3, 7), (5, 7)), 
               ((3, 0), (5, 0), (4, 1), (3, 2), (5, 2)))

bishop_pos = (((2, 9), (6, 9), (0, 7), (4, 7), (9, 7), (2, 5), (6, 5)), 
              ((2, 0), (6, 0), (0, 2), (4, 2), (9, 2), (2, 4), (6, 4)))

"""
king_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]

advisor_dir = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
bishop_dir = [(-2, -2), (2, -2), (2, 2), (-2, 2)]

knight_dir = [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)]
rook_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
cannon_dir = [(0, -1), (1, 0), (0, 1), (-1, 0)]
pawn_dir = [[(0, -1), (-1, 0), (1, 0)], [(0, 1), (-1, 0), (1, 0)]]
"""

#-----------------------------------------------------#
#KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN
chessman_show_names = ( (u"帅",u"仕",u"相",u"马",u"车",u"炮",u"兵"),
                        (u"将",u"士",u"象",u"马",u"车",u"炮",u"卒") )
                    
def get_show_name(kind, color) :
        return chessman_show_names[color][kind]
        
#-----------------------------------------------------#
def get_kind(fen_ch):
    if fen_ch in ['k', 'K']:
        return KING
    elif fen_ch in ['a', 'A']:
        return ADVISOR
    elif fen_ch in ['b', 'B']:
        return BISHOP
    elif fen_ch in ['n', 'N']:
        return KNIGHT
    elif fen_ch in ['r', 'R']:
        return ROOK
    elif fen_ch in ['c', 'C']:
        return CANNON
    elif fen_ch in ['p', 'P']:
        return PAWN
    else:
        return NONE

def get_char(kind, color):
    if kind is KING:
        return ['K', 'k'][color]
    elif kind is ADVISOR:
        return ['A', 'a'][color]
    elif kind is BISHOP:
        return ['B', 'b'][color]
    elif kind is KNIGHT:
        return ['N', 'n'][color]
    elif kind is ROOK:
        return ['R', 'r'][color]
    elif kind is CANNON:
        return ['C', 'c'][color]
    elif kind is PAWN:
        return ['P', 'p'][color]
    else:
        return ''

#-----------------------------------------------------#

class Chessman(object):
    
    def __init__(self, board, kind, color, pos):
        
        self.board = board
        
        self.kind = kind
        self.color = color
        
        self.x, self.y = pos
        
        self.name = get_show_name(kind, color)
        
        self.__can_place_checks = {
            KING : self.__can_place_king, 
            ADVISOR : self.__can_place_advisor, 
            BISHOP : self.__can_place_bishop, 
            PAWN : self.__can_place_pawn
        }
        
        self.__can_move_checks = {
            KING : self.__can_move_king, 
            ADVISOR : self.__can_move_advisor, 
            BISHOP : self.__can_move_bishop, 
            KNIGHT : self.__can_move_knight, 
            ROOK : self.__can_move_rook, 
            CANNON : self.__can_move_cannon,
            PAWN : self.__can_move_pawn
        }
        
        self.__chinese_move_to_std_move_checks = {
            ADVISOR : self.__chinese_move_to_std_move_advisor, 
            BISHOP : self.__chinese_move_to_std_move_bishop, 
            KNIGHT : self.__chinese_move_to_std_move_knight, 
        }
    
    def std_move_to_chinese_move(self, p_to, index_str = None):
        
        if self.kind in [KING, ROOK, CANNON, PAWN]:
            diff = p_to[1] - self.y 
            if diff == 0:
                #平移
                diff_str = u"平" + h_level_index[self.color][p_to[0]]
            else :
                #黑方是红方的反向操作    
                if self.color == BLACK:
                    diff = -diff
                
                if diff < 0 : 
                    diff_str = u"进" + v_change_index[self.color][-diff]
                else :
                    diff_str = u"退" + v_change_index[self.color][diff]
            
            if not index_str :
                move_str = self.name + h_level_index[self.color][self.x] + diff_str 
            else:
                move_str = index_str + self.name + diff_str
                
        else :
            diff = p_to[1] - self.y 
            
            if self.color == BLACK:
                diff = -diff
            
            if diff < 0 : 
                diff_str = u"进"
            else :
                diff_str = u"退"
            
            if not index_str :
                move_str = self.name + h_level_index[self.color][self.x] + diff_str + h_level_index[self.color][p_to[0]]
            else :
                move_str = index_str + self.name + diff_str + h_level_index[self.color][p_to[0]]
            
        return move_str
    
    def chinese_move_to_std_move(self, move_str):
        
        if self.kind in self.__chinese_move_to_std_move_checks :
            new_pos = self.__chinese_move_to_std_move_checks[self.kind](move_str)
        else :    
            new_pos = self.__chinese_move_to_std_move_default(move_str)
        
        if not new_pos :
            return None
            
        if not self.can_move_to(new_pos[0] , new_pos[1]):
            return None 
            
        return ((self.x,  self.y), new_pos)
    
    def can_place_to(self, x, y):
        if not self.__can_place_check_default(x, y):
            return False
            
        if self.kind in self.__can_place_checks:
            return self.__can_place_checks[self.kind](x, y)
        
        return True
        
    def can_move_to(self, x, y):
        
        if not self.__can_move_check_default(x, y):
            print "not self.can_move_default"
            return False
        
        return self.__can_move_checks[self.kind](x, y) 
        
    def __can_place_check_default(self, x, y):
        
        if x < 0 or x > 8 or y < 0 or y > 9:
            return False
        
        if self.board.at_pos(x, y) != None :
            return False
            
        return True
    
    #王
    def __can_place_king(self, x, y):
        
        if x < 3 or x > 5:
            return False
            
        if (self.color == RED) and y < 7:
            return False
            
        if (self.color == BLACK) and y > 2:
            return False
            
        return True
    
    #士
    def __can_place_advisor(self, x, y):
        
        if (x, y) in advisor_pos[self.color] :
            return True    
        
        return False
    
    #象    
    def __can_place_bishop(self, x, y):
        
        if (x, y) in bishop_pos[self.color] :
            return True
            
        return False
    #兵    
    def __can_place_pawn(self, x, y):
        
        if (self.color == RED) and y > 6:
            return False
            
        if (self.color == BLACK) and y < 3:
            return False
            
        return True
    
    def __can_move_check_default(self, x, y):
        
        if x < 0 or x > 8 or y < 0 or y > 9:
            return False
        
        old_man = self.board.at_pos(x, y)
        if old_man and (old_man.color == self.color) :
            return False
            
        return True
    
        
    def __can_move_king(self, x, y):
        
        if not self.__can_place_king(x, y) :
            return False
        
        if (abs(self.x - x) + abs(self.y - y)) != 1:
            return False
        
        #照将检查    
        
        #被将军检查TODO
        
        return True
        
    def __can_move_advisor(self, x, y):
        
        if not self.__can_place_advisor(x, y) :
            return False
        
        if (abs(self.x - x) == 1) and (abs(self.y - y) == 1):
            return True
        else :
            return False
        
    def __can_move_bishop(self, x, y):
        
        if (abs(self.x - x) != 2) or (abs(self.y - y) != 2):
            return False
        
        m_x = (self.x + x) / 2
        m_y = (self.y + y) / 2
        
        #塞象眼检查
        if self.board.at_pos(m_x, m_y) != None :
            return False
        
        return True
    
    def __can_move_knight(self, x, y):
        
        if (abs(self.x - x) == 2) and (abs(self.y - y) == 1):
            
            m_x = (self.x + x) / 2
            m_y = self.y
            
            #别马腿检查
            if self.board.at_pos(m_x, m_y) == None :
                return True

        if (abs(self.x - x) == 1) and (abs(self.y - y) == 2):
            
            m_x = self.x
            m_y = (self.y + y) / 2
            
            #别马腿检查
            if self.board.at_pos(m_x, m_y) == None :
                return True

        return False
        
    def __can_move_rook(self, x, y):
        
        if self.x != x:
            
            #斜向移动是非法的
            if self.y != y:   
                return False
            
            if self.board.between_h_line(self.y, self.x, x) != 0:
                return False
                
        else :
            if self.board.between_v_line(self.x, self.y, y) != 0:
                return False
                
        return True
        
    def __can_move_cannon(self, x, y):
        
        if self.x != x:
            #斜向移动是非法的
            if self.y != y:   
                return False
            
            #水平移动    
            count = self.board.between_h_line(self.y, self.x, x)
            
        else :
            #垂直移动
            count = self.board.between_v_line(self.x, self.y, y)
        
        if count == 0 :
            #炮移动
            if self.board.at_pos(x, y) == None :
                return True
        
        if count == 1 :
            #炮吃子
            if self.board.at_pos(x, y) != None :
                return True
        
        return False
        
    def __pawn_over_river(self) :      
        if (self.color == RED) and (self.y < 5) :
            return True
            
        if (self.color == BLACK) and (self.y > 4 ) :
            return True
            
        return False
    
    def __can_move_pawn(self, x, y):
        
        not_over_river_step = ((0, -1), (0, 1))
        over_river_step = (((-1, 0), (1, 0), (0, -1)), 
                           ((-1, 0), (1, 0), (0, 1)))
                           
                
        step = (x - self.x, y - self.y)
        
        over_river = self.__pawn_over_river()
        
        if (not over_river) and (step == not_over_river_step[self.color]):
                return True
        
        if over_river and (step in over_river_step[self.color]):
                return True
                
        return False
        
    def __chinese_move_to_std_move_advisor(self, move_str):
        if move_str[0] == u"平":
            return None
        
        new_x = h_level_index[self.side].index(move_str[1])
                
        if move_str[0] == u"进" :
            diff_y = 1
        elif move_str[0] == u"退" :
            diff_y = -1    
        else :
            return None
        
        if self.color == BLACK:
            diff_y = - diff_y
        
        new_y = self.y - diff_y
        
        return (new_x,  new_y)
        
    def __chinese_move_to_std_move_bishop(self, move_str):
        if move_str[0] == u"平":
            return None
        
        new_x = h_level_index[self.side].index(move_str[1])
                
        if move_str[0] == u"进" :
            diff_y = 2
        elif move_str[0] == u"退" :
            diff_y = -2    
        else :
            return None
        
        if self.color == BLACK:
            diff_y = - diff_y
        
        new_y = self.y - diff_y
        
        return (new_x,  new_y)
        
    def __chinese_move_to_std_move_knight(self, move_str):
        if move_str[0] == u"平":
            return None
        
        new_x = h_level_index[self.side].index(move_str[1])
        
        diff_x = abs(self.x - new_x)
        
        if move_str[0] == u"进" :
            diff_y = [3, 2, 1][diff_x]
            
        elif move_str[0] == u"退" :
            diff_y = [-3, -2, -1][diff_x]
            
        else :
            return None
        
        if self.color == BLACK:
            diff_y = -diff_y
        
        new_y = self.y - diff_y
        
        return (new_x,  new_y)
        
    def __chinese_move_to_std_move_default(self, move_str):
        
        if move_str[0] == u"平":
            new_x = h_level_index[self.color].index(move_str[1])
            
            return (new_x,  self.y)
            
        else :
            #王，车，炮，兵的前进和后退
            diff = v_change_index[self.side].index(move_str[1])
            
            if move_str[0] == u"进":
                diff = -diff
            elif move_str[0] != u"退":
                return None
                
            if self.color == BLACK:
                diff = -diff
            
            new_y = self.y + diff
            
            return (self.x,  new_y)
    
