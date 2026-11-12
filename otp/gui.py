import tkinter as tk
from tkinter import filedialog, font, messagebox, ttk

from . import __version__
from .pad import ALPHABETS, DEFAULT_ALPHABET, generate_pad, pad_header, pad_id


class OneTimePadApp(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.master = master
        self.current_id = None

        self.alphabet = tk.StringVar(value=DEFAULT_ALPHABET)
        self.groups = tk.IntVar(value=50)
        self.group_size = tk.IntVar(value=5)
        self.status = tk.StringVar(value="Select Generate to create a pad.")

        self._build()
        self.grid(sticky="nsew")
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        master.bind("<Return>", lambda _e: self.generate())
        master.bind("<Control-s>", lambda _e: self.save())

    def _build(self):
        options = ttk.LabelFrame(self, text="Pad settings", padding=8)
        options.grid(row=0, column=0, sticky="ew")

        ttk.Label(options, text="Symbols").grid(row=0, column=0, sticky="w")
        ttk.Combobox(options, textvariable=self.alphabet, values=list(ALPHABETS),
                     state="readonly", width=16).grid(row=0, column=1, padx=(4, 16))

        ttk.Label(options, text="Groups").grid(row=0, column=2, sticky="w")
        ttk.Spinbox(options, from_=1, to=1000, textvariable=self.groups,
                    width=6).grid(row=0, column=3, padx=(4, 16))

        ttk.Label(options, text="Group size").grid(row=0, column=4, sticky="w")
        ttk.Spinbox(options, from_=1, to=20, textvariable=self.group_size,
                    width=4).grid(row=0, column=5, padx=4)

        self.generate_button = ttk.Button(self, text="Generate", command=self.generate)
        self.generate_button.grid(row=1, column=0, sticky="ew", pady=10, ipady=6)

        mono = font.nametofont("TkFixedFont").copy()
        mono.configure(size=12)
        text_frame = ttk.Frame(self)
        text_frame.grid(row=2, column=0, sticky="nsew")
        self.output = tk.Text(text_frame, height=14, width=64, font=mono,
                              wrap="none", state="disabled", padx=8, pady=8)
        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=scroll.set)
        self.output.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        actions = ttk.Frame(self)
        actions.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        ttk.Button(actions, text="Copy", command=self.copy).pack(side="left")
        ttk.Button(actions, text="Save...", command=self.save).pack(side="left", padx=6)
        ttk.Button(actions, text="Clear", command=self.clear).pack(side="left")
        ttk.Label(actions, text="Use each pad once, then destroy every copy.",
                  foreground="#a33").pack(side="right")

        ttk.Label(self, textvariable=self.status, anchor="w").grid(
            row=4, column=0, sticky="ew", pady=(8, 0))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def _read_settings(self):
        try:
            groups = int(self.groups.get())
            size = int(self.group_size.get())
        except (tk.TclError, ValueError):
            raise ValueError("Groups and group size must be whole numbers.")
        if not 1 <= groups <= 1000:
            raise ValueError("Groups must be between 1 and 1000.")
        if not 1 <= size <= 20:
            raise ValueError("Group size must be between 1 and 20.")
        return groups, size

    def _set_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def _pad_text(self):
        return self.output.get("1.0", "end-1c")

    def generate(self):
        try:
            groups, size = self._read_settings()
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc), parent=self.master)
            return
        name = self.alphabet.get()
        self.current_id = pad_id()
        body = generate_pad(groups, size, ALPHABETS[name])
        header = pad_header(self.current_id, name, groups, size)
        self._set_output(f"{header}\n\n{body}\n")
        self.status.set(f"Generated pad {self.current_id}: {groups * size} symbols.")

    def copy(self):
        text = self._pad_text()
        if not text:
            self.status.set("Nothing to copy yet.")
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.status.set(f"Pad {self.current_id} copied to clipboard.")

    def save(self):
        text = self._pad_text()
        if not text:
            self.status.set("Nothing to save yet.")
            return
        path = filedialog.asksaveasfilename(
            parent=self.master, defaultextension=".txt",
            initialfile=f"pad-{self.current_id}.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if not path:
            return
        with open(path, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        self.status.set(f"Pad {self.current_id} saved to {path}")

    def clear(self):
        self._set_output("")
        self.current_id = None
        self.status.set("Cleared.")


def main():
    root = tk.Tk()
    root.title(f"One-Time Pad Generator {__version__}")
    root.minsize(640, 420)
    style = ttk.Style(root)
    if "clam" in style.theme_names() and root.tk.call("tk", "windowingsystem") == "x11":
        style.theme_use("clam")
    OneTimePadApp(root)
    root.mainloop()
