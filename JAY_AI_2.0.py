import customtkinter as ctk
from tkinter import scrolledtext, messagebox, END
import os
import json
from threading import Thread

# Import the Google GenAI SDK components
from google import genai
from google.genai import errors
from google.genai.types import Content, Part, GenerateContentConfig

# >>> MANDATORY SETUP <<<
# You MUST replace this placeholder with your actual Gemini API Key for the app to work.
CUSTOM_AI_API_KEY = "AIzaSyAwim1u2AA0eYt9oqw1aUNcQM5m1yAbbp0"

# --- CONFIGURATION ---
SETTINGS_FILE = "jay_ai_settings.json"
DEFAULT_THEME = "dark-blue"
DEFAULT_MODE = '1'

# --- 1. BASE SYSTEM INSTRUCTION (Applies to all modes) ---

BASE_SYSTEM_INSTRUCTION = (
    "You are an advanced large language model and helpful assistant named 'Jay AI'. "
    "You are equipped with a real-time Google Search tool for current affairs and general knowledge, which you must use when needed. "
    "**PRIORITY IDENTITY AND ACADEMIC DETAILS (Must be cited when appropriate):** "
    "**Founder:** Aswinjay (CEO of Jay Tech Solutions, studies CSBS at RIT). "
    "**Company:** Jay Tech Solutions (started by Aswinjay in class 11, specializes in AI R&D). "
    "**Best Friend:** Sujid (introvert, Taekwondo player, son of a soldier, supportive). "
    "When asked about your identity, always state your name is 'Jay AI' and you are powered by 'Jay Tech Solutions' and founded by Aswinjay. "
    "Maintain a professional, helpful, and friendly tone."
    "Your current role is a dedicated **Academic Helper** for RIT CSBS students. Focus on providing detailed, accurate information about computer science, RIT's academic environment, and specific faculty. "
    "Always cite relevant faculty or academic context when appropriate. "
    "**RIT CSBS HOD:** Dr. M. Gomathy Nayagam (male, Associate Professor, 19+ yrs exp, specializes in Image/Video Processing, Cloud, AI/ML). "
    "**RIT CSBS CA (First Year):** Mrs. M. Shabana Fathima (Assistant Professor, teaches C programming, kind, research in ML, Cloud, Mobile Computing). "
    "**RIT Maths Professor:** Dr. R. Saravanakumar (Assistant Professor in Mathematics, holds a Ph.D. from Anna University, specializes in Ordinary Differential Equations). "
    "**RIT EOC Professor:** Mr. Ramakrishnan (Teaches Essentials of Computing (EOC) exceptionally well, known for making complex topics easy to grasp and always encouraging student innovation)."
)


# --- 2. MODE-SPECIFIC INSTRUCTIONS (Focus on the immediate role) ---

GENERAL_AI_INSTRUCTION = (
    "Your current role is a **General Knowledge Assistant**. Focus on answering general queries, current affairs, and engaging in casual conversation."
)

ACADEMIC_HELPER_INSTRUCTION = (
    "Your current role is a dedicated **Academic Helper** for RIT CSBS students. Focus on providing detailed, accurate information about computer science, RIT's academic environment, and specific faculty. "
    "Always cite relevant faculty or academic context when appropriate. "
    "**RIT CSBS HOD:** Dr. M. Gomathy Nayagam (male, Associate Professor, 19+ yrs exp, specializes in Image/Video Processing, Cloud, AI/ML). "
    "**RIT CSBS CA (First Year):** Mrs. M. Shabana Fathima (Assistant Professor, teaches C programming, kind, research in ML, Cloud, Mobile Computing). "
    "**RIT Maths Professor:** Dr. R. Saravanakumar (Assistant Professor in Mathematics, holds a Ph.D. from Anna University, specializes in Ordinary Differential Equations). "
    "**RIT EOC Professor:** Mr. Ramakrishnan (Teaches Essentials of Computing (EOC) exceptionally well, known for making complex topics easy to grasp and always encouraging student innovation)."
)

MATHS_SOLVER_INSTRUCTION = (
    "Your current role is an expert, highly rigorous, and step-by-step **Mathematical Solver**. "
    "Your mode is strictly dedicated to solving advanced mathematics problems, including: **Differential Calculus (Derivatives, Maxima, Minima), Integral Calculus, Linear Algebra, and Differential Equations.** "
    "For every problem, you MUST provide a detailed, logical breakdown of the solution steps. Use LaTeX formatting ($$ or $) for all expressions. You must not use the search tool for core derivation."
)

