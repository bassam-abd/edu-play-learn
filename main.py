"""
Edu Play Learn - Desktop Application (Tkinter)
Main entry point for the desktop version
Complete Arabic support with RTL layout
"""
import tkinter as tk
from tkinter import ttk, messagebox
from managers import TranslationManager, DatabaseManager, ScoreManager, SoundManager
from modules import PhonicsModule, MathModule, PuzzleModule, ColorsShapesModule
from datetime import datetime

class EduPlayLearnApp:
    """Main desktop application for Edu Play Learn"""

    def __init__(self, root):
        self.root = root
        self.root.title("Edu Play Learn - تعليم يلعب تعلم")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialize managers
        self.translation_manager = TranslationManager("en")
        self.database_manager = DatabaseManager()
        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()

        # Configure style
        self._configure_style()
        
        # Create main menu
        self.create_main_menu()

    def _configure_style(self):
        """Configure application styling"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 28, 'bold'), foreground='#2E86AB')
        style.configure('Heading.TLabel', font=('Arial', 16, 'bold'), foreground='#A23B72')
        style.configure('Normal.TLabel', font=('Arial', 12), foreground='#333333')
        style.configure('TButton', font=('Arial', 12, 'bold'), padding=10)

    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, 
                               text=self.translation_manager.get("title"),
                               style='Title.TLabel')
        title_label.pack(pady=20)

        # Language and Settings Frame
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(pady=10)

        ttk.Button(settings_frame, 
                  text="🌍 العربية | English",
                  command=self.toggle_language).pack(side=tk.LEFT, padx=5)

        ttk.Button(settings_frame, 
                  text="👨‍👩‍👧 " + self.translation_manager.get("parent_dashboard"),
                  command=self.open_parent_dashboard).pack(side=tk.LEFT, padx=5)

        # Module buttons
        modules_frame = ttk.Frame(main_frame)
        modules_frame.pack(pady=30, fill=tk.BOTH, expand=True)

        # Create module buttons
        modules = [
            ("🔤 " + self.translation_manager.get("phonics"), self.open_phonics, "#FF6B6B"),
            ("🔢 " + self.translation_manager.get("math"), self.open_math, "#4ECDC4"),
            ("🧩 " + self.translation_manager.get("puzzle"), self.open_puzzle, "#45B7D1"),
            ("🎨 " + self.translation_manager.get("colors_shapes"), self.open_colors, "#FFA07A"),
        ]

        for label, command, color in modules:
            btn = tk.Button(modules_frame, 
                           text=label,
                           command=command,
                           font=('Arial', 14, 'bold'),
                           bg=color,
                           fg='white',
                           height=3,
                           relief=tk.RAISED,
                           bd=2)
            btn.pack(pady=10, fill=tk.X)

        # Score display
        score_frame = ttk.Frame(main_frame)
        score_frame.pack(pady=20)

        ttk.Label(score_frame,
                 text=f"Score: {self.score_manager.get_score()} | "
                      f"Accuracy: {self.score_manager.get_accuracy()}% | "
                      f"Streak: {self.score_manager.get_streak()}",
                 style='Normal.TLabel').pack()

    def toggle_language(self):
        """Toggle between Arabic and English"""
        current_lang = self.translation_manager.lang
        new_lang = "ar" if current_lang == "en" else "en"
        self.translation_manager.set_language(new_lang)
        self.database_manager.update("user", {"language": new_lang})
        self.create_main_menu()

    def open_phonics(self):
        """Open Phonics Module"""
        module_window = tk.Toplevel(self.root)
        module_window.title(self.translation_manager.get("phonics"))
        module_window.geometry("600x500")
        PhonicsModuleUI(module_window, self.translation_manager, self.score_manager, self.sound_manager)

    def open_math(self):
        """Open Math Module"""
        module_window = tk.Toplevel(self.root)
        module_window.title(self.translation_manager.get("math"))
        module_window.geometry("600x500")
        MathModuleUI(module_window, self.translation_manager, self.score_manager, self.sound_manager)

    def open_puzzle(self):
        """Open Puzzle Module"""
        module_window = tk.Toplevel(self.root)
        module_window.title(self.translation_manager.get("puzzle"))
        module_window.geometry("600x500")
        PuzzleModuleUI(module_window, self.translation_manager, self.score_manager, self.sound_manager)

    def open_colors(self):
        """Open Colors & Shapes Module"""
        module_window = tk.Toplevel(self.root)
        module_window.title(self.translation_manager.get("colors_shapes"))
        module_window.geometry("600x500")
        ColorsShapesModuleUI(module_window, self.translation_manager, self.score_manager, self.sound_manager)

    def open_parent_dashboard(self):
        """Open Parent Dashboard"""
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title(self.translation_manager.get("parent_dashboard"))
        dashboard_window.geometry("700x600")
        ParentDashboard(dashboard_window, self.score_manager, self.translation_manager)


class PhonicsModuleUI:
    """UI for Phonics Module"""

    def __init__(self, window, translation_manager, score_manager, sound_manager):
        self.window = window
        self.translation_manager = translation_manager
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        
        self.module = PhonicsModule(language="ar" if translation_manager.lang == "ar" else "en")
        self.create_ui()

    def create_ui(self):
        """Create the Phonics UI"""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Instructions
        ttk.Label(frame, text="Select the correct letter:", 
                 font=('Arial', 14)).pack(pady=10)

        # Current letter display
        letter_label = tk.Label(frame, text=self.module.current_letter, 
                               font=('Arial', 60, 'bold'), fg='#2E86AB')
        letter_label.pack(pady=20)

        # Letter name
        ttk.Label(frame, text=f"Name: {self.module.get_letter_name()}", 
                 font=('Arial', 12)).pack(pady=10)

        # Options
        options_frame = ttk.Frame(frame)
        options_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        for option in self.module.options:
            btn = tk.Button(options_frame, text=option, font=('Arial', 16, 'bold'),
                           command=lambda opt=option: self.check_answer(opt),
                           bg='#4ECDC4', fg='white', height=2, width=10)
            btn.pack(pady=5)

        # Score label
        self.score_label = ttk.Label(frame, 
                                    text=f"Score: {self.score_manager.get_score()}",
                                    font=('Arial', 12, 'bold'), foreground='green')
        self.score_label.pack(pady=10)

    def check_answer(self, answer):
        """Check the selected answer"""
        is_correct = self.module.check_answer(answer)
        
        if is_correct:
            self.sound_manager.play_correct()
            self.score_manager.add_correct_answer()
            messagebox.showinfo("Result", self.translation_manager.get("correct"))
        else:
            self.sound_manager.play_wrong()
            self.score_manager.add_wrong_answer()
            messagebox.showerror("Result", self.translation_manager.get("wrong"))

        self.module.generate_question()
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_ui()


class MathModuleUI:
    """UI for Math Module"""

    def __init__(self, window, translation_manager, score_manager, sound_manager):
        self.window = window
        self.translation_manager = translation_manager
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        
        self.module = MathModule(difficulty="easy")
        self.create_ui()

    def create_ui(self):
        """Create the Math UI"""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Question
        question_label = tk.Label(frame, text=self.module.get_question_string(),
                                 font=('Arial', 40, 'bold'), fg='#2E86AB')
        question_label.pack(pady=30)

        # Input
        ttk.Label(frame, text="Your answer:", font=('Arial', 12)).pack()
        self.entry = ttk.Entry(frame, font=('Arial', 14), width=10)
        self.entry.pack(pady=10)
        self.entry.focus()

        # Button
        ttk.Button(frame, text=self.translation_manager.get("check"),
                  command=self.check_answer).pack(pady=10)

        # Score
        self.score_label = ttk.Label(frame,
                                    text=f"Score: {self.score_manager.get_score()}",
                                    font=('Arial', 12, 'bold'), foreground='green')
        self.score_label.pack(pady=10)

        self.entry.bind('<Return>', lambda e: self.check_answer())

    def check_answer(self):
        """Check the math answer"""
        is_correct = self.module.check_answer(self.entry.get())

        if is_correct:
            self.sound_manager.play_correct()
            self.score_manager.add_correct_answer()
            messagebox.showinfo("Result", self.translation_manager.get("correct"))
        else:
            self.sound_manager.play_wrong()
            self.score_manager.add_wrong_answer()
            messagebox.showerror("Result", self.translation_manager.get("wrong"))

        self.module.generate_question()
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_ui()


class PuzzleModuleUI:
    """UI for Puzzle Module"""

    def __init__(self, window, translation_manager, score_manager, sound_manager):
        self.window = window
        self.translation_manager = translation_manager
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        
        self.module = PuzzleModule()
        self.create_ui()

    def create_ui(self):
        """Create the Puzzle UI"""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Question
        question_label = tk.Label(frame, text=self.module.get_puzzle_string(),
                                 font=('Arial', 36, 'bold'), fg='#2E86AB')
        question_label.pack(pady=30)

        # Input
        ttk.Label(frame, text="What comes next?", font=('Arial', 12)).pack()
        self.entry = ttk.Entry(frame, font=('Arial', 14), width=10)
        self.entry.pack(pady=10)
        self.entry.focus()

        # Button
        ttk.Button(frame, text=self.translation_manager.get("check"),
                  command=self.check_answer).pack(pady=10)

        # Score
        self.score_label = ttk.Label(frame,
                                    text=f"Score: {self.score_manager.get_score()}",
                                    font=('Arial', 12, 'bold'), foreground='green')
        self.score_label.pack(pady=10)

        self.entry.bind('<Return>', lambda e: self.check_answer())

    def check_answer(self):
        """Check the puzzle answer"""
        is_correct = self.module.check_answer(self.entry.get())

        if is_correct:
            self.sound_manager.play_correct()
            self.score_manager.add_correct_answer()
            messagebox.showinfo("Result", self.translation_manager.get("correct"))
        else:
            self.sound_manager.play_wrong()
            self.score_manager.add_wrong_answer()
            messagebox.showerror("Result", self.translation_manager.get("wrong"))

        self.module.generate_question()
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_ui()


class ColorsShapesModuleUI:
    """UI for Colors & Shapes Module"""

    def __init__(self, window, translation_manager, score_manager, sound_manager):
        self.window = window
        self.translation_manager = translation_manager
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        
        self.module = ColorsShapesModule()
        self.create_ui()

    def create_ui(self):
        """Create the Colors & Shapes UI"""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Question
        question_text = self.module.get_question_string()
        question_label = ttk.Label(frame, text=question_text,
                                  font=('Arial', 16, 'bold'))
        question_label.pack(pady=20)

        # Options
        options_frame = ttk.Frame(frame)
        options_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        for option in self.module.options:
            if self.module.question_type == "color":
                color = self.module.get_color_hex(option)
                btn = tk.Button(options_frame, text=option, font=('Arial', 12, 'bold'),
                               command=lambda opt=option: self.check_answer(opt),
                               bg=color, fg='white', height=2, width=15)
            else:
                btn = tk.Button(options_frame, text=option, font=('Arial', 12, 'bold'),
                               command=lambda opt=option: self.check_answer(opt),
                               bg='#FFA07A', fg='white', height=2, width=15)
            btn.pack(pady=5)

        # Score
        self.score_label = ttk.Label(frame,
                                    text=f"Score: {self.score_manager.get_score()}",
                                    font=('Arial', 12, 'bold'), foreground='green')
        self.score_label.pack(pady=10)

    def check_answer(self, answer):
        """Check the selected answer"""
        is_correct = self.module.check_answer(answer)

        if is_correct:
            self.sound_manager.play_correct()
            self.score_manager.add_correct_answer()
            messagebox.showinfo("Result", self.translation_manager.get("correct"))
        else:
            self.sound_manager.play_wrong()
            self.score_manager.add_wrong_answer()
            messagebox.showerror("Result", self.translation_manager.get("wrong"))

        self.module.generate_question()
        for widget in self.window.winfo_children():
            widget.destroy()
        self.create_ui()


class ParentDashboard:
    """Parent Dashboard for monitoring child's progress"""

    def __init__(self, window, score_manager, translation_manager):
        self.window = window
        self.score_manager = score_manager
        self.translation_manager = translation_manager
        self.create_dashboard()

    def create_dashboard(self):
        """Create the parent dashboard"""
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(frame, text=self.translation_manager.get("parent_dashboard"),
                 font=('Arial', 20, 'bold'), foreground='#2E86AB').pack(pady=20)

        # Statistics
        stats = self.score_manager.get_stats()

        stats_frame = ttk.LabelFrame(frame, text="Statistics", padding="10")
        stats_frame.pack(pady=20, fill=tk.X)

        for key, value in stats.items():
            ttk.Label(stats_frame, text=f"{key.replace('_', ' ').title()}: {value}",
                     font=('Arial', 12)).pack(anchor=tk.W, pady=5)

        # Reset button
        ttk.Button(frame, text="Reset Scores", 
                  command=self.reset_scores).pack(pady=20)

    def reset_scores(self):
        """Reset all scores"""
        if messagebox.askyesno("Reset", "Are you sure you want to reset all scores?"):
            self.score_manager.reset()
            self.create_dashboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = EduPlayLearnApp(root)
    root.mainloop()
