from copy import deepcopy
import random
import pandas as pd
class Agent:
  '''
  Class thực hiện chức năng chọn hành động trong trò chơi.
  Agent sẽ bao gồm các thành phần sau:
  - board: một ma trận kích thước 20x10, thể hiện state hiện tại của trò chơi. Giá trị của các số trong board thể hiện:
    + 0: ô trống
    + 1: ô đã được lấp kín
    + 0.7: khối tetris hiện tại cùng vị trí của nó
    + 0.3: vị trí của khối tetris, nếu được thả rơi xuống
  - PIECE_NUM2TYPE: cách decode các số trong biến holding và pieces thành các khối tương ứng
  - PIECE_TYPE2NUM: cách decode ngược lại với PIECE_NUM2TYPE
  - holding: khối tetris đang được hold, trả về 0 nếu không có khối nào
  - pieces: khối tetris hiện tại, cùng 5 khối tetris tiếp theo
  Các action có thể trả về: 
  - 0: "NOOP",
  - 1: "hold",
  - 2: "drop",
  - 3: "rotate_right",
  - 4: "rotate_left",
  - 5: "right",
  - 6: "left",
  - 7: "down"
  Việc cần làm:
  Hãy implement function để trả về action tốt nhất cho trạng thái hiện tại
  Dữ liệu mẫu của biến 'obs':
    0.0,0.0,0.0,0.0,1.0,0.7,0.7,0.0,0.0,0.0,1.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.7,0.7,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,1.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,1.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.7,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,1.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,1.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,1.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,1.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,1.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,1.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,-20.0,-20.0,1.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,1.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.3,0.3,0.0,0.0,0.0,0.0,-20.0,1.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,-0.1,0.0,0.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,-0.1,0.0,0.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,1.0,1.0,1.0,1.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0
    0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.988,0.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,-20.0,-20.0,-20.0,-20.0,-20.0,-20.0,0.988

  '''

  PIECE_NUM2TYPE = {1: 'I', 2: 'O', 3: 'J', 4: 'L', 5: 'Z', 6: 'S', 7: 'T'}
  PIECE_TYPE2NUM = {val: key for key, val in PIECE_NUM2TYPE.items()}
  START_POS = {
    'Z': 4,
    'S': 4,
    'L': 4,
    'J': 4,
    'I': 4,
    'T': 4,
    'O': 5,
  }
  blank_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

  def __init__(self, turn = 0):
    '''
    Strategy sẽ như sau:
    - Đưa khối qua trái xa nhất có thể
    - Đưa khối qua phải xa nhất có thể
    - Đưa khối lại vị trí ban đầu
    - Mỗi khi qua 1 vị trí mới, lưu state hiện tại vào kho
    - Trong tất cả các state, chọn ra state tốt nhất
    - Di chuyển đến state tốt nhất
    - Drop down, sau đó reset toàn bộ quá trình

    Điểm hạn chế:
    - CHƯA sử dụng rotate
    - Hàm evaluate cần được cải tiến
    - CHƯA sử dụng được T-spin
    '''
    self.turn  = turn
    self.board = []
    self.holding = 0
    self.pieces = []
    self.strategy = [ # Chứa các tuple, có dạng (state, các action cần thiết)
    ]
    self.refresh = 1
    self.base = None
    self.chosen_actions = {}
    self.sim = []
    self.current_actions = {
      'left' : 0,
      'right' : 0,
      'rotate' : 0
    }
    self.orient = 'left'
    self.touch = 0
  
  def renew(self):
    self.touch = 0
    self.orient = 'left'
    self.current_actions = {
      'left' : 0,
      'right' : 0,
      'rotate' : 0,
    }
    self.refresh = 1
    self.base = None
    self.strategy = []

  def initialize(self, obs):

    # initialize
    self.board = []
    self.holing = 0
    self.pieces = []

    # if self.turn == 1:
    #   # get the board
    #   for i in range(20):
    #     row = []
    #     for j in range(10):
    #       row.append(obs[i][j][0])
    #     self.board.append(row)
      
    #   # get the holding piece
    #   for i in range(10, 17):
    #     if obs[0][i][0] == 1:
    #       self.holding = i - 9
      
    #   # get next 5 pieces
    #   for i in range(10, 17):
    #     for j in range(1, 6):
    #       if obs[j][i][0] == 1:
    #         self.pieces.append(i - 9)
    #         break
    # else:
    #   # get the board
    for i in range(20):
      row = []
      for j in range(17, 27):
        row.append(obs[i][j][0])
      self.board.append(row[:])
    
    # get the holding piece
    for i in range(27, 34):
      if obs[0][i][0] == 1:
        self.holding = i - 26
    
    # get next 5 pieces
    for j in range(1, 6):
      for i in range(27, 34):
        if obs[j][i][0] == 1:
          self.pieces.append(i - 26)
          break

  def end_phase(self):
    self.current_actions['rotate'] = 0
    self.base = self.strategy[0][0]
    self.touch = 100

  def choose_action(self, obs):

    # lấy thông tin từ obs
    self.initialize(obs)
    # self.turn += 1
    # if self.turn % 2 == 0:
    #   return 0
    if self.turn == 0:
      self.turn = 1
      return 0
    
    pd.DataFrame(self.sim).to_csv("data2.csv")

    # Nếu vẫn còn hành động phải làm
    if self.sim != []:
      print(100)
      if self.simulate(self.board) == self.sim:
        self.chosen_actions = {}
        self.sim = []
        return 2
      elif self.chosen_actions['rotate'] > 0:
        self.chosen_actions['rotate'] -= 1
        # self.chosen_actions['left'] = 8
        # self.chosen_actions['right'] = 8
        return 3
      elif self.chosen_actions['left'] > 0:
        self.chosen_actions['left'] -= 1
        return 6
      elif self.chosen_actions['right'] > 0:
        self.chosen_actions['right'] -= 1
        return 5
      else:
        self.chosen_actions['left'] = 10
        self.chosen_actions['right'] = 10
        return 3

    # print(len(self.strategy))
    cur_piece = self.pieces[0]

    # Nếu đây là vị trí bắt đầu
    # print(self.board)
    sim = self.simulate(deepcopy(self.board))
    # sim = deepcopy(self.board)
    # print(simulate)

    if self.refresh:
      self.base = deepcopy(sim)
      self.refresh = 0
      self.strategy.append((deepcopy(sim), deepcopy(self.current_actions)))
      return 6
    # Ngược lại
    else:
      # Kiểm tra xem state hiện tại có phải state bắt đầu không: Nếu có nghĩa là đã đi 1 nửa vòng
      # Nếu đây là lần thứ 2 chạm state đầu tiên, nghĩa là đã duyệt toàn bộ các state cần tìm
      print(101)
      if sim == self.base:
        self.touch += 1
        print(self.touch)
        if self.touch == 2:
          if cur_piece == self.PIECE_TYPE2NUM['O']:
            self.end_phase()
          else:
            self.current_actions['rotate'] += 1
            self.refresh = 1
          return 3
        elif self.touch == 4:
          if cur_piece == self.PIECE_TYPE2NUM['I'] or cur_piece == self.PIECE_TYPE2NUM['Z'] or cur_piece == self.PIECE_TYPE2NUM['S']:
            self.end_phase()
          else:
            self.current_actions['rotate'] += 1
            self.refresh = 1
          return 3
        elif self.touch == 6:
          self.current_actions['rotate'] += 1
          self.refresh = 1
          return 3
        elif self.touch == 8:
          self.end_phase()
          return 3
      if self.touch > 10: # Đã duyệt hết, chọn ra vị trí tối ưu
        self.evaluate()
        self.renew()
        print(102)
        return 0
          
      if sim != self.strategy[-1][0]:
        if self.orient == 'left':
          if self.current_actions['right'] > 0:
            self.current_actions['right'] -= 1
          else:
            self.current_actions['left'] += 1
        else:
          if self.current_actions['left'] > 0:
            self.current_actions['left'] -= 1
          else:
            self.current_actions['right'] += 1
      else:
        if self.orient == 'left':
          self.orient = 'right'
        else:
          self.orient = 'left'
      
      # Kiểm tra xem state hiện tại đã có trong strategy chưa:
      check = any(x == (sim, self.current_actions) for x in self.strategy)
      if check == 0:
        self.strategy.append((deepcopy(sim), deepcopy(self.current_actions)))

      print(103)
      if self.orient == 'left':
        return 6
      else:
        return 5

    # return random.randint(0, 7)

  def simulate(self, state):
    # s = deepcopy(state)
    s = state[::-1]

    EPSILON = 0.0001

    for i in range(10):
      for j in range(20):
        if abs(s[j][i] - 0.7) < EPSILON:
          s[j][i] = 0
        if abs(s[j][i] - 0.3) < EPSILON:
          s[j][i] = 1
    s = s[::-1]
    
    s = self.clear_rows(s)

    return s
  
  def clear_rows(self, board):
    new_board = []
    b = board[::-1]
    for row in b:
      if sum(row) < 10:
        new_board.append(row[:])
    while len(new_board) < 20:
      new_board.append(self.blank_row[:])
    b = b[::-1]
    new_board = new_board[::-1]
    return new_board
  
  # Hàm chính để tính toán số điểm của một state
  def calculate(self, state):
    state = state[::-1]

    EPSILON = 0.0001

    for i in range(10):
      for j in range(20):
        if abs(state[j][i] - 0.7) < EPSILON:
          state[j][i] = 0
        if abs(state[j][i] - 0.3) < EPSILON:
          state[j][i] = 1
    
    state = self.clear_rows(state)

    height = 0
    for i in range(10):
      for j in range(20):
        # print(state, j, i)
        if state[j][i] == 1:
          height = max(height, j)
    
    holes = 0
    for i in range(10):
      exist = 0
      for j in range(19, -1, -1):
        if exist and state[j][i] == 0:
          holes += 1
        if state[j][i] == 1:
          exist = 1

    points = -height * 10 - holes * 100
    return points
  
  # Hàm để drop "thử" thanh tetris xuống, và tính toán số điểm của nó
  def extract(self, state):
    return self.calculate(deepcopy(state))

  # Hàm lấy ra state tốt nhất trong strategy
  def evaluate(self):
    s, a, p = None, None, -1e10
    for state, action in self.strategy:
      points = self.extract(state)
      if points > p:
        p = points
        s = state
        a = action
        # print(p, s, a)
        a['left'] = 10
        a['right'] = 10
        # a['rotate'] = 3
    # self.sim = self.simulate(s)
    self.sim = deepcopy(s)
    self.chosen_actions = deepcopy(a)