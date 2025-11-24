import customtkinter as ctk
from tkinter import filedialog
import threading
import json
import os
import time
from uploaders.youtube import upload_youtube
from uploaders.instagram import upload_instagram
from uploaders.facebook import upload_facebook
from uploaders.tiktok import upload_tiktok

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CrossPostApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cross Post App")
        self.geometry("600x500")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=0) # Video Select
        self.grid_rowconfigure(2, weight=1) # Caption
        self.grid_rowconfigure(3, weight=0) # Platforms
        self.grid_rowconfigure(4, weight=0) # Upload Button
        self.grid_rowconfigure(5, weight=0) # Status

        # Title
        self.label_title = ctk.CTkLabel(self, text="Cross Post Video Uploader", font=("Arial", 20, "bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=20)

        # Video Selection
        self.frame_video = ctk.CTkFrame(self)
        self.frame_video.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_select_video = ctk.CTkButton(self.frame_video, text="Select Video", command=self.select_video)
        self.btn_select_video.pack(side="left", padx=10, pady=10)
        
        self.label_video_path = ctk.CTkLabel(self.frame_video, text="No video selected")
        self.label_video_path.pack(side="left", padx=10, pady=10)
        
        self.video_path = None

        # Caption
        self.label_caption = ctk.CTkLabel(self, text="Caption:")
        self.label_caption.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.textbox_caption = ctk.CTkTextbox(self, height=100)
        self.textbox_caption.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")

        # Platforms Checkboxes
        self.frame_platforms = ctk.CTkFrame(self)
        self.frame_platforms.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.check_youtube = ctk.CTkCheckBox(self.frame_platforms, text="YouTube")
        self.check_youtube.pack(side="left", padx=10, pady=10)
        self.check_youtube.select()
        
        self.check_instagram = ctk.CTkCheckBox(self.frame_platforms, text="Instagram")
        self.check_instagram.pack(side="left", padx=10, pady=10)
        self.check_instagram.select()
        
        self.check_facebook = ctk.CTkCheckBox(self.frame_platforms, text="Facebook")
        self.check_facebook.pack(side="left", padx=10, pady=10)
        self.check_facebook.select()
        
        self.check_tiktok = ctk.CTkCheckBox(self.frame_platforms, text="TikTok")
        self.check_tiktok.pack(side="left", padx=10, pady=10)
        self.check_tiktok.select()

        # Upload Button
        self.btn_upload = ctk.CTkButton(self, text="Upload to All Selected", command=self.start_upload_thread, height=40, font=("Arial", 14, "bold"))
        self.btn_upload.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

        # Status
        self.label_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.label_status.grid(row=6, column=0, padx=20, pady=10)

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.mov *.avi")])
        if file_path:
            self.video_path = file_path
            self.label_video_path.configure(text=os.path.basename(file_path))

    def start_upload_thread(self):
        if not self.video_path:
            self.label_status.configure(text="Please select a video first!", text_color="red")
            return
        
        self.btn_upload.configure(state="disabled")
        self.label_status.configure(text="Uploading...", text_color="blue")
        
        thread = threading.Thread(target=self.upload_process)
        thread.start()

    def upload_process(self):
        caption = self.textbox_caption.get("1.0", "end-1c")
        
        # Load Config
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            self.update_status("Error: config.json not found!", "red")
            self.btn_upload.configure(state="normal")
            return

        self.update_status("Starting simultaneous uploads...", "blue")
        
        threads = []
        results = {}
        results_lock = threading.Lock()

        def run_uploader(name, func, *args):
            try:
                # Small delay to prevent browser launch conflicts
                time.sleep(1) 
                res = func(*args)
                with results_lock:
                    results[name] = res
            except Exception as e:
                with results_lock:
                    results[name] = f"Error: {str(e)}"

        if self.check_youtube.get():
            t = threading.Thread(target=run_uploader, args=("YouTube", upload_youtube, self.video_path, caption, config.get('youtube', {})))
            threads.append(t)
            t.start()
            time.sleep(2) # Stagger slightly to avoid driver conflicts

        if self.check_instagram.get():
            t = threading.Thread(target=run_uploader, args=("Instagram", upload_instagram, self.video_path, caption, config.get('instagram', {})))
            threads.append(t)
            t.start()

        if self.check_facebook.get():
            t = threading.Thread(target=run_uploader, args=("Facebook", upload_facebook, self.video_path, caption, config.get('facebook', {})))
            threads.append(t)
            t.start()
            time.sleep(2) # Stagger slightly

        if self.check_tiktok.get():
            t = threading.Thread(target=run_uploader, args=("TikTok", upload_tiktok, self.video_path, caption, config.get('tiktok', {})))
            threads.append(t)
            t.start()

        # Wait for all threads
        for t in threads:
            t.join()

        # Format results
        final_status_list = []
        for name in ["YouTube", "Instagram", "Facebook", "TikTok"]:
            if name in results:
                final_status_list.append(f"{name}: {results[name]}")
        
        final_status = " | ".join(final_status_list)
        self.update_status(final_status, "green")
        self.btn_upload.configure(state="normal")

    def update_status(self, text, color):
        self.label_status.configure(text=text, text_color=color)

if __name__ == "__main__":
    app = CrossPostApp()
    app.mainloop()
