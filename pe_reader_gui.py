#!/usr/bin/env python3
"""
Interface graphique pour le lecteur PE
Utilise tkinter pour une interface conviviale
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pe_reader import PEReader
import io
import sys

class PEReaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur PE - Analyseur de fichiers exécutables Windows")
        self.root.geometry("1000x700")
        
        # Variables
        self.current_file = tk.StringVar()
        self.analysis_running = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration de la grille
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Section de sélection de fichier
        file_frame = ttk.LabelFrame(main_frame, text="Fichier PE", padding="5")
        file_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(file_frame, text="Fichier:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.current_file, state='readonly')
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_btn = ttk.Button(file_frame, text="Parcourir...", command=self.browse_file)
        self.browse_btn.grid(row=0, column=2)
        
        self.analyze_btn = ttk.Button(file_frame, text="Analyser", command=self.analyze_file, state='disabled')
        self.analyze_btn.grid(row=0, column=3, padx=(5, 0))
        
        # Barre de progression
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Zone de résultats
        results_frame = ttk.LabelFrame(main_frame, text="Résultats de l'analyse", padding="5")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Notebook pour organiser les résultats
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Onglets
        self.create_tabs()
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_tabs(self):
        """Crée les onglets pour les différentes sections d'analyse"""
        # Onglet Vue d'ensemble
        self.overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.overview_frame, text="Vue d'ensemble")
        
        self.overview_text = scrolledtext.ScrolledText(self.overview_frame, wrap=tk.WORD, 
                                                      font=('Consolas', 10))
        self.overview_text.pack(fill=tk.BOTH, expand=True)
        
        # Onglet En-têtes
        self.headers_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.headers_frame, text="En-têtes")
        
        self.headers_text = scrolledtext.ScrolledText(self.headers_frame, wrap=tk.WORD,
                                                     font=('Consolas', 10))
        self.headers_text.pack(fill=tk.BOTH, expand=True)
        
        # Onglet Sections
        self.sections_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sections_frame, text="Sections")
        
        # Treeview pour les sections
        self.sections_tree = ttk.Treeview(self.sections_frame, columns=('va', 'size', 'raw_size', 'chars'), 
                                         show='tree headings')
        self.sections_tree.heading('#0', text='Nom')
        self.sections_tree.heading('va', text='Adresse virtuelle')
        self.sections_tree.heading('size', text='Taille virtuelle')
        self.sections_tree.heading('raw_size', text='Taille fichier')
        self.sections_tree.heading('chars', text='Caractéristiques')
        
        # Scrollbars pour le treeview
        sections_scrolly = ttk.Scrollbar(self.sections_frame, orient=tk.VERTICAL, 
                                        command=self.sections_tree.yview)
        sections_scrollx = ttk.Scrollbar(self.sections_frame, orient=tk.HORIZONTAL, 
                                        command=self.sections_tree.xview)
        self.sections_tree.configure(yscrollcommand=sections_scrolly.set, 
                                    xscrollcommand=sections_scrollx.set)
        
        self.sections_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sections_scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        sections_scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Onglet Log complet
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="Log complet")
        
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD,
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def browse_file(self):
        """Ouvre un dialogue pour sélectionner un fichier PE"""
        filetypes = [
            ('Fichiers exécutables', '*.exe;*.dll;*.sys;*.ocx'),
            ('Tous les fichiers', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier PE",
            filetypes=filetypes
        )
        
        if filename:
            self.current_file.set(filename)
            self.analyze_btn.config(state='normal')
            self.clear_results()
            self.status_var.set(f"Fichier sélectionné: {os.path.basename(filename)}")
    
    def clear_results(self):
        """Efface les résultats précédents"""
        self.overview_text.delete(1.0, tk.END)
        self.headers_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        # Effacer le treeview des sections
        for item in self.sections_tree.get_children():
            self.sections_tree.delete(item)
    
    def analyze_file(self):
        """Lance l'analyse du fichier PE dans un thread séparé"""
        if self.analysis_running:
            return
            
        filepath = self.current_file.get()
        if not filepath or not os.path.exists(filepath):
            messagebox.showerror("Erreur", "Veuillez sélectionner un fichier valide")
            return
        
        # Démarrer l'analyse dans un thread
        self.analysis_running = True
        self.analyze_btn.config(state='disabled')
        self.progress.start()
        self.status_var.set("Analyse en cours...")
        
        thread = threading.Thread(target=self.run_analysis, args=(filepath,))
        thread.daemon = True
        thread.start()
    
    def run_analysis(self, filepath):
        """Exécute l'analyse PE"""
        try:
            # Capturer la sortie
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            # Créer et exécuter le lecteur PE
            reader = PEReader(filepath)
            success = reader.analyze()
            
            if success:
                reader.display_results()
                output = captured_output.getvalue()
                
                # Planifier la mise à jour de l'interface dans le thread principal
                self.root.after(0, self.update_results, reader, output, True)
            else:
                error_output = captured_output.getvalue()
                self.root.after(0, self.update_results, None, error_output, False)
                
        except Exception as e:
            error_msg = f"Erreur lors de l'analyse: {str(e)}"
            self.root.after(0, self.update_results, None, error_msg, False)
        finally:
            sys.stdout = old_stdout
            self.root.after(0, self.analysis_complete)
    
    def update_results(self, reader, output, success):
        """Met à jour l'interface avec les résultats"""
        if success and reader:
            # Vue d'ensemble
            overview = self.generate_overview(reader)
            self.overview_text.insert(tk.END, overview)
            
            # En-têtes détaillés
            headers = self.generate_headers_info(reader)
            self.headers_text.insert(tk.END, headers)
            
            # Sections dans le treeview
            self.populate_sections_tree(reader)
            
            self.status_var.set(f"Analyse terminée - {len(reader.sections)} sections trouvées")
        else:
            self.overview_text.insert(tk.END, "Erreur lors de l'analyse du fichier PE\n")
            self.status_var.set("Erreur lors de l'analyse")
        
        # Log complet
        self.log_text.insert(tk.END, output)
        
    def generate_overview(self, reader):
        """Génère un résumé de l'analyse"""
        overview = "=== RÉSUMÉ DE L'ANALYSE ===\n\n"
        
        # Informations de base
        overview += f"Fichier: {os.path.basename(reader.filepath)}\n"
        overview += f"Taille: {len(reader.data):,} bytes\n\n"
        
        # Type de machine
        overview += f"Architecture: {reader.get_machine_type()}\n"
        
        # Type de fichier
        characteristics = reader.get_characteristics()
        if "DLL" in characteristics:
            file_type = "DLL (Dynamic Link Library)"
        elif "Executable image" in characteristics:
            file_type = "Exécutable"
        elif "System file" in characteristics:
            file_type = "Fichier système"
        else:
            file_type = "Inconnu"
        
        overview += f"Type: {file_type}\n\n"
        
        # Informations sur l'en-tête optionnel
        if reader.optional_header:
            is_pe32_plus = reader.optional_header['magic'] == 0x20b
            overview += f"Format: {'PE32+' if is_pe32_plus else 'PE32'}\n"
            overview += f"Point d'entrée: 0x{reader.optional_header['address_of_entry_point']:08x}\n"
            overview += f"Base de l'image: 0x{reader.optional_header['image_base']:08x}\n\n"
        
        # Sections
        overview += f"Nombre de sections: {len(reader.sections)}\n"
        if reader.sections:
            overview += "Sections:\n"
            for section in reader.sections:
                overview += f"  • {section['name']} ({section['virtual_size']:,} bytes)\n"
        
        return overview
    
    def generate_headers_info(self, reader):
        """Génère les informations détaillées des en-têtes"""
        info = "=== EN-TÊTES DÉTAILLÉS ===\n\n"
        
        # En-tête DOS
        info += "EN-TÊTE DOS:\n"
        info += f"  Signature: 0x{reader.dos_header['signature']:04x}\n"
        info += f"  Offset PE: 0x{reader.dos_header['pe_header_offset']:08x}\n\n"
        
        # En-tête PE/COFF
        info += "EN-TÊTE PE/COFF:\n"
        info += f"  Signature: 0x{reader.pe_header['signature']:08x}\n"
        info += f"  Machine: 0x{reader.pe_header['machine']:04x} ({reader.get_machine_type()})\n"
        info += f"  Nombre de sections: {reader.pe_header['number_of_sections']}\n"
        
        from datetime import datetime
        timestamp = datetime.fromtimestamp(reader.pe_header['time_date_stamp'])
        info += f"  Date de compilation: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"  Taille en-tête optionnel: {reader.pe_header['size_of_optional_header']}\n"
        info += f"  Caractéristiques: 0x{reader.pe_header['characteristics']:04x}\n"
        
        # Caractéristiques détaillées
        characteristics = reader.get_characteristics()
        if characteristics:
            info += "  Flags:\n"
            for char in characteristics:
                info += f"    • {char}\n"
        
        # En-tête optionnel
        if reader.optional_header:
            info += "\nEN-TÊTE OPTIONNEL:\n"
            info += f"  Magic: 0x{reader.optional_header['magic']:04x}\n"
            info += f"  Version linker: {reader.optional_header['major_linker_version']}.{reader.optional_header['minor_linker_version']}\n"
            info += f"  Taille du code: {reader.optional_header['size_of_code']:,} bytes\n"
            info += f"  Taille données initialisées: {reader.optional_header['size_of_initialized_data']:,} bytes\n"
            info += f"  Taille données non-initialisées: {reader.optional_header['size_of_uninitialized_data']:,} bytes\n"
            info += f"  Point d'entrée: 0x{reader.optional_header['address_of_entry_point']:08x}\n"
            info += f"  Base du code: 0x{reader.optional_header['base_of_code']:08x}\n"
            info += f"  Base de l'image: 0x{reader.optional_header['image_base']:08x}\n"
        
        return info
    
    def populate_sections_tree(self, reader):
        """Remplit le treeview avec les informations des sections"""
        for i, section in enumerate(reader.sections):
            # Caractéristiques principales
            chars = reader.get_section_characteristics(section['characteristics'])
            chars_str = ", ".join(chars[:3])  # Limiter l'affichage
            if len(chars) > 3:
                chars_str += "..."
            
            self.sections_tree.insert('', 'end', 
                                     text=section['name'],
                                     values=(
                                         f"0x{section['virtual_address']:08x}",
                                         f"{section['virtual_size']:,}",
                                         f"{section['size_of_raw_data']:,}",
                                         chars_str
                                     ))
    
    def analysis_complete(self):
        """Appelé quand l'analyse est terminée"""
        self.analysis_running = False
        self.analyze_btn.config(state='normal')
        self.progress.stop()

def main():
    """Fonction principale"""
    root = tk.Tk()
    app = PEReaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()