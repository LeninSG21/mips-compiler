
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMA I IMM J LABEL LABELDEF MNEMONIC NUMBER O OFFSET PA PC R REGexp : exp expexp : inst exp : LABELDEF inst inst : R REG COMA REG COMA REGinst : R REG COMA REGinst : R REGinst : R REG COMA REG COMA IMMinst : I REG COMA REG COMA IMMinst : I REG COMA IMMinst : I REG COMA IMM PA REG PCinst : I REG COMA REG COMA LABEL'
    
_lr_action_items = {'LABELDEF':([0,1,2,6,7,8,12,14,18,19,20,21,23,],[3,3,-2,3,-3,-6,-5,-9,-4,-7,-8,-11,-10,]),'R':([0,1,2,3,6,7,8,12,14,18,19,20,21,23,],[4,4,-2,4,4,-3,-6,-5,-9,-4,-7,-8,-11,-10,]),'I':([0,1,2,3,6,7,8,12,14,18,19,20,21,23,],[5,5,-2,5,5,-3,-6,-5,-9,-4,-7,-8,-11,-10,]),'$end':([1,2,6,7,8,12,14,18,19,20,21,23,],[0,-2,-1,-3,-6,-5,-9,-4,-7,-8,-11,-10,]),'REG':([4,5,10,11,15,17,],[8,9,12,13,18,22,]),'COMA':([8,9,12,13,],[10,11,15,16,]),'IMM':([11,15,16,],[14,19,20,]),'PA':([14,],[17,]),'LABEL':([16,],[21,]),'PC':([22,],[23,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'exp':([0,1,6,],[1,6,6,]),'inst':([0,1,3,6,],[2,2,7,2,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> exp","S'",1,None,None,None),
  ('exp -> exp exp','exp',2,'p_exp_exp','mipsCompiler.py',81),
  ('exp -> inst','exp',1,'p_exp','mipsCompiler.py',85),
  ('exp -> LABELDEF inst','exp',2,'p_exp_label','mipsCompiler.py',89),
  ('inst -> R REG COMA REG COMA REG','inst',6,'p_R1','mipsCompiler.py',93),
  ('inst -> R REG COMA REG','inst',4,'p_R2','mipsCompiler.py',100),
  ('inst -> R REG','inst',2,'p_R3','mipsCompiler.py',104),
  ('inst -> R REG COMA REG COMA IMM','inst',6,'p_Rshift','mipsCompiler.py',111),
  ('inst -> I REG COMA REG COMA IMM','inst',6,'p_I1','mipsCompiler.py',116),
  ('inst -> I REG COMA IMM','inst',4,'p_I2','mipsCompiler.py',123),
  ('inst -> I REG COMA IMM PA REG PC','inst',7,'p_I3','mipsCompiler.py',130),
  ('inst -> I REG COMA REG COMA LABEL','inst',6,'p_I1Label','mipsCompiler.py',134),
]