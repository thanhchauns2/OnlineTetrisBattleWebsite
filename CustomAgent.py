import os
import numpy as np
import math


class Agent:
    def __init__(self, turn):
        #         dir_path = os.path.dirname(os.path.realpath(__file__))
        #         weight_file_path = os.path.join(dir_path, turn, 'weight')

        self.PIECE_NUM2TYPE = {1: 'I', 2: 'O', 3: 'J', 4: 'L', 5: 'Z', 6: 'S', 7: 'T', 8: 'G'}
        self.width = 10
        self.height = 20

        self.current_actions = []

        self.best_genes = [
            # 83.9582, 85.5775, 1.0495, 1.0602, 5.7449, 13.3834, 13.8588, 6.7820, 2.1385, -6.0317, 3.000] # 7 - 3
            0.07997577476430706, 55.03458641831113, 64.10136662551174, 8.980024437134759, 
             92.5343296614591, 84.44831840217519, 56.57232556900489, 
             58.20552431230755, 96.68367418548978, -58.740576957346704, 35.625766277218354]
        self.genes = ['holeCountMultiplier', 'openHoleCountMultiplier', 'maximumLineHeightMultiplier',
                      'addedShapeHeightMultiplier', 'pillarCountMultiplier', 'blocksInRightMostLaneMultiplier',
                      'nonTetrisClearPenalty', 'blocksAboveHolesMultiplier', 'bumpinessMultiplier', 
                      'tetrisRewardMultiplier', 'minMaxDiffMultiplier']

    def state_to_infos(self, state):
        state = np.squeeze(state)
        all_ones_rows = np.all(state == 1, axis=1)
        state[all_ones_rows] = -1
        matrix_block = np.transpose(state[:, :10], (1, 0))  # 10 x 20
        matrix_block = np.where(matrix_block < 1, 0, matrix_block)
        matrix_block = np.transpose(matrix_block)
        all_ones_rows = np.all(matrix_block == 1, axis=1)
        matrix_block[all_ones_rows] = -1
        matrix_block = np.transpose(matrix_block)
        # print(matrix_block)

        feature_vector = state[:, 10:17]
        hold_shape_vector = feature_vector[0]
        next_shape_vector = feature_vector[1:6]
        current_shape_vector = feature_vector[6]

        info_vector = feature_vector[7]
        time_left = feature_vector[-1][-1]

        return matrix_block, hold_shape_vector, next_shape_vector, current_shape_vector, info_vector, time_left

    def vector_to_shape(self, vector):
        for i in range(len(vector)):
            if vector[i] == 1:
                return self.PIECE_NUM2TYPE[i + 1]
        return 0

    def get_line_height(self, matrix_block):
        heights = [0] * 10
        for i in range(10):
            for j in range(20):
                if matrix_block[j][i] == 1:
                    heights[i] = (self.height - j)
                    break

        return heights


    ###########################################
    ####                                   ####
    ####            CALCULATIONS           ####
    ####                                   ####
    ###########################################

    def drop_down(self, grid, piece):
        matrix_block = np.transpose(grid, (1, 0))
        heights = self.get_line_height(matrix_block)
        steps = []

        if piece == 'I':
            for i in range(2):
                # if i == 0:
                #     '''
                #     Chiều dương là từ [dưới lên trên][phải sang trái]

                #     {6, 5, 4, 3} -> cột bắt đầu là 3
                #     [0, 0, 0, 0], 
                #     [4, 3, 2, 1], 
                #     [0, 0, 0, 0], 
                #     [0, 0, 0, 0]

                #     + gridc[20 - 1 - max_height][j] != 1:
                #     Kiểm tra xem vị trí số 1 có trống hay không
                #     + gridc[20 - 1 - max_height][j + 1] != 1:
                #     Kiểm tra xem vị trí số 2 có trống hay không
                #     + gridc[20 - 1 - max_height][j + 2] != 1:
                #     Kiểm tra xem vị trí số 3 có trống hay không
                #     + gridc[20 - 1 - max_height][j + 3] != 1
                #     Kiểm tra xem vị trí số 4 có trống hay không
                #     '''
                #     for j in range(7):
                #         gridc = matrix_block.copy()
                #         sequence = [0]
                #         if (j - 3) < 0:
                #             for shift in range(3 - j): sequence.append(6)
                #         else:
                #             for shift in range(j - 3): sequence.append(5)
                #         max_height = int(max(heights[0 + j:5 + j]))
                #         if  gridc[20 - 1 - max_height][j] != 1 and \
                #             gridc[20 - 1 - max_height][j + 1] != 1 and \
                #             gridc[20 - 1 - max_height][j + 2] != 1 and \
                #             gridc[20 - 1 - max_height][j + 3] != 1:
                #             gridc[20 - 1 - max_height][j] = 1            #   [      4]
                #             gridc[20 - 1 - max_height][j + 1] = 1        #   [1  2  3]
                #             gridc[20 - 1 - max_height][j + 2] = 1
                #             gridc[20 - 1 - max_height][j + 3] = 1
                #         steps.append([sequence, gridc, heights[j] + 1])
                # else:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 5
                    [0, 1, 0, 0], 
                    [0, 1, 0, 0], 
                    [0, 1, 0, 0], 
                    [0, 1, 0, 0]

                    + gridc[20 - 1 - max_height][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[20 - 1 - max_height][j + 1] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[20 - 1 - max_height][j + 2] != 1:
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[20 - 1 - max_height][j + 3] != 1
                    Kiểm tra xem vị trí số 4 có trống hay không
                    '''
                    for j in range(10):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 5) < 0:
                            for shift in range(5 - j): sequence.append(6)
                        else:
                            for shift in range(j - 5): sequence.append(5)
                        for z in range(4):
                            if (z + 1 + heights[j] > 19): break
                            gridc[int(20 - 1 - (heights[j] + z))][int(j)] = 1
                        steps.append([sequence, gridc, heights[j] + 4])

        if piece == 'O':
            for j in range(8):
                sequence = []
                gridc = matrix_block.copy()
                if (j - 5) < 0:
                    for shift in range(5 - j): sequence.append(6)
                else:
                    for shift in range(j - 5): sequence.append(5)
                gridc[20 - 1 - int(max(heights[j:j + 2]))][j] = 1
                gridc[20 - 1 - int(max(heights[j:j + 2]))][j + 1] = 1
                gridc[20 - 1 - int(max(heights[j:j + 2]) + 1)][j] = 1
                gridc[20 - 1 - int(max(heights[j:j + 2]) + 1)][j + 1] = 1

                steps.append([sequence, gridc, max(heights[0 + j:2 + j]) + 2])

        if piece == 'L':
            for i in range(4):
                if i == 0:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 4
                    [0, 0, 0, 0], 
                    [0, 0, 0, 0], 
                    [3, 2, 1, 0], 
                    [4, 0, 0, 0]

                    + gridc[20 - 1 - max_height][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[20 - 1 - max_height][j + 1] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[20 - 1 - max_height][j + 2] != 1:
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j + 2] != 1
                    Kiểm tra xem vị trí số 4 có trống hay không
                    '''
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = []
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:3 + j]))
                        if      gridc[20 - 1 - max_height][j] != 1 and \
                                gridc[20 - 1 - max_height][j + 1] != 1 and \
                                gridc[20 - 1 - max_height][j + 2] != 1 and \
                                gridc[20 - 1 - max_height - 1][j + 2] != 1:
                            gridc[20 - 1 - max_height][j] = 1            #   [      4]
                            gridc[20 - 1 - max_height][j + 1] = 1        #   [1  2  3]
                            gridc[20 - 1 - max_height][j + 2] = 1
                            gridc[20 - 1 - max_height - 1][j + 2] = 1

                            steps.append([sequence, gridc, max(heights[0 + j:3 + j]) + 2])

                if i == 1:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 4
                    [0, 0, 0, 0], 
                    [0, 4, 0, 0], 
                    [0, 3, 0, 0], 
                    [0, 2, 1, 0]

                    + gridc[(20 - 1 - max_height)][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[(20 - 1 - max_height)][j + 1] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[(20 - 1 - max_height + 1)][j + 1] != 1 :
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[(20 - 1 - max_height + 2)][j + 1] != 1:
                    Kiểm tra xem vị trí số 4 có trống hay không

                    [4, .]
                    [3, *]
                    [2, 1] -> tăng lên 2 hàng
                    
                    [4, .]
                    [3, .]
                    [2, 1] -> tăng lên 3 hàng

                    [1, 2]
                    [*, 3]
                    [*, 4] -> tăng lên 1 hàng
                    '''
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max([heights[0 + j], 3, heights[1 + j] + 2])) # 0 + j -> cột bên trái, 3 -> khi thả xuống đất bằng phẳng, 1 + j -> cột bên phải

                        if  gridc[(20 - 1 - max_height)][j] != 1 and \
                            gridc[(20 - 1 - max_height)][j + 1] != 1 and\
                            gridc[(20 - 1 - max_height + 1)][j + 1] != 1 and \
                            gridc[(20 - 1 - max_height + 2)][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[(20 - 1 - max_height + 1)][j + 1] = 1
                            gridc[(20 - 1 - max_height + 2)][j + 1] = 1

                            if heights[j] > heights[j + 1]:
                                if heights[j] - heights[j + 1] == 1:
                                    block_height = heights[j] + 2
                                else:
                                    block_height = heights[j] + 1
                            else:
                                block_height = heights[j + 1] + 3

                            steps.append([sequence, gridc, block_height])

                if i == 2:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 4
                    [0, 0, 0, 0], 
                    [0, 0, 1, 0], 
                    [4, 3, 2, 0], 
                    [0, 0, 0, 0]

                    + gridc[20 - 1 - max_height][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j + 1] != 1:
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j + 2] != 1:
                    Kiểm tra xem vị trí số 4 có trống hay không

                    [., .][., ., 1]
                    [*, *][1, 1, 1] -> tăng lên 1 hàng
                    
                    [., .][., ., 1]
                    [., .][1, 1, 1] -> tăng lên 2 hàng
                    '''
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = [4, 4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:3 + j]))

                        if max_height != heights[0 + j] and (max_height == heights[1 + j] or max_height == heights[2 + j]):
                            max_height -= 1
                        if gridc[20 - 1 - max_height][j] != 1 and \
                                gridc[20 - 1 - max_height - 1][j] != 1 and\
                                gridc[20 - 1 - max_height - 1][j + 1] != 1 and \
                                gridc[20 - 1 - max_height - 1][j + 2] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 2] = 1

                            if heights[j] < heights[j + 1] and heights[j] < heights[j + 2]:
                                block_height = max(heights[j + 1], heights[j + 2]) + 1
                            else:
                                block_height = heights[j] + 2

                            steps.append([sequence, gridc, block_height])

                if i == 3:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 5
                    [0, 0, 0, 0], 
                    [2, 1, 0, 0], 
                    [0, 3, 0, 0], 
                    [0, 4, 0, 0]]

                    + gridc[20 - 1 - max_height][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[20 - 1 - max_height][j + 1] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j] != 1:
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[20 - 1 - max_height - 2][j] != 1:
                    Kiểm tra xem vị trí số 4 có trống hay không
                    '''
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [3]
                        if (j - 5 < 0):
                            for shift in range(5 - j):
                                sequence.append(6)
                        if (j - 5 > 0):
                            for shift in range(j - 5):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:2 + j]))
                        if gridc[20 - 1 - max_height][j] != 1 and \
                                gridc[20 - 1 - max_height][j + 1] != 1 and \
                                gridc[20 - 1 - max_height - 1][j] != 1 and \
                                gridc[20 - 1 - max_height - 2][j] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height - 2][j] = 1

                            steps.append([sequence, gridc, max(heights[0 + j:2 + j]) + 3])

        if piece == 'J':
            for i in range(4):
                if i == 0:
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = []
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        if gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j] != 1 and \
                                gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j + 1] != 1 and \
                                gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j + 2] != 1 and \
                                gridc[20 - 1 - int(max(heights[0 + j:3 + j]) + 1)][j] != 1:
                            gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j] = 1
                            gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j + 1] = 1
                            gridc[20 - 1 - int(max(heights[0 + j:3 + j]))][j + 2] = 1
                            gridc[20 - 1 - int(max(heights[0 + j:3 + j]) + 1)][j] = 1

                            steps.append([sequence, gridc, max(heights[0 + j:3 + j]) + 2])

                if i == 1:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [3]
                        if (j - 5) < 0:
                            for shift in range(5 - j):
                                sequence.append(6)
                        if (j - 5) > 0:
                            for shift in range(j - 5):
                                sequence.append(5)

                        max_height = int(max(heights[0 + j], heights[1 + j] - 2))

                        if gridc[(20 - 1 - max_height)][j] != 1 and gridc[(20 - 1 - max_height - 1)][j] != 1 and \
                                gridc[(20 - 1 - max_height - 2)][j] != 1 and gridc[(20 - 1 - max_height - 2)][j + 1] != 1 and (
                                max_height + 2) >= heights[j + 1]:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height - 2][j] = 1
                            gridc[20 - 1 - max_height - 2][j + 1] = 1

                            if heights[j] < heights[j + 1]:
                                if heights[j] - heights[j + 1] == -1:
                                    block_height = heights[j + 1] + 2
                                else:
                                    block_height = heights[j + 1] + 1
                            else:
                                block_height = heights[j + 1] + 3

                            steps.append([sequence, gridc, block_height])

                if i == 2:
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = [4, 4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:3 + j]))
                        if max_height != heights[2 + j] and (max_height == heights[1 + j] or max_height == heights[0 + j]):
                            max_height -= 1
                        if gridc[20 - 1 - max_height][j + 2] != 1 and gridc[20 - 1 - max_height - 1][j + 1] != 1 and \
                                gridc[20 - 1 - max_height - 1][j + 2] != 1 and gridc[20 - 1 - max_height - 1][j] != 1:
                            gridc[20 - 1 - max_height][j + 2] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 2] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1

                            if heights[j + 2] < heights[j + 1] and heights[j + 2] < heights[j]:
                                block_height = max(heights[j + 1], heights[j]) + 1
                            else:
                                block_height = heights[j + 2] + 2

                            steps.append([sequence, gridc, block_height])

                if i == 3:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 4 < 0):
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4 > 0):
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:2 + j]))
                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height - 1][
                            j + 1] != 1 and gridc[20 - 1 - max_height - 2][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height - 2][j + 1] = 1

                            steps.append([sequence, gridc, max(heights[0 + j:2 + j]) + 3])

        if piece == 'S':
            for i in range(2):
                if i == 0:
                    '''
                    Chiều dương là từ [dưới lên trên][phải sang trái]

                    {6, 5, 4, 3} -> cột bắt đầu là 4
                    [0, 0, 0, 0], 
                    [0, 2, 1, 0], 
                    [4, 3, 0, 0], 
                    [0, 0, 0, 0]

                    + gridc[20 - 1 - max_height][j] != 1:
                    Kiểm tra xem vị trí số 1 có trống hay không
                    + gridc[20 - 1 - max_height][j + 1] != 1:
                    Kiểm tra xem vị trí số 2 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j + 1] != 1:
                    Kiểm tra xem vị trí số 3 có trống hay không
                    + gridc[20 - 1 - max_height - 1][j + 2] != 1:
                    Kiểm tra xem vị trí số 4 có trống hay không
                    '''
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = []
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j], heights[1 + j], (heights[2 + j] - 1)))
                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height - 1][
                            j + 1] != 1 and gridc[20 - 1 - max_height - 1][j + 2] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 2] = 1

                            if heights[j] < heights[j + 2] and heights[j + 1] < heights[j + 2]:
                                block_height = heights[j + 2] + 1
                            else:
                                block_height = max(heights[j], heights[j + 1]) + 2

                            steps.append([sequence, gridc, block_height])

                if i == 1:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max([heights[0 + j], heights[1 + j] + 1]))
                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height - 1][
                            j] != 1 and gridc[20 - 1 - max_height + 1][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height + 1][j + 1] = 1

                            if heights[j] <= heights[j + 1]:
                                block_height = heights[j + 1] + 3
                            else:
                                block_height = heights[j] + 2

                            steps.append([sequence, gridc, block_height])

        if piece == 'Z':
            for i in range(2):
                if i == 0:
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = []
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max([heights[0 + j], 1 + heights[1 + j], 1 + heights[2 + j]]))

                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height + 1][
                            j + 1] != 1 and gridc[20 - 1 - max_height + 1][j + 2] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height + 1][j + 1] = 1
                            gridc[20 - 1 - max_height + 1][j + 2] = 1

                            if heights[j + 2] < heights[j] and heights[j + 1] < heights[j]:
                                block_height = heights[j] + 1
                            else:
                                block_height = max(heights[j + 2], heights[j + 1]) + 2

                            steps.append([sequence, gridc, block_height])

                if i == 1:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max([heights[0 + j], heights[1 + j] - 1]))
                        if gridc[int(20 - 1 - max_height)][j] != 1 and gridc[int(20 - 1 - max_height - 1)][j] != 1 and \
                                gridc[int(20 - 1 - max_height - 1)][j + 1] != 1 and gridc[int(20 - 1 - max_height - 2)][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height - 2][j + 1] = 1

                            if heights[j] < heights[j + 1]:
                                block_height = heights[j + 1] + 2
                            else:
                                block_height = heights[j] + 3

                            steps.append([sequence, gridc, block_height])

        if piece == "T":
            for i in range(4):
                if i == 0:
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = []
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max(heights[0 + j:3 + j]))
                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height][
                            j + 2] != 1 and gridc[20 - 1 - max_height - 1][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height][j + 2] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1

                            steps.append([sequence, gridc, max(heights[0 + j:3 + j]) + 2])

                if i == 1:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)
                        max_height = int(max([heights[j + 0], heights[j + 1] + 1]))

                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height - 1][
                            j + 1] != 1 and gridc[20 - 1 - max_height + 1][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1
                            gridc[20 - 1 - max_height + 1][j + 1] = 1

                            if heights[j] > heights[j + 1]:
                                block_height = heights[j] + 2
                            else:
                                block_height = heights[j + 1] + 3

                            steps.append([sequence, gridc, block_height])

                if i == 2:
                    for j in range(8):
                        gridc = matrix_block.copy()
                        sequence = [4, 4]
                        if (j - 4) < 0:
                            for shift in range(4 - j):
                                sequence.append(6)
                        if (j - 4) > 0:
                            for shift in range(j - 4):
                                sequence.append(5)

                        max_height = int(max([heights[j], heights[j + 1] + 1, heights[j + 2]]))
                        if gridc[20 - 1 - max_height][j + 1] != 1 and gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height][
                            j + 2] != 1 and gridc[20 - 1 - max_height + 1][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height][j + 1] = 1
                            gridc[20 - 1 - max_height][j + 2] = 1
                            gridc[20 - 1 - max_height + 1][j + 1] = 1

                            if heights[j + 1] < heights[j] and heights[j + 1] < heights[j + 2]:
                                block_height = max(heights[j], heights[j + 2]) + 1
                            else:
                                block_heights = heights[j + 1] + 2

                            steps.append([sequence, gridc, block_height])

                if i == 3:
                    for j in range(9):
                        gridc = matrix_block.copy()
                        sequence = [3]
                        if (j - 5) < 0:
                            for shift in range(5 - j):
                                sequence.append(6)
                        if (j - 5) > 0:
                            for shift in range(j - 5):
                                sequence.append(5)

                        max_height = int(max([heights[j], heights[j + 1] - 1]))
                        if gridc[20 - 1 - max_height][j] != 1 and gridc[20 - 1 - max_height - 1][j] != 1 and gridc[20 - 1 - max_height - 2][
                            j] != 1 and gridc[20 - 1 - max_height - 1][j + 1] != 1:
                            gridc[20 - 1 - max_height][j] = 1
                            gridc[20 - 1 - max_height - 1][j] = 1
                            gridc[20 - 1 - max_height - 2][j] = 1
                            gridc[20 - 1 - max_height - 1][j + 1] = 1

                            if heights[j] >= heights[j + 1]:
                                block_height = heights[j] + 3
                            else:
                                block_height = heights[j + 1] + 2

                            steps.append([sequence, gridc, block_height])
        # print(steps[0])
        return steps
    
    ###########################################
    ####                                   ####
    ####                                   ####
    ####                                   ####
    ###########################################

    def count_holes(self, matrix_block):
        hole_count = 0
        open_hole_count = 0
        #     an open hole is one which isnt fully covered, like there isnt a block to the left or right,
        #     open holes are less bad than normal holes because you can slip a piece in there.
        #     actually an open hole needs 2 spots to a side to be able to be filled.
        blocks_above_holes = 0

        for i in range(self.width):
            block_found = False
            number_of_blocks_found = 0

            # going down each column look for a block and once found each block below is a hole
            for j in range(self.height):
                if matrix_block[i][j] != 0:
                    block_found = True
                    number_of_blocks_found += 1
                elif block_found:
                    blocks_above_holes += number_of_blocks_found

                    # if i < self.width - 2:
                    #     # check if there is 2 spaces to the right
                    #     if matrix_block[i + 1][j] == 0 and matrix_block[i + 2][j] == 0:
                    #         if j == self.height - 1 or matrix_block[i + 1][j + 1] != 0:
                    #             open_hole_count += 1
                    #             continue

                    # if i >= 2:
                    #     # check to the left
                    #     if matrix_block[i - 1][j] == 0 and matrix_block[i - 2][j] == 0:
                    #         if j == self.height - 1 or matrix_block[i - 1][j + 1] != 0:
                    #             open_hole_count += 1
                    #             continue
                    # if reached this point then the hole is a full hole
                    hole_count += 1
        return hole_count, open_hole_count, blocks_above_holes

    def calc_max_line_height(self, matrix_block):
        max_line_height = 0
        for i in range(self.width):
            for j in range(self.height):
                if matrix_block[i][j] == 1:
                    max_line_height = max(max_line_height, self.height - j)
                    break

        return max_line_height

    def count_pillars(self, matrix_block):
        pillar_cnt = 0
        for i in range(self.width):
            current_pillar_height_L = 0
            current_pillar_height_R = 0

            for j in reversed(range(self.height - 1)):
                if (i > 0 and matrix_block[i][j] != 0) and matrix_block[i - 1][j] == 0:
                    current_pillar_height_L += 1
                else:
                    if current_pillar_height_L >= 3:
                        pillar_cnt += current_pillar_height_L
                    current_pillar_height_L = 0

                if (i < self.width - 2 and matrix_block[i][j] != 0 and matrix_block[i + 1][j] == 0):
                    current_pillar_height_R += 1
                else:
                    if current_pillar_height_R >= 3:
                        pillar_cnt += current_pillar_height_R
                    current_pillar_height_R = 0

            if current_pillar_height_R >= 3:
                pillar_cnt += current_pillar_height_R
            if current_pillar_height_L >= 3:
                pillar_cnt += current_pillar_height_L

        return pillar_cnt

    def count_number_of_block_in_right_lane(self, matrix_block):
        blocks_in_right_lane = 0
        for j in range(self.height):
            if matrix_block[self.width - 1][j] != 0:
                blocks_in_right_lane += 1

        return blocks_in_right_lane

    def calc_bumpiness(self, matrix_block):
        bumpiness = 0
        previous_line_height = 0

        for i in range(self.width - 1):
            for j in range(self.height):
                if matrix_block[i][j] != 0:
                    current_line_height = self.height - j
                    if i != 0:
                        bumpiness += abs(previous_line_height - current_line_height)
                    previous_line_height = current_line_height
                    break

        return bumpiness
    
    def calc_min_max_diff(self, matrix_block):
        mn, mx = 1000000000, 0

        for i in range(self.width):
            for j in range(self.height):
                if matrix_block[i][j] != 0:
                    current_line_height = self.height - j
                    mn = min(mn, current_line_height)
                    mx = max(mx, current_line_height)

        return mx - mn

    def clear_lines(self, matrix_block):
        cleared = 0
        matrix_block = matrix_block.tolist()
        for y in reversed(range(self.height)):
            y = -(y + 1)
            row = 0
            for x in range(self.width):
                if matrix_block[x][y] == 1:
                    row += 1

            if row == self.width:
                cleared += 1
                for i in range(self.width):
                    del matrix_block[i][y]
                    matrix_block[i] = [0] + matrix_block[i]

        return np.array(matrix_block), cleared

    def calc_cost(self, matrix_block, block_height):
        dict_genes = {key: value for key, value in zip(self.genes, self.best_genes)}

        matrix_block, line_cleared = self.clear_lines(matrix_block)
        hole_cnt, open_hole_cnt, blocks_above_holes = self.count_holes(matrix_block)
        max_line_height = self.calc_max_line_height(matrix_block)
        pillar_cnt = self.count_pillars(matrix_block)
        block_in_right_lane = self.count_number_of_block_in_right_lane(matrix_block)
        bumpiness = self.calc_bumpiness(matrix_block)
        min_max_diff = self.calc_max_line_height(matrix_block)

        lines_clear_which_arent_tetrises = 1 if (line_cleared > 0 and line_cleared < 4) else 0
        tetrises = 1 if line_cleared == 4 else 0

        nonTetrisClearPenalty = dict_genes['nonTetrisClearPenalty']
        blocksInRightMostLaneMultiplier = dict_genes['blocksInRightMostLaneMultiplier']
        minMaxDiffMultiplier = dict_genes['minMaxDiffMultiplier']

        if min_max_diff > 8 or hole_cnt > 0 or pillar_cnt > 10:
            nonTetrisClearPenalty = 0
            blocksInRightMostLaneMultiplier = 0

        if max_line_height > 16:
            max_line_height **= 5
            min_max_diff **= 3

        return (dict_genes['holeCountMultiplier'] * hole_cnt +
                dict_genes['openHoleCountMultiplier'] * open_hole_cnt +
                dict_genes['maximumLineHeightMultiplier'] * max_line_height +
                dict_genes['pillarCountMultiplier'] * pillar_cnt +
                blocksInRightMostLaneMultiplier * block_in_right_lane +
                nonTetrisClearPenalty * lines_clear_which_arent_tetrises +
                dict_genes['blocksAboveHolesMultiplier'] * blocks_above_holes +
                dict_genes['bumpinessMultiplier'] * bumpiness +
                dict_genes['addedShapeHeightMultiplier'] * block_height +
                dict_genes['tetrisRewardMultiplier'] * tetrises + 
                minMaxDiffMultiplier * min_max_diff), line_cleared

    def find_best_movement_plan(self, all_matrix_block):
        min_holes = 10000
        min_holes_matrix = []

        for [actions, matrix, shape_height] in all_matrix_block:
            matrix = np.transpose(matrix, (1, 0))
            matrix_holes = self.count_holes(matrix)[0]
            if matrix_holes < min_holes:
                min_holes = matrix_holes

        for [actions, matrix, shape_height] in all_matrix_block:
            matrix = np.transpose(matrix, (1, 0))
            matrix_holes = self.count_holes(matrix)[0]

            if matrix_holes == min_holes:
                min_holes_matrix.append([actions, matrix, shape_height])

        min_score = 1e9
        min_score_matrix_actions = []
        min_score_matrix_line_cleared = 0

        for [actions, matrix, shape_height] in min_holes_matrix:
            score, line_cleared = self.calc_cost(matrix, shape_height)
            if min_score > score:
                min_score = score
                min_score_matrix_actions = actions
                min_score_matrix_line_cleared = line_cleared
        return min_score_matrix_actions, min_score_matrix_line_cleared

    def calc_best_movement_plan(self, state):
        matrix_block, hold_block_vector, next_blocks_vector, current_block_vector, _, _ = self.state_to_infos(state)
        current_shape = self.vector_to_shape(current_block_vector)
        hold_shape = self.vector_to_shape(hold_block_vector)
        next_shape = self.vector_to_shape(next_blocks_vector[0])

        candidates_shape = {
            0: current_shape,
            1: hold_shape if hold_shape != 0 else next_shape
        }

        all_possible_matrix_block_shape = []
        for hold, shape in candidates_shape.items():
            end_matrix_block_shape = self.drop_down(matrix_block, shape)
            if hold == 1:
                for actions in end_matrix_block_shape:
                    actions[0] = [1] + actions[0]
            all_possible_matrix_block_shape += end_matrix_block_shape

        best_actions, best_line_cleared = self.find_best_movement_plan(all_possible_matrix_block_shape)

        self.line_cleared = best_line_cleared

        return best_actions

    def get_actions(self, state):
        actions = self.calc_best_movement_plan(state)
        actions.append(2)
        return actions

    def choose_action(self, state):
        if len(self.current_actions) > 0:
            self.line_cleared = 0
            return self.current_actions.pop(0)
        else:
            self.current_actions = self.get_actions(state)
            return self.current_actions.pop(0)