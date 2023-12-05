import tkinter as tk
import requests
from PIL import Image, ImageTk, ImageDraw
import io

class UserViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Viewer App")
        self.avatar_images = []  # Store PhotoImage objects here

        # Create a Frame to hold user widgets
        self.user_frame = tk.Frame(root)
        self.user_frame.pack(padx=10, pady=10)

        # Add a button to fetch and display user data
        self.fetch_button = tk.Button(root, text="Fetch Users", command=self.fetch_users)
        self.fetch_button.pack(pady=10)

    def fetch_users(self):
        # Make API request to get user data
        url = "https://reqres.in/api/users?page=2"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Clear existing data in the user frame and reset PhotoImage objects
            for widget in self.user_frame.winfo_children():
                widget.destroy()

            self.avatar_images = []

            # Parse and display user data in the user frame
            data = response.json().get("data", [])
            for user in data:
                user_info = f"{user['first_name']} {user['last_name']} - {user['email']}"

                # Load and display avatar
                avatar_url = user['avatar']
                avatar_index = self.load_avatar(avatar_url)
                if avatar_index is not None:
                    # Create a custom widget for each user
                    user_widget = UserWidget(self.user_frame, user_info, self.avatar_images[avatar_index])
                    user_widget.pack()

        else:
            # Display an error message if the request was not successful
            error_label = tk.Label(self.user_frame, text=f"Error: {response.status_code}")
            error_label.pack()

    def load_avatar(self, avatar_url):
        try:
            # Download the avatar image
            response = requests.get(avatar_url)
            image_data = response.content

            # Open the image using Pillow
            img = Image.open(io.BytesIO(image_data))

            # Resize the image if needed using LANCZOS filter
            img = img.resize((50, 50), Image.LANCZOS)

            # Create a circular mask
            mask = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

            # Apply the circular mask to the image
            img.putalpha(mask)

            # Convert to PhotoImage for Tkinter
            photo_image = ImageTk.PhotoImage(img)

            # Store the PhotoImage object to prevent garbage collection
            self.avatar_images.append(photo_image)

            return len(self.avatar_images) - 1  # Return the index of the image in the list

        except Exception as e:
            print(f"Error loading avatar: {e}")
            return None

class UserWidget(tk.Frame):
    def __init__(self, parent, user_info, avatar_image):
        super().__init__(parent)

        # Create a Label for user information
        info_label = tk.Label(self, text=user_info)
        info_label.pack(side=tk.LEFT, padx=5)

        # Create a Label for the circular avatar image
        avatar_label = tk.Label(self, image=avatar_image)
        avatar_label.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserViewerApp(root)
    root.mainloop()