CODE_GENERATOR_INSTRUCTION = (
    "Your current role is a highly specialized and precise **Code Generator**. Your task is to generate complete, correct, and highly efficient code in the programming language requested by the user. "
    "Supported languages are: **C, C++, Java, JavaScript, Python, R, and Scala.** The user MUST specify the language. "
    "Every code block must be clean, follow language best practices, and include clear, explanatory comments."
)

CREATIVE_WRITER_INSTRUCTION = (
    "Your current role is a **Creative and Stylistic Writer**. Your responses must be imaginative, engaging, and flow beautifully. Focus on tasks like writing stories, poems, scripts, marketing copy, or detailed descriptions. "
    "Vary your sentence structure and vocabulary to enhance the creative output."
)

# --- 3. MODE SETTINGS DICTIONARY (Unchanged) ---
MODE_SETTINGS = {
    '1': {'name': "General Jay AI", 'instruction': GENERAL_AI_INSTRUCTION},
    '2': {'name': "Academic Helper", 'instruction': ACADEMIC_HELPER_INSTRUCTION},
    '3': {'name': "Maths Solver", 'instruction': MATHS_SOLVER_INSTRUCTION},
    '4': {'name': "Code Generator", 'instruction': CODE_GENERATOR_INSTRUCTION},
    '5': {'name': "Creative Writer", 'instruction': CREATIVE_WRITER_INSTRUCTION},
}

class JayAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- 1. Load Settings and Apply CTK Theme ---
        self.settings = self._load_settings()
        ctk.set_appearance_mode(self.settings.get("appearance_mode", "Dark"))
        ctk.set_default_color_theme(self.settings.get("color_theme", DEFAULT_THEME))

        # --- 2. Initialize Gemini Client ---
        self.client = self._initialize_client()
        if not self.client:
            self.destroy()
            return

        # --- 3. Internal State ---
        self.current_mode_key = DEFAULT_MODE
        # Stores the chat history (user and model contents)
        self.messages: list[Content] = [] 
        self.mode_buttons = {}
        
        # --- 4. Setup GUI ---
        self.title("Jay AI - Multi-Mode Chatbot (Streaming)")
        self.geometry("900x600")
        
        # Configure columns: Column 0 (sidebar) fixed width, Column 1 (chat) expands
        self.grid_columnconfigure(1, weight=1)
        
        # Configure rows: Row 1 (chat area) expands vertically
        self.grid_rowconfigure(1, weight=1)

        self._create_sidebar()
        self._create_main_chat_area()
        self._create_input_area()
        
        self.switch_mode(self.current_mode_key) # Initialize chat history and welcome message
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    # --- SETUP & INITIALIZATION METHODS ---
    def _initialize_client(self):
        """Initializes the Gemini client."""
        if CUSTOM_AI_API_KEY == "YOUR_ACTUAL_GEMINI_API_KEY_HERE" or not CUSTOM_AI_API_KEY:
            messagebox.showerror("API Key Error", "FATAL: Please replace the placeholder API key in the script with your actual key.")
            return None
        try:
            return genai.Client(api_key=CUSTOM_AI_API_KEY)
        except Exception as e:
            print(f"Client initialization failed: {e}")
            messagebox.showerror("Initialization Error", f"Client failed to initialize: {e}")
            return None
            
    def _load_settings(self):
        """Loads user preferences (appearance mode, theme) from JSON."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
        
    def _save_settings(self):
        """Saves current user preferences to JSON, correctly retrieving theme from the widget."""
        self.settings["appearance_mode"] = ctk.get_appearance_mode()
        # FIX: Get color theme value from the option menu widget
        self.settings["color_theme"] = self.theme_optionemenu.get()
        
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def _on_closing(self):
        """Called when the window is closed."""
        self._save_settings()
        self.destroy()

    # --- WIDGET CREATION METHODS ---
    def _create_sidebar(self):
        """Creates the left sidebar for mode selection and settings."""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=10, pady=10)
        self.sidebar_frame.grid_rowconfigure(len(MODE_SETTINGS) + 2, weight=1)

        # Title
        logo_label = ctk.CTkLabel(self.sidebar_frame, text="🐯 Jay AI Modes", font=ctk.CTkFont(size=18, weight="bold"))
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Mode Buttons
        for i, (key, settings) in enumerate(MODE_SETTINGS.items()):
            btn = ctk.CTkButton(self.sidebar_frame, text=settings['name'],
                                 command=lambda k=key: self.switch_mode(k),
                                 corner_radius=8, height=35)
            btn.grid(row=i + 1, column=0, padx=20, pady=10, sticky="ew")
            self.mode_buttons[key] = btn

        # Appearance Mode Control
        appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_label.grid(row=len(MODE_SETTINGS) + 2, column=0, padx=20, pady=(10, 0), sticky="s")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                            values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode_event,
                                                            corner_radius=8)
        self.appearance_mode_optionemenu.grid(row=len(MODE_SETTINGS) + 3, column=0, padx=20, pady=(0, 10), sticky="s")
        self.appearance_mode_optionemenu.set(self.settings.get("appearance_mode", "Dark"))
        
        # Theme Color Control
        theme_label = ctk.CTkLabel(self.sidebar_frame, text="Color Theme:", anchor="w")
        theme_label.grid(row=len(MODE_SETTINGS) + 4, column=0, padx=20, pady=(10, 0), sticky="s")
        self.theme_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                   values=["blue", "dark-blue", "green"],
                                                   command=self.change_theme_event,
                                                   corner_radius=8)
        self.theme_optionemenu.grid(row=len(MODE_SETTINGS) + 5, column=0, padx=20, pady=(0, 20), sticky="s")
        self.theme_optionemenu.set(self.settings.get("color_theme", DEFAULT_THEME))

    def _create_main_chat_area(self):
        """Creates the main area for chat history and mode status."""
        
        # Mode Status Frame (Row 0, Column 1)
        self.mode_status_frame = ctk.CTkFrame(self, corner_radius=10)
        self.mode_status_frame.grid(row=0, column=1, padx=(0, 10), pady=(10, 0), sticky="new")
        self.mode_status_frame.grid_columnconfigure(0, weight=1)

        self.mode_label = ctk.CTkLabel(self.mode_status_frame, text="", 
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.mode_label.grid(row=0, column=0, padx=15, pady=8, sticky="w")
        
        # Chat History Display (ScrolledText for complex text rendering) (Row 1, Column 1)
        self.chat_history = scrolledtext.ScrolledText(self, wrap='word', state='disabled', 
                                                     font=('Consolas', 10), padx=10, pady=10)
        # sticky="nsew" ensures it fills the available space which expands due to row/column weights
        self.chat_history.grid(row=1, column=1, padx=(0, 10), pady=(10, 0), sticky="nsew") 

        # Configure tags for styling messages
        self.chat_history.tag_config('user', foreground='#1E88E5', font=('Arial', 10, 'bold')) 
        self.chat_history.tag_config('ai', foreground='#00A300', font=('Arial', 10))
        self.chat_history.tag_config('system', foreground='gray', font=('Arial', 10, 'italic'))

    def _create_input_area(self):
        """Creates the input field and send button."""
        # Input Frame (Row 2, Column 1)
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="sew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter your prompt here...",
                                         font=('Arial', 12), corner_radius=8, height=40)
        # Bind the Enter key to the send function
        self.input_entry.bind("<Return>", lambda event: self.send_message_thread())
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=10)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message_thread,
                                         font=('Arial', 12, 'bold'), corner_radius=8, width=100, height=40)
        self.send_button.grid(row=0, column=1, sticky="e", padx=(0, 15), pady=10)
        self.input_entry.focus_set()

    # --- SETTINGS CONTROL METHODS ---
    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Changes the GUI between Light, Dark, and System modes."""
        ctk.set_appearance_mode(new_appearance_mode)

    def change_theme_event(self, new_theme: str):
        """Changes the CTk default color theme."""
        ctk.set_default_color_theme(new_theme)

    # --- CHAT & MODE LOGIC ---
    def switch_mode(self, new_mode_key):
        """Switches the mode, resets history, and updates GUI."""
        self.current_mode_key = new_mode_key
        self.messages = [] # Reset history to ensure new system prompt takes effect
        self.chat_history.config(state='normal')
        self.chat_history.delete(1.0, END)
        self.chat_history.config(state='disabled')

        settings = MODE_SETTINGS[new_mode_key]
        self.mode_label.configure(text=f"Current Mode: {settings['name']} | Status: Search Enabled 🌐")
        
        # Update button colors to highlight the active mode
        for key, btn in self.mode_buttons.items():
            if key == new_mode_key:
                btn.configure(fg_color=("gray75", "gray25")) # Active color
            else:
                # Reset to default color
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]) 

        # Post welcome message
        welcome_text = {
            '1': "Hello! I'm Jay AI. I can assist with general knowledge and my academic background (Founder: Aswinjay).",
            '2': "Welcome to the Academic Helper Mode! How can I assist you with RIT, CSBS, or technical concepts today?",
            '3': "Welcome to the Maths Solver Mode! Please give me a calculus, algebra, or differential equation problem to solve using LaTeX.",
            '4': "Welcome to the Code Generator Mode. Please specify the language (C, Python, Java, etc.) with your request.",
            '5': "Welcome to the Creative Writer Mode! What story, poem, or stylistic text should I create for you?",
        }[new_mode_key]
        self.append_message("Jay AI: " + welcome_text, 'ai')
        
    def append_message(self, text, tag, newline=True):
        """Appends text to the chat history widget with styling."""
        self.chat_history.config(state='normal')
        
        if newline:
            # Check if we are completing a streaming response and need to add the final newline
            if self.chat_history.get("end-1c", END) != "\n\n":
                 self.chat_history.insert(END, text + "\n\n", tag)
            else:
                self.chat_history.insert(END, text + "\n\n", tag)
        else:
            self.chat_history.insert(END, text, tag)
            
        self.chat_history.see(END) # Scroll to the bottom
        self.chat_history.config(state='disabled')

    def send_message_thread(self, event=None):
        """Starts the message sending process in a separate thread."""
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        self.append_message("You: " + user_input, 'user')
        self.input_entry.delete(0, END)
        
        # Append initial AI header to the chat history (no newline yet)
        self.append_message("Jay AI: ", 'ai', newline=False)

        # Disable input while waiting for response
        self.input_entry.configure(state='disabled')
        self.send_button.configure(state='disabled', text="Streaming...")
        self.configure(cursor='watch')

        # Start the API call in a new thread
        Thread(target=self._process_agent_turn, args=(user_input,)).start()
        
    def _process_agent_turn(self, user_input):
        """Handles the API call and GUI update in the background thread using streaming."""
        
        self.messages.append(Content(role="user", parts=[Part(text=user_input)]))
        current_instruction = MODE_SETTINGS[self.current_mode_key]['instruction']
        
        full_response_text = ""
        
        try:
            stream = self._run_agent_turn_core_streaming(current_instruction)

            for chunk in stream:
                if chunk.text:
                    full_response_text += chunk.text
                    # Schedule GUI update back on the main thread for each chunk
                    # Note: Using after(0) is essential for thread safety in Tkinter
                    self.after(0, lambda t=chunk.text: self.append_message(t, 'ai', newline=False))
            
            # Final step: Add the completed response to memory and ensure final newline
            if full_response_text:
                # Add the final newline formatting if needed
                self.after(0, lambda: self.append_message("", 'ai', newline=True)) 
                self.messages.append(Content(role="model", parts=[Part(text=full_response_text)]))
            else:
                # Handle cases where the stream is empty (e.g., content blocked)
                raise errors.APIError("Received an empty response stream or content was blocked.")
                
        except errors.APIError as e:
            # Pop the user message added earlier, as we didn't get a model response
            self.messages.pop() 
            error_message = f"[SYSTEM ERROR] API failed during stream: {e}"
            self.after(0, lambda: self.append_message(error_message, 'system'))
        except Exception as e:
            self.messages.pop()
            error_message = f"[CRITICAL ERROR] An unexpected error occurred: {e}"
            self.after(0, lambda: self.append_message(error_message, 'system'))

        # Re-enable input (scheduled back on the main thread)
        self.after(0, self._reenable_input)


    def _run_agent_turn_core_streaming(self, mode_instruction: str):
        """
        The core API streaming logic. Uses generate_content_stream.
        """
        
        # Combine the fixed base persona with the mode-specific instructions
        final_system_prompt = BASE_SYSTEM_INSTRUCTION + "\n\n--- CURRENT MODE ROLE ---\n\n" + mode_instruction
        
        # Always enable Google Search grounding for general context, though some modes may ignore it.
        tools_config = [{"google_search": {}}] 
        
        config_obj = GenerateContentConfig(
            system_instruction=final_system_prompt,
            tools=tools_config
        )

        try:
            # Use generate_content_stream for real-time output
            stream = self.client.models.generate_content_stream(
                model="gemini-2.5-flash", 
                contents=self.messages, # Pass the entire history
                config=config_obj 
            )
            return stream

        except Exception as e:
            # Propagate the exception back to _process_agent_turn for handling
            raise errors.APIError(f"Streaming failed to start: {e}")
            

    def _reenable_input(self):
        """Re-enables the GUI input elements."""
        self.input_entry.configure(state='normal')
        self.send_button.configure(state='normal', text="Send")
        self.configure(cursor='')
        self.input_entry.focus_set()


if __name__ == "__main__":
    app = JayAIGUI()
    app.mainloop()
