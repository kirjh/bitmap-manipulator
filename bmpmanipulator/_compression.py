import math
import time
import tkinter as tk
from tkinter.filedialog import asksaveasfilename

# header (10 bytes)
# title (2 bytes)
# index size (4 bytes)
# body size (4 bytes)
# ---
# body 
def to_bits(value, bits=8):
  if isinstance(value, str):
    return ''.join(f"{str:=0{bits}b}" for str in bytearray(value.encode("utf-8")))
  elif isinstance(value, int):
    return f"{value:=0{bits}b}"

def compress(self):
  try:
    with open(self.file_path.get(), "rb") as f:
      try:
        img_bytes = f.read()
        if img_bytes[0:2].decode("utf-8") != "BM":
          raise Exception()
      except:
        tk.messagebox.showerror("Error", "Invalid file type.")
        return

      start_time = time.perf_counter()

      dictionary = {}
      for i in range(256):
        dictionary[bytes([i])] = i
      
      result = []
      max = 0
      init_byte = b""
      
      for byte in img_bytes:
        new_byte = init_byte + bytes([byte])
        # if symbol exists
        if dictionary.get(new_byte):
          init_byte = new_byte
        # if symbol doesn't exist
        else:
          result.append(dictionary[init_byte])
          if dictionary[init_byte] > max:
            max = dictionary[init_byte]
          dictionary[new_byte] = len(dictionary.keys())
          init_byte = bytes([byte])
      result.append(dictionary[init_byte])
      if dictionary[init_byte] > max:
        max = dictionary[init_byte]

      index_bits = math.ceil(math.log(max, 2))
      # create header
      bit_string = to_bits("CM") + f'{index_bits:032b}' + f'{len(result):032b}'
      # add index bits
      for bits in result:
        bit_string += to_bits(bits, index_bits)
      # add padding
      bit_string = bit_string + "0"*(8-(len(bit_string) % 8))
      hex_array = b''
      #convert to hex
      for i in range(int(len(bit_string) / 8)):
        hex_array += bytes([int(bit_string[i*8:(i+1)*8], 2)])

      end_time = time.perf_counter() - start_time
      
      try:
        files = [('CMPT365 Compressed File', '*.cmpt365')]
        file_path = asksaveasfilename(filetypes = files, defaultextension = files)
        start_time = time.perf_counter()
        with open(file_path, 'wb') as file:
          file.write(hex_array)
        end_time = time.perf_counter() - start_time + end_time
      except:
        tk.messagebox.showerror("Error", "Compressed image was not saved.")
        return
      
      self.img_size.set(int.from_bytes(img_bytes[2:6], 'little')) # old size
      self.new_img_size.set(len(hex_array)) # new size
      self.ratio.set(f'{(self.img_size.get() / self.new_img_size.get()):.4f}')
      self.time.set(round(end_time * 1000))
      
      self.editor_frame.pack_forget()
      self.compress_frame.pack()

      return
  except:
    tk.messagebox.showerror("Error", "Invalid file path.")

def decompress(self):
  try:
    with open(self.file_path.get(), "rb") as f:
      try:
        img_bytes = f.read()
        if img_bytes[0:2].decode("utf-8") != "CM":
          raise Exception()
      except:
        tk.messagebox.showerror("Error", "Invalid file type.")
        return
    header_index = int.from_bytes(img_bytes[2:6], 'big')
    body_size = int.from_bytes(img_bytes[6:10], 'big')

    dictionary = {}
    for i in range(256):
      dictionary[i] = bytes([i])
    
    bit_string = ''.join(f'{byte:08b}' for byte in img_bytes[10:])
    
    init_index = dictionary[int(bit_string[0:header_index], 2)]
    result = []
    result.append(init_index)
    i = 1
    for index in range(body_size-1):
      index = int(bit_string[header_index*i:header_index*(i+1)], 2)
      i += 1
      
      if dictionary.get(index):
        output = dictionary[index]
        dictionary[len(dictionary.keys())] = init_index + bytes([output[0]])
      else:
        output = init_index + bytes([init_index[0]])
        dictionary[len(dictionary.keys())] = output
      result.append(output)
      init_index = output
    img_data = b"".join(result)

    self.parse_image(img_data)
  except:
      tk.messagebox.showerror("Error", "Invalid file path.")