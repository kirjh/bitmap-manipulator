import tkinter as tk
from tkinter.filedialog import askopenfilename
from time import sleep
from threading import Thread

def browse_file():
  filepath = askopenfilename()
  path_entry.delete(0, tk.END)
  path_entry.insert(0, filepath)

def clear_path():
  path_entry.delete(0, tk.END)

def read_file():
  #try:
  with open(file_path.get(), "rb") as f:
    try:
      img_bytes = f.read()
      if img_bytes[0:2].decode("utf-8") != "BM":
        raise Exception()
    except:
      tk.messagebox.showerror("Error", "Invalid file type.")
      return
    img_size.set(int.from_bytes(img_bytes[2:6], 'little')) # size
    img_width.set(int.from_bytes(img_bytes[18:22], 'little')) # width
    img_height.set(int.from_bytes(img_bytes[22:26], 'little')) # height
    img_depth.set(int.from_bytes(img_bytes[28:30], 'little')) # bit depth
    a = int.from_bytes(img_bytes[10:14], 'little')
    b = int.from_bytes(img_bytes[2:6], 'little')
    print(a)
    print(b)
    print(img_bytes[a:])
    
    return
  #except:
  #  tk.messagebox.showerror("Error", "Invalid file path.")

def start_read():
  Thread(target=read_file).start()

root = tk.Tk()
# define variables
file_path = tk.StringVar()
img_size = tk.IntVar()
img_width = tk.IntVar()
img_height = tk.IntVar()
img_depth = tk.IntVar()

# define frames
browse_frame = tk.Frame(root)
load_frame = tk.Frame(root)
data_frame = tk.Frame(root)

browse_frame.pack()
data_frame.pack(side=tk.BOTTOM)
load_frame.pack(side=tk.BOTTOM)

var = 0

# browse file
tk.Label(browse_frame, text="File Path").pack(side=tk.LEFT)
path_entry = tk.Entry(browse_frame, width=30, textvariable=file_path)
path_entry.pack(side=tk.LEFT)
tk.Button(browse_frame, text="Browse", command=browse_file).pack(side=tk.LEFT)
# open file
tk.Button(load_frame, text="Read File", command=start_read).pack()
# file details
tk.Label(data_frame, text="Size").grid(row=0, column=0)
tk.Label(data_frame, textvariable=img_size).grid(row=0, column=1)
tk.Label(data_frame, text="Width").grid(row=1, column=0)
tk.Label(data_frame, textvariable=img_width).grid(row=1, column=1)
tk.Label(data_frame, text="Height").grid(row=2, column=0)
tk.Label(data_frame, textvariable=img_height).grid(row=2, column=1)
tk.Label(data_frame, text="Bits Per Pixel").grid(row=3, column=0)
tk.Label(data_frame, textvariable=img_depth).grid(row=3, column=1)


root.mainloop()