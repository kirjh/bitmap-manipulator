from ._conversions import convert_to_YUV, convert_to_RGB
import numpy as np

def adjust_brightness(self, event):
  if self.perf.get() == 1:
    self.adjust_all()
    return
  array = np.zeros((self.img_height.get(), self.img_width.get(), 3), dtype=np.uint8)
  for h in range(self.img_height.get()):
    for w in range(self.img_width.get()):
      temp = convert_to_YUV(self.pixel_array[h,w])
      temp[0] = temp[0] * (int(event)/50)
      array[h,w] = convert_to_RGB(temp)
  self.render_image(array)
  return

def toggle_button(self):
  if self.perf.get() == 1:
    self.adjust_all()
    return
  array = np.zeros((self.img_height.get(), self.img_width.get(), 3), dtype=np.uint8)
  mask = np.array((self.red.get(), self.green.get(), self.blue.get()))
  for h in range(self.img_height.get()):
    for w in range(self.img_width.get()):
      array[h,w] = np.multiply(self.pixel_array[h,w], mask)
  self.render_image(array)
  return

def adjust_size(self, scale):
  if self.perf.get() == 1:
    self.adjust_all()
    return
  height = int(self.img_height.get() * self.scale.get() / 100)
  width = int(self.img_width.get() * self.scale.get() / 100)
  array = np.zeros((height, width, 3), dtype=np.uint8)
  for h in range(height):
    for w in range(width):
      array[h,w] = self.pixel_array[int(h / (self.scale.get()/100)),int(w / (self.scale.get()/100))]

  self.render_image(array)
  return

def adjust_all(self, event=0):
  height = int(self.img_height.get() * self.scale.get() / 100)
  width = int(self.img_width.get() * self.scale.get() / 100)
  mask = np.array((self.red.get(), self.green.get(), self.blue.get()))
  array = np.zeros((height, width, 3), dtype=np.uint8)
  for h in range(height):
    for w in range(width):
      # nearest neighbour for scaling
      array[h,w] = self.pixel_array[int(h / (self.scale.get()/100)),int(w / (self.scale.get()/100))]
      # colour channel masking
      array[h,w] = np.multiply(array[h,w], mask)
      # YUV conversions for brightness manipulation
      temp = convert_to_YUV(array[h,w])
      temp[0] = temp[0] * (self.lum.get()/50)
      array[h,w] = convert_to_RGB(temp)
  
  self.render_image(array)
  return
