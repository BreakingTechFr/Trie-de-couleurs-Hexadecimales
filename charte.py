import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def is_valid_hex_color(color):
    color = color.strip("#")
    return len(color) == 6 and all(c.isdigit() or c.lower() in 'abcdef' for c in color)

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_primary_color(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    primary_colors = {
        "Rouge": r,
        "Vert": g,
        "Bleu": b
    }
    primary_colors = sorted(primary_colors.items(), key=lambda x: x[1], reverse=True)
    return primary_colors[0][0]

def get_luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    luminance = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return luminance

def sort_colors(colors):
    colors.sort(key=lambda color: (get_primary_color(color), get_luminance(color)), reverse=True)

def group_colors(colors):
    grouped_colors = {}
    for color in colors:
        primary_color = get_primary_color(color)
        if primary_color not in grouped_colors:
            grouped_colors[primary_color] = []
        grouped_colors[primary_color].append(color)
    return grouped_colors

def extract_colors(groups):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                for primary_color, colors in groups.items():
                    file.write(f"{primary_color}:\n")
                    for color in colors:
                        file.write(f"    {color}\n")
            messagebox.showinfo("Extraction réussie", "Les couleurs ont été extraites avec succès dans le fichier.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'écriture du fichier : {str(e)}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt")])
    if file_path:
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                hex_colors = [line.strip() for line in lines if is_valid_hex_color(line.strip())]
                sort_colors(hex_colors)
                grouped_colors = group_colors(hex_colors)
                display_colors(grouped_colors)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la lecture du fichier : {str(e)}")

def close_windows(root, result_window):
    if result_window:
        result_window.destroy()
    root.quit()  # Quitte uniquement la fenêtre principale

def exit_program(root):
    root.destroy()  # Ferme la fenêtre principale
    sys.exit()  # Quitte le script complètement

def display_colors(groups):
    result_window = tk.Tk()
    result_window.title("Résultat")
    result_window.geometry("400x1000")

    canvas_frame = tk.Frame(result_window)
    canvas_frame.pack(fill="both", expand=True)

    y_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
    y_scrollbar.pack(side="right", fill="y")

    canvas = tk.Canvas(canvas_frame, yscrollcommand=y_scrollbar.set)
    canvas.pack(fill="both", expand=True)

    y_scrollbar.config(command=canvas.yview)

    columns_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=columns_frame, anchor="nw")

    def update_canvas_size(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    columns_frame.bind("<Configure>", update_canvas_size)

    vert_frame = tk.Frame(columns_frame)
    vert_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

    rouge_frame = tk.Frame(columns_frame)
    rouge_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    bleu_frame = tk.Frame(columns_frame)
    bleu_frame.grid(row=0, column=2, padx=10, pady=10, sticky="n")

    for primary_color, colors in groups.items():
        if primary_color == "Vert":
            column_frame = vert_frame
        elif primary_color == "Rouge":
            column_frame = rouge_frame
        elif primary_color == "Bleu":
            column_frame = bleu_frame
        else:
            continue

        tk.Label(column_frame, text=primary_color, font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2)

        for i, color in enumerate(colors, start=1):
            rgb = hex_to_rgb(color)
            color_label = tk.Label(column_frame, text=color, font=("Helvetica", 12))
            color_label.grid(row=i, column=0, sticky="w")
            color_canvas = tk.Canvas(column_frame, width=30, height=30, bg="#{:02x}{:02x}{:02x}".format(*rgb))
            color_canvas.grid(row=i, column=1, padx=5, pady=5)

    extract_button = tk.Button(result_window, text="Extraire", command=lambda: extract_colors(groups))
    extract_button.pack(pady=10)


    result_window.mainloop()

root = tk.Tk()
root.title("Tri des Couleurs by BreakingTech")
root.geometry("320x100")

browse_button = tk.Button(root, text="Parcourir", command=browse_file)
browse_button.pack(pady=10)

quit_button = tk.Button(root, text="Quitter", command=lambda: exit_program(root))
quit_button.pack(pady=10)

root.mainloop()
