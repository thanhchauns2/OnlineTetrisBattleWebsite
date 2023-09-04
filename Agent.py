import os
import numpy as np
import math


class Test:
    def __init__(self, turn):
        self.PIECE_NUM2TYPE = {1: 'I', 2: 'O', 3: 'J', 4: 'L', 5: 'Z', 6: 'S', 7: 'T', 8: 'G'}
        self.width = 10
        self.height = 20
        self.current_actions = []
        self.best_genes = [83.9582, 85.5775, 1.0495, 1.0602, 5.7449, 13.3834, 13.8588, 6.7820, 2.1385, -6.0317]
        self.genes = ['holeCountMultiplier', 'openHoleCountMultiplier', 'maximumLineHeightMultiplier',
                      'addedShapeHeightMultiplier', 'pillarCountMultiplier', 'blocksInRightMostLaneMultiplier',
                      'nonTetrisClearPenalty', 'blocksAboveHolesMultiplier', 'bumpinessMultiplier', 'tetrisRewardMultiplier']
        self.board =  np.array([[0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]])
        self.holding_piece, self.current_piece = 0, 0
        self.next_pieces, self.info_vector, self.time_left, self.heights = [], [], [], []
        self.holding = 0
        self.starting_position = (-2, 3)
        self.decode = {
            'I' : [ # 3 -> 2 -> 1 -> 4
                np.array([  [0, 0, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 1, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 0, 0, 0], 
                                            [1, 1, 1, 1], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 1, 0, 0], 
                                                            [0, 1, 0, 0], 
                                                            [0, 1, 0, 0], 
                                                            [0, 1, 0, 0]]),
                                                                np.array(  [[0, 0, 0, 0], 
                                                                            [1, 1, 1, 1], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'O' : [
                np.array([  [0, 0, 0, 0], 
                            [0, 1, 1, 0], 
                            [0, 1, 1, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 0], 
                                            [0, 1, 1, 0], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 0, 0, 0], 
                                                            [0, 1, 1, 0], 
                                                            [0, 1, 1, 0], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [0, 0, 0, 0], 
                                                                            [0, 1, 1, 0], 
                                                                            [0, 1, 1, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'J' : [
                np.array([  [0, 1, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 1], 
                                            [0, 1, 0, 0], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 0, 1, 0], 
                                                            [0, 0, 1, 0], 
                                                            [0, 0, 1, 1], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [0, 0, 0, 1], 
                                                                            [0, 1, 1, 1], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'L' : [
                np.array([  [0, 0, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 1, 1, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 1], 
                                            [0, 0, 0, 1], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 0, 1, 1], 
                                                            [0, 0, 1, 0], 
                                                            [0, 0, 1, 0], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [0, 1, 0, 0], 
                                                                            [0, 1, 1, 1], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'Z' : [
                np.array([  [0, 1, 0, 0], 
                            [0, 1, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 0], 
                                            [1, 1, 0, 0], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 1, 0, 0], 
                                                            [0, 1, 1, 0], 
                                                            [0, 0, 1, 0], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [0, 0, 1, 1], 
                                                                            [0, 1, 1, 0], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'S' : [
                np.array([  [0, 0, 1, 0], 
                            [0, 1, 1, 0], 
                            [0, 1, 0, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 0], 
                                            [0, 0, 1, 1], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 0, 1, 0], 
                                                            [0, 1, 1, 0], 
                                                            [0, 1, 0, 0], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [1, 1, 0, 0], 
                                                                            [0, 1, 1, 0], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ],
            'T' : [
                np.array([  [0, 0, 1, 0], 
                            [0, 1, 1, 0], 
                            [0, 0, 1, 0], 
                            [0, 0, 0, 0]]),
                                np.array([  [0, 0, 0, 0], 
                                            [0, 1, 1, 1], 
                                            [0, 0, 1, 0], 
                                            [0, 0, 0, 0]]),
                                                np.array([  [0, 0, 1, 0], 
                                                            [0, 0, 1, 1], 
                                                            [0, 0, 1, 0], 
                                                            [0, 0, 0, 0]]),
                                                                np.array([  [0, 0, 1, 0], 
                                                                            [0, 1, 1, 1], 
                                                                            [0, 0, 0, 0], 
                                                                            [0, 0, 0, 0]]),
            ]
        }

    def calculate_heights(self, block):
        return np.array([20 - np.where(block[i] == 1)[0][0] if 1 in block[i] else 0 for i in range(0, 10)])

    def state_to_infos(self, state):
        state = np.squeeze(state)
        self.board = np.transpose(state[:, :10], (1, 0))  # 10 x 20
        self.board = np.where(self.board < 1, 0, self.board)
        # print(np.shape(self.board))
        self.heights = self.calculate_heights(self.board)

        feature_vector = state[:, 10:17]

        self.holding_piece = 0 if not self.holding else np.where(feature_vector[0] == 1)[0][0] + 1
        self.next_pieces.clear()

        for i in range(1, 7):
            self.next_pieces.append(np.where(feature_vector[i] == 1)[0][0] + 1)

        self.current_piece = np.where(feature_vector[6] == 1)[0][0] + 1

        self.info_vector = feature_vector[7]
        self.time_left = feature_vector[-1][-1]

        # print(self.board, self.holding_piece, self.next_pieces, self.current_piece)
        # print(self.heights)

    def hard_drop(self, shape):
        actions = []
        hard_drops = []
        sum_heights = np.sum(self.heights)
        for spin in range(0, 4):
            current_shape = self.decode[self.PIECE_NUM2TYPE[shape]][spin]
            last_dots = np.array([np.where(current_shape[i] == 1)[0][-1] if 1 in current_shape[i] else -1 for i in range(0, 4)])
            actions2 = actions
            for left_shift in range(0, 8):

                # check compatible
                compatible = 1
                for col in range(0, 4):
                    c = col + 3 + left_shift
                    if last_dots[col] == -1:
                        continue
                    if c < 10:
                        continue
                    compatible = 0
                    break
                if not compatible: break

                # calculate max drops available
                max_drop = 100
                for col in range(0, 4):
                    if last_dots[col] == -1: continue
                    c = col + 3 + left_shift
                    drop_available = 20 - self.heights[c] + 1 - last_dots[col]
                    max_drop = min(max_drop, drop_available)

                # drop
                board = self.board.copy()
                for i in range(0, 4):
                    for j in range(0, 4):
                        if i + left_shift < 0 or i + left_shift > 9 or j - 2 + max_drop < 0 or j - 2 + max_drop > 19: continue
                        board[i + left_shift][j - 2 + max_drop] += current_shape[i][j]
                # print(current_shape, last_dots, self.board, max_drop, left_shift)

                # save
                block_height = np.sum(self.calculate_heights(board)) - sum_heights
                hard_drops.append([actions, board, block_height])
                actions.append(6)
            actions2 = actions
            for right_shift in range(0, 8):

                # check compatible
                compatible = 1
                for col in range(0, 4):
                    c = col + 3 - right_shift
                    if last_dots[col] == -1:
                        continue
                    if c < 10:
                        continue
                    compatible = 0
                    break
                if not compatible: break

                # calculate max drops available
                max_drop = 100
                for col in range(0, 4):
                    if last_dots[col] == -1: continue
                    c = col + 3 - right_shift
                    drop_available = 20 - self.heights[c] + 1 - last_dots[col]
                    max_drop = min(max_drop, drop_available)

                # drop
                board = self.board.copy()
                for i in range(0, 4):
                    for j in range(0, 4):
                        if i - right_shift < 0 or i - right_shift > 9 or j - 2 + max_drop < 0 or j - 2 + max_drop > 19: continue
                        board[i - right_shift][j - 2 + max_drop] += current_shape[i][j]
                # print(current_shape, last_dots, self.board, max_drop, left_shift)

                # save
                block_height = np.sum(self.calculate_heights(board)) - sum_heights
                hard_drops.append([actions, board, block_height])
                actions.append(6)

            # spin
            actions.append(4)
        return hard_drops

    def calc_best_movement_plan(self, state):
        self.state_to_infos(state)
        candidates = {
            0: self.current_piece,
            1: self.holding_piece if self.holding_piece != 0 else self.next_pieces[0]
        }
        best_actions = [0]

        hard_drops = []
        for hold, shape in candidates.items():
            hd = self.hard_drop(shape)
            if hold == 1:
                for actions in hd:
                    actions[0] = [1] + actions[0]
            hard_drops += hd

        best_actions, best_line_cleared = self.find_best_movement_plan(hard_drops)

        self.line_cleared = best_line_cleared

        return best_actions


    def get_actions(self, state):
        # actions = []
        actions = self.calc_best_movement_plan(state)
        self.hard_drop(self.current_piece)
        actions.append(2)
        # actions.append(0)
        # actions.append(0)
        # actions.append(0)
        # actions.append(0)
        # actions.append(0)
        # actions.append(0)
        return actions

    def choose_action(self, state):
        if len(self.current_actions) > 0:
            self.line_cleared = 0
            return self.current_actions.pop(0)
        else:
            self.current_actions = self.get_actions(state)
            return self.current_actions.pop(0)

    def calc_max_line_height(self, matrix_block):
        return np.max(self.calculate_heights(matrix_block))
    
    ## TODO: Optimize

    # def count_holes(self, matrix_block):
    #     hole_count, open_hole_count, blocks_above_holes = 0, 0, 0
    #     #     an open hole is one which isnt fully covered, like there isnt a block to the left or right,
    #     #     open holes are less bad than normal holes because you can slip a piece in there.
    #     #     actually an open hole needs 2 spots to a side to be able to be filled.

    #     for i in range(self.width):
    #         block_found = False
    #         holes_found = False

    #         # going down each column look for a block and once found each block below is a hole
    #         for j in range(self.height):
    #             if matrix_block[i][j] == 1:
    #                 block_found = True
    #             elif block_found == True:
    #                 hole_count += 1
            
    #         for j in reversed(range(self.height)):
    #             if matrix_block[i][j] == 0:
    #                 holes_found = True
    #             elif holes_found == True:
    #                 blocks_above_holes += 1
                
    #     return hole_count, open_hole_count, blocks_above_holes
    

    # def count_pillars(self, matrix_block):
    #     pillar_cnt = 0
    #     for i in range(self.width):
    #         current_pillar_height_L = 0
    #         current_pillar_height_R = 0

    #         for j in reversed(range(self.height - 1)):
    #             if (i > 0 and matrix_block[i][j] != 0) and matrix_block[i - 1][j] == 0:
    #                 current_pillar_height_L += 1
    #             else:
    #                 if current_pillar_height_L >= 3:
    #                     pillar_cnt += current_pillar_height_L
    #                 current_pillar_height_L = 0

    #             if (i < self.width - 2 and matrix_block[i][j] != 0 and matrix_block[i + 1][j] == 0):
    #                 current_pillar_height_R += 1
    #             else:
    #                 if current_pillar_height_R >= 3:
    #                     pillar_cnt += current_pillar_height_R
    #                 current_pillar_height_R = 0

    #         if current_pillar_height_R >= 3:
    #             pillar_cnt += current_pillar_height_R
    #         if current_pillar_height_L >= 3:
    #             pillar_cnt += current_pillar_height_L

    #     return pillar_cnt

    # def count_number_of_block_in_right_lane(self, matrix_block):
    #     return np.sum(matrix_block[self.width - 1])
    #     # blocks_in_right_lane = 0
    #     # for j in range(self.height):
    #     #     if matrix_block[self.width - 1][j] != 0:
    #     #         blocks_in_right_lane += 1

    #     # return blocks_in_right_lane

    # # 1

    # def calc_bumpiness(self, matrix_block):
    #     bumpiness = 0
    #     previous_line_height = 0

    #     for i in range(self.width - 1):
    #         for j in range(self.height):
    #             if matrix_block[i][j] != 0:
    #                 current_line_height = self.height - j
    #                 if i != 0:
    #                     bumpiness += abs(previous_line_height - current_line_height)
    #                 previous_line_height = current_line_height
    #                 break

    #     return bumpiness

    # # 2

    # def clear_lines(self, matrix_block):
    #     cleared = 0
    #     matrix_block = matrix_block.tolist()
    #     for y in reversed(range(self.height)):
    #         # y = -(y + 1)
    #         row = 0
    #         for x in range(self.width):
    #             print(matrix_block, x, y)
    #             if matrix_block[x][y] == 1:
    #                 row += 1

    #         if row == self.width:
    #             cleared += 1
    #             for i in range(self.width):
    #                 del matrix_block[i][y]
    #                 matrix_block[i] = [0] + matrix_block[i]

    #     return np.array(matrix_block), cleared

    # def calc_cost(self, matrix_block, block_height):
    #     dict_genes = {key: value for key, value in zip(self.genes, self.best_genes)}
    #     hole_cnt, open_hole_cnt, max_line_height, pillar_cnt = 0, 0, 0, 0 
    #     block_in_right_lane, lines_clear_which_arent_tetrises, blocksInRightMostLaneMultiplier = 0, 0, 0
    #     blocks_above_holes, bumpiness, block_height, line_cleared = 0, 0, 0, 0
    #     nonTetrisClearPenalty, tetrises = 0, 0

    #     matrix_block, line_cleared = self.clear_lines(matrix_block)
    #     # # transpose_block = np.transpose(matrix_block)
    #     # hole_cnt, open_hole_cnt, blocks_above_holes = self.count_holes(matrix_block)
    #     # max_line_height = self.calc_max_line_height(matrix_block)
    #     # pillar_cnt = self.count_pillars(matrix_block)
    #     # block_in_right_lane = self.count_number_of_block_in_right_lane(matrix_block)
    #     # bumpiness = self.calc_bumpiness(matrix_block)

    #     # lines_clear_which_arent_tetrises = 1 if (line_cleared > 0 and line_cleared < 4) else 0
    #     # tetrises = 1 if line_cleared == 4 else 0

    #     # nonTetrisClearPenalty = dict_genes['nonTetrisClearPenalty']
    #     # blocksInRightMostLaneMultiplier = dict_genes['blocksInRightMostLaneMultiplier']

    #     # if max_line_height > 6 or hole_cnt > 0 or pillar_cnt > 10:
    #     #     nonTetrisClearPenalty = 0
    #     #     blocksInRightMostLaneMultiplier = 0

    #     return (dict_genes['holeCountMultiplier'] * hole_cnt +
    #             dict_genes['openHoleCountMultiplier'] * open_hole_cnt +
    #             dict_genes['maximumLineHeightMultiplier'] * max_line_height +
    #             dict_genes['pillarCountMultiplier'] * pillar_cnt +
    #             blocksInRightMostLaneMultiplier * block_in_right_lane +
    #             nonTetrisClearPenalty * lines_clear_which_arent_tetrises +
    #             dict_genes['blocksAboveHolesMultiplier'] * blocks_above_holes +
    #             dict_genes['bumpinessMultiplier'] * bumpiness +
    #             dict_genes['addedShapeHeightMultiplier'] * block_height +
    #             dict_genes['tetrisRewardMultiplier'] * tetrises), line_cleared
    
    # def find_best_movement_plan(self, all_matrix_block): # 1
    #     min_holes = 10000
    #     min_holes_matrix = []

    #     for [actions, matrix, block_height] in all_matrix_block:
    #         matrix_holes = self.count_holes(matrix)[0]
    #         if matrix_holes < min_holes:
    #             min_holes = matrix_holes

    #     for [actions, matrix, block_height] in all_matrix_block:
    #         matrix_holes = self.count_holes(matrix)[0]

    #         if matrix_holes == min_holes:
    #             min_holes_matrix.append([actions, matrix, block_height])

    #     min_score = 1e9
    #     min_score_matrix_actions = []
    #     min_score_matrix_line_cleared = 0

    #     for [actions, matrix, block_height] in min_holes_matrix:
    #         score, line_cleared = self.calc_cost(matrix, block_height)
    #         if min_score > score:
    #             min_score = score
    #             min_score_matrix_actions = actions
    #             min_score_matrix_line_cleared = line_cleared
    #     return min_score_matrix_actions, min_score_matrix_line_cleared