# image-captioning
next js with trainde model on flicker 8k (note connection are not join , underwork)

Do this first !!!!!!!!!!!!!!!!!

/project-root
│── /server  (Python backend)
│   ├── server.py
│   ├── model.keras
│   ├── tokenizer.pkl
│   ├── max_len.pkl
│   ├── reference_caption.pkl

│── /nextjs-app  (Next.js frontend)
│   ├── pages/
│   ├── components/
│   ├── public/
│   ├── package.json
│   ├── next.config.js





Steps to Run Next.js with a Trained Model on Flickr8K
1️⃣ Keep the backend (Python server) and frontend (Next.js) in separate folders.

Place server.py, model.keras, tokenizer.pkl, max_len.pkl, and caption.pkl in a separate folder away from Next.js.

2️⃣ Start the Python server:

Open CMD (Command Prompt) or Terminal.

Go to the folder where server.py is located.

Run:
python server.py
This will start the backend, allowing it to accept images and return captions.

3️⃣ Start the Next.js project:

Open a new terminal.

Navigate to the Next.js project folder.

Run:
npm run dev
This will start the frontend.

Now, your Python server is running in the background, and your Next.js project is ready to connect to it. 🚀




Website: 


![Project Screenshot](screenshots/Screenshot%202025-03-23%20185302.png)
![Project Screenshot](screenshots/Screenshot%202025-03-23%20185328.png)


Server.py:

![Project Screenshot](screenshots/Screenshot%202025-03-23%20185423.png)








