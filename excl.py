import tkinter as tk
from PIL import Image, ImageTk
import io

class FileImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image from File Byte Array")
        
        self.photo_image = None
        
        self.load_button = tk.Button(root, text="Load Image from File", 
                                   command=self.load_from_file)
        self.load_button.pack(pady=10)
        
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
    
    def load_from_file(self):
        import tkinter.filedialog as filedialog
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            # Read file as byte array
            with open(file_path, 'rb') as file:
                image_bytes = file.read()
            
            # Convert to PIL Image and then to PhotoImage
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Resize if too large for display
            if pil_image.width > 400 or pil_image.height > 400:
                pil_image = pil_image.resize((400, 400), Image.Resampling.LANCZOS)
            
            self.photo_image = ImageTk.PhotoImage(pil_image)
            self.image_label.configure(image=self.photo_image)

root = tk.Tk()
app = FileImageApp(root)
root.mainloop()