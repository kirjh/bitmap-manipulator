import numpy as np

def clamp(n, low, high):
  return max(min(n, high), low)

def convert_to_YUV(tuple):
  tuple = tuple / 255

  conv_matrix = np.array([[ 0.299,  0.587,  0.114],
                          [-0.299, -0.587,  0.886],
                          [ 0.701, -0.587, -0.114]])
  
  conv_matrix = np.multiply(conv_matrix, tuple)
  y = np.sum(conv_matrix[0])
  u = np.sum(conv_matrix[1])
  v = np.sum(conv_matrix[2])
  return np.array((y,u,v))

def convert_to_RGB(tuple):
  tuple = tuple

  conv_matrix = np.array([[ 1,      0,       1],
                          [ 1, -0.194,  -0.509],
                          [ 1,      1,       0]])
  
  conv_matrix = np.multiply(conv_matrix, tuple)
  r = int(clamp(np.sum(conv_matrix[0]) * 255, 0, 255))
  g = int(clamp(np.sum(conv_matrix[1]) * 255, 0, 255))
  b = int(clamp(np.sum(conv_matrix[2]) * 255, 0, 255))
  return np.array((r,g,b))