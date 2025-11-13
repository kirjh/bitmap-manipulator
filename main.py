import tkinter as tk
from tkinter.filedialog import askopenfilename
import numpy as np
import math
from PIL import Image, ImageTk
from conversions import *

class BMPParserApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Bitmap Parser")

    # define frames
    self.browse_frame = tk.Frame(root)
    self.load_frame = tk.Frame(root)
    self.data_frame = tk.Frame(root)
    self.image_frame = tk.Frame(root)
    self.slider_frame = tk.Frame(root)
    self.button_frame = tk.Frame(root)
    self.bottom_frame = tk.Frame(root)

    self.browse_frame.pack(padx=10, pady=[10, 0])
    self.load_frame.pack(pady=[0, 10])
    self.data_frame.pack()
    self.image_frame.pack()
    self.slider_frame.pack()
    self.button_frame.pack()
    self.bottom_frame.pack(pady=[0, 10])
    # image frame
    self.image = None
    self.image_label = tk.Label(self.image_frame)
    self.image_label.pack(padx=10, pady=10)

    # define variables
    self.file_path = tk.StringVar()
    self.img_size = tk.IntVar()
    self.img_width = tk.IntVar()
    self.img_height = tk.IntVar()
    self.img_bits = tk.IntVar()
    self.img_offset = tk.IntVar()

    self.red = tk.IntVar()
    self.green = tk.IntVar()
    self.blue = tk.IntVar()

    self.perf = tk.IntVar()

    self.colour_table = None
    self.bitmap = None
    self.pixel_array = None

    # browse file
    tk.Label(self.browse_frame, text="File Path").pack(side=tk.LEFT)
    self.path_entry = tk.Entry(self.browse_frame, width=30, textvariable=self.file_path)
    self.path_entry.pack(side=tk.LEFT)
    tk.Button(self.browse_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)
    # open file
    tk.Button(self.load_frame, text="Parse Bitmap", command=self.parse_image).pack()
    # display file details
    tk.Label(self.data_frame, text="File Size").grid(row=0, column=0)
    tk.Label(self.data_frame, textvariable=self.img_size).grid(row=0, column=1)
    tk.Label(self.data_frame, text="Width").grid(row=1, column=0)
    tk.Label(self.data_frame, textvariable=self.img_width).grid(row=1, column=1)
    tk.Label(self.data_frame, text="Height").grid(row=2, column=0)
    tk.Label(self.data_frame, textvariable=self.img_height).grid(row=2, column=1)
    tk.Label(self.data_frame, text="Bits Per Pixel").grid(row=3, column=0)
    tk.Label(self.data_frame, textvariable=self.img_bits).grid(row=3, column=1)
    # sliders
    tk.Label(self.slider_frame, text="Brightness").grid(row=0, column=0)
    self.lum = tk.IntVar()
    self.lum.set(50)
    self.lum_scale = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=self.adjust_brightness, variable=self.lum)
    self.lum_scale.grid(row=1, column=0)
    tk.Label(self.slider_frame, text="Scale").grid(row=0, column=1)
    self.scale = tk.IntVar()
    self.scale.set(100)
    self.size_scale = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=self.adjust_size, variable=self.scale)
    self.size_scale.grid(row=1, column=1)
    # buttons
    self.red_button = tk.Checkbutton(self.button_frame, text="Red", state='disabled', command=self.toggle_button, variable=self.red)
    self.red_button.select()
    self.red_button.grid(row=0, column=0)
    self.green_button = tk.Checkbutton(self.button_frame, text="Green", state='disabled', command=self.toggle_button, variable=self.green)
    self.green_button.select()
    self.green_button.grid(row=0, column=1)
    self.blue_button = tk.Checkbutton(self.button_frame, text="Blue", state='disabled', command=self.toggle_button, variable=self.blue)
    self.blue_button.select()
    self.blue_button.grid(row=0, column=2)
    self.perf_button = tk.Checkbutton(self.bottom_frame, text="Advanced editing (Performance warning)", state='disabled', variable=self.perf)
    self.perf_button.pack()
    return
  
  def browse_file(self):
    # browse file explorer
    filepath = askopenfilename()
    self.path_entry.delete(0, tk.END)
    self.path_entry.insert(0, filepath)
    return
  
  def render_image(self, array):
    self.image = ImageTk.PhotoImage(Image.fromarray(array))
    self.image_label.configure(image=self.image)
    return

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



root = tk.Tk()
app = BMPParserApp(root)
root.mainloop()