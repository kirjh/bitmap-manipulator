import numpy as np
import math
import tkinter as tk

def parse_image(self):
  # parse image as a byte array
  try:
    with open(self.file_path.get(), "rb") as f:
      # attempt to read file
      # if file header does not match or if file is unreadable throw 'invalid file type'
      try:
        img_bytes = f.read()
        if img_bytes[0:2].decode("utf-8") != "BM":
          raise Exception()
      except:
        tk.messagebox.showerror("Error", "Invalid file type.")
        return
      # decode byte array
      self.img_size.set(int.from_bytes(img_bytes[2:6], 'little')) # size
      self.img_width.set(int.from_bytes(img_bytes[18:22], 'little')) # width
      self.img_height.set(int.from_bytes(img_bytes[22:26], 'little')) # height
      self.img_bits.set(int.from_bytes(img_bytes[28:30], 'little')) # bits per pixel
      self.bitmap = img_bytes[int.from_bytes(img_bytes[10:14], 'little'):] # pixel bitmap
      
      # construct colour table, if applicable
      # image parse function depends on whether colour table exists
      if (self.img_bits.get() <= 8):
        self.colour_table = []
        # at 1 bit we have 2 values to work with
        for x in range(max(2,2 ** self.img_bits.get())):
          self.colour_table.append((img_bytes[56 + 4*x], img_bytes[55 + 4*x], img_bytes[54 + 4*x]))

      self.parse_bitmap()

      self.lum_scale['state'] = 'normal'
      self.red_button['state'] = 'normal'
      self.green_button['state'] = 'normal'
      self.blue_button['state'] = 'normal'
      self.perf_button['state'] = 'normal'

      return
  except:
    tk.messagebox.showerror("Error", "Invalid file path.")

def parse_bitmap(self):
  # read bitmap into a 2D array
  array = np.zeros((self.img_height.get(), self.img_width.get(), 3), dtype=np.uint8)
  # padding
  bytes_per_line = math.ceil(self.img_width.get() / (8 / self.img_bits.get()))
  if (bytes_per_line % 4 != 0):
    bytes_per_line += 4 - (bytes_per_line % 4)
  for h in range(self.img_height.get()):
    # row inverse: start at bottom and multiply by length of width to increase height
    row = (self.img_height.get() - h - 1) * bytes_per_line
    for w in range(self.img_width.get()):
      if (self.img_bits.get() <= 8):
        # Case 1: 8 bits or less
        # byte_index rounds down to stay on a byte until all bits are parsed
        # bit_index keeps track of which bit group is being parsed
        # code is dynamic and self-adjusts to the number of bits/byte
        byte_index = row + (w // (8 // self.img_bits.get()))
        bit_index = (8-self.img_bits.get()) - (w * self.img_bits.get() % 8)
        # bit shift and mask to obtain only the bits we want
        bit_val = (self.bitmap[byte_index] >> bit_index) & ((1 << self.img_bits.get()) - 1 )
        array[h, w] = self.colour_table[bit_val]
      else:
        # Case 2: 24 bits
        # colours inverse: each byte is a colour in BGR format
        byte_index = row + (w * 3)
        array[h,w] = (self.bitmap[byte_index+2], self.bitmap[byte_index+1], self.bitmap[byte_index])
      
  self.pixel_array = array
  self.render_image(self.pixel_array)
  return