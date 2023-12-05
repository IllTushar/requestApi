import tkinter as tk
import requests
from PIL import Image, ImageTk
import io

class UserViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Viewer App")
        self.avatar_images = []  # Store PhotoImage objects here

        # Create a Listbox to display user data
        self.listbox = tk.Listbox(root, width=50)
        self.listbox.pack(padx=10, pady=10)

        # Add a button to fetch and display user data
        self.fetch_button = tk.Button(root, text="Fetch Users", command=self.fetch_users)
        self.fetch_button.pack(pady=10)

    def fetch_users(self):
        # Make API request to get user data
        url = "https://reqres.in/api/users?page=2"
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Clear existing data in the Listbox and reset PhotoImage objects
            self.listbox.delete(0, tk.END)
            self.avatar_images = []

            # Parse and display user data in the Listbox
            data = response.json().get("data", [])
            for user in data:
                user_info = f"{user['first_name']} {user['last_name']} - {user['email']}"
                self.listbox.insert(tk.END, user_info)

                # Load and display avatar
                avatar_url = user['avatar']
                avatar_index = self.load_avatar(avatar_url)
                if avatar_index is not None:
                    # Display the avatar image using a Label
                    avatar_label = tk.Label(self.root, image=self.avatar_images[avatar_index])
                    avatar_label.pack()

        else:
            # Display an error message if the request was not successful
            self.listbox.delete(0, tk.END)
            self.listbox.insert(tk.END, f"Error: {response.status_code}")

    def load_avatar(self, avatar_url):
        try:
            # Download the avatar image
            response = requests.get(avatar_url)
            image_data = response.content

            # Open the image using Pillow
            img = Image.open(io.BytesIO(image_data))

            # Resize the image if needed using LANCZOS filter
            img = img.resize((50, 50), Image.LANCZOS)

            # Convert to PhotoImage for Tkinter
            photo_image = ImageTk.PhotoImage(img)

            # Store the PhotoImage object to prevent garbage collection
            self.avatar_images.append(photo_image)

            return len(self.avatar_images) - 1  # Return the index of the image in the list

        except Exception as e:
            print(f"Error loading avatar: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = UserViewerApp(root)
    root.mainloop()
