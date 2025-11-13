import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

class bitmapManipulator:
  from ._image import parse_image, parse_bitmap
  from ._adjustments import adjust_brightness, adjust_size, adjust_all, toggle_button

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