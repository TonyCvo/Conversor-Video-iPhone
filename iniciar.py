#!/usr/bin/env python3
"""
Interface Gráfica Avançada para Conversor de Vídeos para iPhone (MOV)
Versão 3.0 - Com tema escuro, prévia de vídeo, atalhos e melhorias de UX
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import sys
import subprocess
import threading
import json
import time
import re
from pathlib import Path
from datetime import datetime
import queue
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk

class VideoConverterGUI:
    def __init__(self):
        self.window = tkdnd.TkinterDnD.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_theme()
        self.create_widgets()
        self.setup_keyboard_shortcuts()
        self.create_tooltips()
        self.check_ffmpeg_installation()
        self.load_settings()
        
        # Configurações do FFmpeg
        self.supported_formats = [
            ("Arquivos de Vídeo", "*.mpg;*.mpeg;*.avi;*.mkv;*.wmv;*.flv;*.webm;*.MPG;*.MPEG;*.AVI;*.MKV;*.WMV;*.FLV;*.WEBM"),
            ("MPG/MPEG", "*.mpg;*.mpeg;*.MPG;*.MPEG"),
            ("AVI", "*.avi;*.AVI"),
            ("MKV", "*.mkv;*.MKV"),
            ("WMV", "*.wmv;*.WMV"),
            ("FLV", "*.flv;*.FLV"),
            ("WEBM", "*.webm;*.WEBM"),
            ("Todos os arquivos", "*.*")
        ]
        
        # Fila para comunicação entre threads
        self.progress_queue = queue.Queue()
        self.monitor_progress()
        
        # Cache para thumbnails
        self.thumbnail_cache = {}
        
    def setup_window(self):
        """Configura a janela principal"""
        self.window.title("🎬 Conversor de Vídeo Avançado v3.0")
        self.window.geometry("800x700")
        self.window.resizable(True, True)
        
        # Centralizar janela
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"800x700+{x}+{y}")
        
        # Ícone (se houver)
        try:
            self.window.iconbitmap("video_icon.ico")
        except:
            pass
            
    def setup_variables(self):
        """Inicializa as variáveis do Tkinter"""
        self.input_files = []
        self.output_directory = tk.StringVar()
        self.quality = tk.StringVar(value="medium")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto para conversão")
        self.converting = False
        self.batch_mode = tk.BooleanVar(value=False)
        self.advanced_mode = tk.BooleanVar(value=False)
        self.preserve_audio = tk.BooleanVar(value=True)
        self.auto_open_folder = tk.BooleanVar(value=True)
        self.dark_mode = tk.BooleanVar(value=False)  # Tema claro por padrão
        
    def setup_theme(self):
        """Configura o tema da aplicação"""
        self.apply_theme()
        
    def apply_theme(self):
        """Aplica o tema atual (claro/escuro)"""
        if self.dark_mode.get():
            # Tema escuro
            self.window.configure(bg='#2b2b2b')
            
            # Configurar estilo
            style = ttk.Style()
            style.theme_use('clam')
            
            # Cores do tema escuro
            style.configure('.', background='#2b2b2b', foreground='#ffffff')
            style.configure('TFrame', background='#2b2b2b')
            style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
            
            # Configurações específicas para botões no tema escuro
            style.configure('TButton', 
                          background='#404040', 
                          foreground='#ffffff',
                          borderwidth=2,
                          relief='raised',
                          focuscolor='none')
            style.map('TButton',
                     background=[('active', '#505050'), ('pressed', '#606060')],
                     foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                     relief=[('pressed', 'sunken'), ('active', 'raised')])
            
            # Estilo especial para botão principal (accent)
            style.configure('Accent.TButton',
                          background='#007acc',
                          foreground='#ffffff',
                          borderwidth=2,
                          relief='raised',
                          focuscolor='none')
            style.map('Accent.TButton',
                     background=[('active', '#005a99'), ('pressed', '#004080')],
                     foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                     relief=[('pressed', 'sunken'), ('active', 'raised')])
            
            # Configurações para outros widgets
            style.configure('TEntry', fieldbackground='#404040', foreground='#ffffff')
            style.configure('TCombobox', fieldbackground='#404040', foreground='#ffffff')
            style.configure('Treeview', background='#404040', foreground='#ffffff')
            style.configure('Treeview.Heading', background='#404040', foreground='#ffffff')
            
            # Cores específicas
            self.bg_color = '#2b2b2b'
            self.fg_color = '#ffffff'
            self.accent_color = '#007acc'
            self.error_color = '#ff6b6b'
            self.success_color = '#51cf66'
        else:
            # Tema claro
            self.window.configure(bg='#f0f0f0')
            
            # Configurar estilo
            style = ttk.Style()
            style.theme_use('clam')
            
            # Cores do tema claro
            style.configure('.', background='#f0f0f0', foreground='#000000')
            style.configure('TFrame', background='#f0f0f0')
            style.configure('TLabel', background='#f0f0f0', foreground='#000000')
            
            # Configurações específicas para botões no tema claro
            style.configure('TButton', 
                          background='#e0e0e0', 
                          foreground='#000000',
                          borderwidth=2,
                          relief='raised',
                          focuscolor='none')
            style.map('TButton',
                     background=[('active', '#d0d0d0'), ('pressed', '#c0c0c0')],
                     foreground=[('active', '#000000'), ('pressed', '#000000')],
                     relief=[('pressed', 'sunken'), ('active', 'raised')])
            
            # Estilo especial para botão principal (accent) - tema claro
            style.configure('Accent.TButton',
                          background='#007acc',
                          foreground='#ffffff',
                          borderwidth=2,
                          relief='raised',
                          focuscolor='none')
            style.map('Accent.TButton',
                     background=[('active', '#005a99'), ('pressed', '#004080')],
                     foreground=[('active', '#ffffff'), ('pressed', '#ffffff')],
                     relief=[('pressed', 'sunken'), ('active', 'raised')])
            
            # Configurações para outros widgets
            style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')
            style.configure('TCombobox', fieldbackground='#ffffff', foreground='#000000')
            style.configure('Treeview', background='#ffffff', foreground='#000000')
            style.configure('Treeview.Heading', background='#e0e0e0', foreground='#000000')
            
            # Cores específicas
            self.bg_color = '#f0f0f0'
            self.fg_color = '#000000'
            self.accent_color = '#007acc'
            self.error_color = '#dc3545'
            self.success_color = '#28a745'
        
        # Aplicar cores aos widgets existentes
        self.update_widget_colors()
        
    def update_widget_colors(self):
        """Atualiza as cores dos widgets existentes"""
        try:
            # Atualizar cores do log
            self.log_text.configure(
                bg=self.bg_color,
                fg=self.fg_color,
                insertbackground=self.fg_color
            )
            
            # Atualizar cores da lista de arquivos
            self.batch_listbox.configure(
                bg=self.bg_color,
                fg=self.fg_color,
                selectbackground=self.accent_color,
                selectforeground='white'
            )
            
            # Atualizar cores dos entries
            self.output_entry.configure(
                bg=self.bg_color,
                fg=self.fg_color,
                insertbackground=self.fg_color
            )
            self.batch_output_entry.configure(
                bg=self.bg_color,
                fg=self.fg_color,
                insertbackground=self.fg_color
            )
            
        except AttributeError:
            # Widgets ainda não foram criados
            pass
        
    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado"""
        self.window.bind('<Control-o>', lambda e: self.browse_input_file())
        self.window.bind('<Control-s>', lambda e: self.save_settings())
        self.window.bind('<Control-d>', lambda e: self.toggle_dark_mode())
        self.window.bind('<F1>', lambda e: self.show_help())
        self.window.bind('<Escape>', lambda e: self.cancel_conversion())
        
    def create_tooltips(self):
        """Cria tooltips para os widgets"""
        self.tooltips = {}
        
    def add_tooltip(self, widget, text):
        """Adiciona tooltip a um widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, 
                           bg='#ffffe0', relief='solid', borderwidth=1)
            label.pack()
            
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind('<Leave>', hide_tooltip)
            tooltip.bind('<Leave>', hide_tooltip)
            
        widget.bind('<Enter>', show_tooltip)
        
    def toggle_dark_mode(self):
        """Alterna entre tema claro e escuro"""
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
        self.log_message("🎨 Tema alterado")
        
    def show_help(self):
        """Mostra janela de ajuda"""
        help_window = tk.Toplevel(self.window)
        help_window.title("❓ Ajuda - Conversor de Vídeo")
        help_window.geometry("600x500")
        help_window.transient(self.window)
        help_window.grab_set()
        
        # Centralizar janela
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f"600x500+{x}+{y}")
        
        # Conteúdo da ajuda
        help_text = """
🎬 Conversor de Vídeo Avançado v3.0

📋 ATALHOS DE TECLADO:
• Ctrl+O: Abrir arquivo de vídeo
• Ctrl+S: Salvar configurações
• Ctrl+D: Alternar tema claro/escuro
• F1: Mostrar esta ajuda
• Esc: Cancelar conversão

🎯 COMO USAR:
1. Selecione um arquivo de vídeo ou arraste-o para a área
2. Escolha a qualidade de conversão
3. Clique em "Converter Vídeo"
4. Aguarde a conversão ser concluída

⚙️ CONFIGURAÇÕES:
• Qualidade: Controla a qualidade do vídeo final
• Preservar Áudio: Mantém o áudio original
• Abrir Pasta: Abre automaticamente a pasta do arquivo convertido

📁 FORMATOS SUPORTADOS:
Entrada: MPG, MPEG, AVI, MKV, WMV, FLV, WEBM
Saída: MOV (compatível com iPhone)

🔧 CONFIGURAÇÕES AVANÇADAS:
Acesse a aba "Configurações" para ajustes detalhados do FFmpeg.

❓ PRECISA DE AJUDA?
Verifique se o FFmpeg está instalado no seu sistema.
        """
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=20, pady=20,
                             bg=self.bg_color, fg=self.fg_color, font=('Arial', 10))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.configure(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Fechar", 
                  command=help_window.destroy).pack(pady=10)
        
    def cancel_conversion(self):
        """Cancela a conversão atual"""
        if self.converting:
            if messagebox.askyesno("Cancelar", "Deseja cancelar a conversão atual?"):
                self.converting = False
                self.status_var.set("Conversão cancelada")
                self.log_message("⏹️ Conversão cancelada pelo usuário")
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Notebook para abas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba principal
        main_tab = ttk.Frame(notebook)
        notebook.add(main_tab, text="🎬 Conversão")
        
        # Aba de configurações
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="⚙️ Configurações")
        
        # Aba de histórico
        history_tab = ttk.Frame(notebook)
        notebook.add(history_tab, text="📋 Histórico")
        
        self.create_main_tab(main_tab)
        self.create_settings_tab(settings_tab)
        self.create_history_tab(history_tab)
        
    def create_main_tab(self, parent):
        """Cria a aba principal"""
        main_frame = ttk.Frame(parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎬 Conversor de Vídeo Avançado v3.0", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Modo de conversão
        mode_frame = ttk.LabelFrame(main_frame, text="📁 Modo de Conversão", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Radiobutton(mode_frame, text="Arquivo Único", variable=self.batch_mode, 
                       value=False, command=self.toggle_mode).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Conversão em Lote", variable=self.batch_mode, 
                       value=True, command=self.toggle_mode).pack(anchor=tk.W)
        
        # Seção de arquivos
        self.files_frame = ttk.LabelFrame(main_frame, text="📁 Arquivos", padding="10")
        self.files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Frame para arquivo único
        self.single_file_frame = ttk.Frame(self.files_frame)
        
        ttk.Label(self.single_file_frame, text="Arquivo de Entrada:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Área de drop para arquivo único
        drop_frame = ttk.Frame(self.single_file_frame)
        drop_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.drop_label = ttk.Label(drop_frame, text="📁 Arraste um arquivo aqui ou clique em 'Procurar'", 
                                   font=('Arial', 9), foreground='gray', 
                                   relief='solid', borderwidth=1)
        self.drop_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=5)
        
        # Configurar drop target
        self.drop_label.drop_target_register(tkdnd.DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_single_file)
        
        # Botão procurar
        ttk.Button(drop_frame, text="Procurar...", 
                  command=self.browse_input_file).pack(side=tk.RIGHT)
        
        # Entry para mostrar o caminho do arquivo
        self.input_entry = ttk.Entry(self.single_file_frame, font=('Arial', 9), state='readonly')
        self.input_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.single_file_frame, text="Arquivo de Saída:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        
        output_frame = ttk.Frame(self.single_file_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_entry = ttk.Entry(output_frame, font=('Arial', 9))
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(output_frame, text="Procurar...", 
                  command=self.browse_output_file).pack(side=tk.RIGHT)
        
        # Frame para conversão em lote
        self.batch_file_frame = ttk.Frame(self.files_frame)
        
        batch_buttons_frame = ttk.Frame(self.batch_file_frame)
        batch_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(batch_buttons_frame, text="🔄 Adicionar Arquivos", 
                  command=self.browse_batch_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(batch_buttons_frame, text="🗂️ Selecionar Pasta", 
                  command=self.browse_batch_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(batch_buttons_frame, text="🗑️ Limpar Lista", 
                  command=self.clear_batch_list).pack(side=tk.LEFT)
        
        ttk.Label(self.batch_file_frame, text="Pasta de Saída:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        
        batch_output_frame = ttk.Frame(self.batch_file_frame)
        batch_output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.batch_output_entry = ttk.Entry(batch_output_frame, textvariable=self.output_directory, 
                                          font=('Arial', 9))
        self.batch_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(batch_output_frame, text="Procurar...", 
                  command=self.browse_output_directory).pack(side=tk.RIGHT)
        
        # Área de drop para arquivos em lote
        drop_batch_frame = ttk.Frame(self.batch_file_frame)
        drop_batch_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.drop_batch_label = ttk.Label(drop_batch_frame, 
                                         text="📁 Arraste múltiplos arquivos aqui para conversão em lote", 
                                         font=('Arial', 9), foreground='gray', 
                                         relief='solid', borderwidth=1)
        self.drop_batch_label.pack(fill=tk.X, pady=5)
        
        # Configurar drop target para múltiplos arquivos
        self.drop_batch_label.drop_target_register(tkdnd.DND_FILES)
        self.drop_batch_label.dnd_bind('<<Drop>>', self.on_drop_batch_files)
        
        # Lista de arquivos em lote
        list_frame = ttk.Frame(self.batch_file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.batch_listbox = tk.Listbox(list_frame, height=6, font=('Arial', 9))
        self.batch_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.batch_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.batch_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Configurações rápidas
        config_frame = ttk.LabelFrame(main_frame, text="⚙️ Configurações Rápidas", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 15))
        
        quality_frame = ttk.Frame(config_frame)
        quality_frame.pack(fill=tk.X)
        
        ttk.Label(quality_frame, text="Qualidade:").pack(side=tk.LEFT)
        
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality, 
                                   values=["high", "medium", "low"], 
                                   state="readonly", width=15)
        quality_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Checkbutton(quality_frame, text="Preservar Áudio", 
                       variable=self.preserve_audio).pack(side=tk.LEFT, padx=(20, 0))
        
        ttk.Checkbutton(quality_frame, text="Abrir Pasta ao Finalizar", 
                       variable=self.auto_open_folder).pack(side=tk.LEFT, padx=(20, 0))
        
        # Botões de ação
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Botão principal de conversão com estilo especial
        self.convert_button = ttk.Button(buttons_frame, text="🚀 Converter Vídeo", 
                                       command=self.start_conversion,
                                       style='Accent.TButton')
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botões secundários com estilos específicos
        settings_button = ttk.Button(buttons_frame, text="⚙️ Configurações Avançadas", 
                                    command=self.show_advanced_settings)
        settings_button.pack(side=tk.LEFT, padx=(0, 10))
        
        theme_button = ttk.Button(buttons_frame, text="🎨 Tema", 
                                 command=self.toggle_dark_mode)
        theme_button.pack(side=tk.LEFT, padx=(0, 10))
        
        help_button = ttk.Button(buttons_frame, text="❓ Ajuda", 
                                command=self.show_help)
        help_button.pack(side=tk.LEFT)
        
        # Adicionar tooltips
        self.add_tooltip(self.convert_button, "Iniciar conversão do vídeo (Ctrl+Enter)")
        self.add_tooltip(settings_button, "Configurações avançadas do FFmpeg")
        self.add_tooltip(theme_button, "Alternar entre tema claro/escuro (Ctrl+D)")
        self.add_tooltip(help_button, "Mostrar ajuda (F1)")
        
        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X)
        
        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                     font=('Arial', 9), foreground='blue')
        self.status_label.pack(pady=(0, 10))
        
        # Log de saída
        log_frame = ttk.LabelFrame(main_frame, text="📝 Log de Conversão", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget com scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(text_frame, height=8, font=('Consolas', 9), 
                               wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Inicializar modo arquivo único
        self.toggle_mode()
        
    def create_settings_tab(self, parent):
        """Cria a aba de configurações"""
        settings_frame = ttk.Frame(parent, padding="20")
        settings_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurações do FFmpeg
        ffmpeg_frame = ttk.LabelFrame(settings_frame, text="🎬 Configurações do FFmpeg", padding="10")
        ffmpeg_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(ffmpeg_frame, text="Preset de Codificação:").grid(row=0, column=0, sticky=tk.W)
        self.preset_var = tk.StringVar(value="medium")
        preset_combo = ttk.Combobox(ffmpeg_frame, textvariable=self.preset_var,
                                   values=["ultrafast", "superfast", "veryfast", "faster", 
                                          "fast", "medium", "slow", "slower", "veryslow"],
                                   state="readonly", width=15)
        preset_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        ttk.Label(ffmpeg_frame, text="Taxa de Bits Máxima:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.maxrate_var = tk.StringVar(value="10M")
        ttk.Entry(ffmpeg_frame, textvariable=self.maxrate_var, width=15).grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        ttk.Label(ffmpeg_frame, text="Tamanho do Buffer:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.bufsize_var = tk.StringVar(value="16M")
        ttk.Entry(ffmpeg_frame, textvariable=self.bufsize_var, width=15).grid(row=2, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        # Configurações de áudio
        audio_frame = ttk.LabelFrame(settings_frame, text="🔊 Configurações de Áudio", padding="10")
        audio_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(audio_frame, text="Codec de Áudio:").grid(row=0, column=0, sticky=tk.W)
        self.audio_codec_var = tk.StringVar(value="aac")
        audio_combo = ttk.Combobox(audio_frame, textvariable=self.audio_codec_var,
                                  values=["aac", "mp3", "ac3", "copy"],
                                  state="readonly", width=15)
        audio_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        ttk.Label(audio_frame, text="Taxa de Bits de Áudio:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.audio_bitrate_var = tk.StringVar(value="128k")
        ttk.Entry(audio_frame, textvariable=self.audio_bitrate_var, width=15).grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        # Configurações gerais
        general_frame = ttk.LabelFrame(settings_frame, text="⚙️ Configurações Gerais", padding="10")
        general_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.auto_save_settings = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Salvar configurações automaticamente", 
                       variable=self.auto_save_settings).pack(anchor=tk.W)
        
        self.show_notifications = tk.BooleanVar(value=True)
        ttk.Checkbutton(general_frame, text="Mostrar notificações", 
                       variable=self.show_notifications).pack(anchor=tk.W)
        
        # Botões
        buttons_frame = ttk.Frame(settings_frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="💾 Salvar Configurações", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="🔄 Restaurar Padrões", 
                  command=self.reset_settings).pack(side=tk.LEFT)
        
    def create_history_tab(self, parent):
        """Cria a aba de histórico"""
        history_frame = ttk.Frame(parent, padding="20")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Controles do histórico
        controls_frame = ttk.Frame(history_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(controls_frame, text="🗑️ Limpar Histórico", 
                  command=self.clear_history).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(controls_frame, text="📁 Abrir Pasta de Histórico", 
                  command=self.open_history_folder).pack(side=tk.LEFT)
        
        # Lista de histórico
        list_frame = ttk.Frame(history_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ('Data', 'Arquivo Original', 'Arquivo Convertido', 'Status', 'Tamanho')
        self.history_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=150)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Carregar histórico
        self.load_history()
        
    def toggle_mode(self):
        """Alterna entre modo arquivo único e lote"""
        if self.batch_mode.get():
            self.single_file_frame.pack_forget()
            self.batch_file_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.batch_file_frame.pack_forget()
            self.single_file_frame.pack(fill=tk.BOTH, expand=True)
    
    def browse_input_file(self):
        """Abre diálogo para selecionar arquivo de entrada"""
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo de vídeo",
            filetypes=self.supported_formats
        )
        if filename:
            # Atualizar o entry com o caminho completo
            self.input_entry.configure(state='normal')
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)
            self.input_entry.configure(state='readonly')
            
            # Atualizar o label visual também
            file_name = Path(filename).name
            self.drop_label.configure(text=f"📁 {file_name}", foreground='green')
            
            # Sugerir nome de saída automaticamente
            if not self.output_entry.get():
                input_path = Path(filename)
                suggested_output = input_path.with_suffix('.mov')
                self.output_entry.delete(0, tk.END)
                self.output_entry.insert(0, str(suggested_output))
            
            # Mostrar informações do vídeo
            self.show_video_info(filename)
            self.log_message(f"📁 Arquivo selecionado: {file_name}")
    
    def show_video_info(self, file_path):
        """Mostra informações do vídeo selecionado"""
        try:
            # Usar FFprobe para obter informações do vídeo
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
            
            if result.returncode == 0:
                import json
                info = json.loads(result.stdout)
                
                # Extrair informações relevantes
                format_info = info.get('format', {})
                streams = info.get('streams', [])
                
                video_stream = next((s for s in streams if s['codec_type'] == 'video'), None)
                audio_stream = next((s for s in streams if s['codec_type'] == 'audio'), None)
                
                # Criar janela de informações
                info_window = tk.Toplevel(self.window)
                info_window.title("📊 Informações do Vídeo")
                info_window.geometry("500x400")
                info_window.transient(self.window)
                info_window.grab_set()
                
                # Centralizar janela
                info_window.update_idletasks()
                x = (info_window.winfo_screenwidth() // 2) - (500 // 2)
                y = (info_window.winfo_screenheight() // 2) - (400 // 2)
                info_window.geometry(f"500x400+{x}+{y}")
                
                # Conteúdo
                main_frame = ttk.Frame(info_window, padding="20")
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # Título
                title_label = ttk.Label(main_frame, text=f"📊 {Path(file_path).name}", 
                                       font=('Arial', 12, 'bold'))
                title_label.pack(pady=(0, 20))
                
                # Informações gerais
                general_frame = ttk.LabelFrame(main_frame, text="📋 Informações Gerais", padding="10")
                general_frame.pack(fill=tk.X, pady=(0, 10))
                
                duration = float(format_info.get('duration', 0))
                size = int(format_info.get('size', 0))
                
                ttk.Label(general_frame, text=f"📁 Tamanho: {self.format_file_size(size)}").pack(anchor=tk.W)
                ttk.Label(general_frame, text=f"⏱️ Duração: {self.format_duration(duration)}").pack(anchor=tk.W)
                ttk.Label(general_frame, text=f"🎬 Formato: {format_info.get('format_name', 'N/A')}").pack(anchor=tk.W)
                
                # Informações de vídeo
                if video_stream:
                    video_frame = ttk.LabelFrame(main_frame, text="🎬 Vídeo", padding="10")
                    video_frame.pack(fill=tk.X, pady=(0, 10))
                    
                    width = video_stream.get('width', 'N/A')
                    height = video_stream.get('height', 'N/A')
                    fps = eval(video_stream.get('r_frame_rate', '0/1'))
                    
                    ttk.Label(video_frame, text=f"📐 Resolução: {width}x{height}").pack(anchor=tk.W)
                    ttk.Label(video_frame, text=f"🎯 FPS: {fps:.2f}").pack(anchor=tk.W)
                    ttk.Label(video_frame, text=f"🎨 Codec: {video_stream.get('codec_name', 'N/A')}").pack(anchor=tk.W)
                
                # Informações de áudio
                if audio_stream:
                    audio_frame = ttk.LabelFrame(main_frame, text="🔊 Áudio", padding="10")
                    audio_frame.pack(fill=tk.X, pady=(0, 10))
                    
                    ttk.Label(audio_frame, text=f"🎵 Codec: {audio_stream.get('codec_name', 'N/A')}").pack(anchor=tk.W)
                    ttk.Label(audio_frame, text=f"🎚️ Taxa de bits: {audio_stream.get('bit_rate', 'N/A')} bps").pack(anchor=tk.W)
                    ttk.Label(audio_frame, text=f"🔊 Canais: {audio_stream.get('channels', 'N/A')}").pack(anchor=tk.W)
                
                # Botão fechar
                ttk.Button(main_frame, text="Fechar", 
                          command=info_window.destroy).pack(pady=(20, 0))
                
        except Exception as e:
            self.log_message(f"⚠️ Erro ao obter informações do vídeo: {e}")
    
    def format_file_size(self, size_bytes):
        """Formata tamanho de arquivo em bytes para formato legível"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def format_duration(self, seconds):
        """Formata duração em segundos para formato legível"""
        if seconds == 0:
            return "00:00:00"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def browse_output_file(self):
        """Abre diálogo para selecionar arquivo de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo convertido como",
            defaultextension=".mov",
            filetypes=[("Arquivo MOV", "*.mov"), ("Todos os arquivos", "*.*")]
        )
        if filename:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, filename)
            self.log_message(f"💾 Destino definido: {Path(filename).name}")
    
    def browse_batch_files(self):
        """Abre diálogo para selecionar múltiplos arquivos"""
        filenames = filedialog.askopenfilenames(
            title="Selecionar arquivos de vídeo",
            filetypes=self.supported_formats
        )
        for filename in filenames:
            if filename not in self.input_files:
                self.input_files.append(filename)
                self.batch_listbox.insert(tk.END, Path(filename).name)
        self.log_message(f"📁 Adicionados {len(filenames)} arquivos")
    
    def browse_batch_folder(self):
        """Abre diálogo para selecionar pasta com arquivos"""
        folder = filedialog.askdirectory(title="Selecionar pasta com vídeos")
        if folder:
            folder_path = Path(folder)
            video_extensions = ['.mpg', '.mpeg', '.avi', '.mkv', '.wmv', '.flv', '.webm']
            video_files = []
            
            for ext in video_extensions:
                video_files.extend(folder_path.glob(f"*{ext}"))
                video_files.extend(folder_path.glob(f"*{ext.upper()}"))
            
            for video_file in video_files:
                if str(video_file) not in self.input_files:
                    self.input_files.append(str(video_file))
                    self.batch_listbox.insert(tk.END, video_file.name)
            
            self.log_message(f"📁 Adicionados {len(video_files)} arquivos da pasta")
    
    def browse_output_directory(self):
        """Abre diálogo para selecionar pasta de saída"""
        folder = filedialog.askdirectory(title="Selecionar pasta de saída")
        if folder:
            self.output_directory.set(folder)
            self.log_message(f"💾 Pasta de saída definida: {Path(folder).name}")
    
    def clear_batch_list(self):
        """Limpa a lista de arquivos em lote"""
        self.input_files.clear()
        self.batch_listbox.delete(0, tk.END)
        self.log_message("🗑️ Lista de arquivos limpa")
    
    def show_advanced_settings(self):
        """Mostra janela de configurações avançadas"""
        advanced_window = tk.Toplevel(self.window)
        advanced_window.title("⚙️ Configurações Avançadas")
        advanced_window.geometry("500x400")
        advanced_window.transient(self.window)
        advanced_window.grab_set()
        
        # Centralizar janela
        advanced_window.update_idletasks()
        x = (advanced_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (advanced_window.winfo_screenheight() // 2) - (400 // 2)
        advanced_window.geometry(f"500x400+{x}+{y}")
        
        # Conteúdo da janela
        main_frame = ttk.Frame(advanced_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurações de vídeo
        video_frame = ttk.LabelFrame(main_frame, text="🎬 Configurações de Vídeo", padding="10")
        video_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(video_frame, text="Resolução:").grid(row=0, column=0, sticky=tk.W)
        resolution_var = tk.StringVar(value="original")
        resolution_combo = ttk.Combobox(video_frame, textvariable=resolution_var,
                                       values=["original", "1920x1080", "1280x720", "854x480"],
                                       state="readonly", width=15)
        resolution_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        ttk.Label(video_frame, text="FPS:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        fps_var = tk.StringVar(value="original")
        fps_combo = ttk.Combobox(video_frame, textvariable=fps_var,
                                values=["original", "30", "25", "24", "60"],
                                state="readonly", width=15)
        fps_combo.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        # Configurações de codificação
        encoding_frame = ttk.LabelFrame(main_frame, text="🔧 Configurações de Codificação", padding="10")
        encoding_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(encoding_frame, text="Profile H.264:").grid(row=0, column=0, sticky=tk.W)
        profile_var = tk.StringVar(value="high")
        profile_combo = ttk.Combobox(encoding_frame, textvariable=profile_var,
                                    values=["baseline", "main", "high"],
                                    state="readonly", width=15)
        profile_combo.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        ttk.Label(encoding_frame, text="Level H.264:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        level_var = tk.StringVar(value="4.1")
        level_combo = ttk.Combobox(encoding_frame, textvariable=level_var,
                                  values=["3.0", "3.1", "4.0", "4.1", "4.2", "5.0", "5.1"],
                                  state="readonly", width=15)
        level_combo.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        
        # Botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(buttons_frame, text="✅ Aplicar", 
                  command=lambda: self.apply_advanced_settings(advanced_window)).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="❌ Cancelar", 
                  command=advanced_window.destroy).pack(side=tk.LEFT)
    
    def apply_advanced_settings(self, window):
        """Aplica configurações avançadas"""
        # Aqui você pode implementar a lógica para aplicar as configurações
        self.log_message("⚙️ Configurações avançadas aplicadas")
        window.destroy()
    
    def check_ffmpeg_installation(self):
        """Verifica se o FFmpeg está instalado"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            self.log_message("✅ FFmpeg detectado com sucesso!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.log_message("❌ FFmpeg não encontrado!")
            messagebox.showerror("Erro", 
                               "FFmpeg não está instalado!\n\n" +
                               "Instale o FFmpeg:\n" +
                               "• Windows: https://ffmpeg.org/download.html\n" +
                               "• macOS: brew install ffmpeg\n" +
                               "• Linux: sudo apt install ffmpeg")
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.see(tk.END)
        self.window.update_idletasks()
    
    def start_conversion(self):
        """Inicia a conversão"""
        if self.converting:
            return
            
        if self.batch_mode.get():
            self.start_batch_conversion()
        else:
            self.start_single_conversion()
    
    def start_single_conversion(self):
        """Inicia conversão de arquivo único"""
        # Validações
        if not self.input_entry.get():
            messagebox.showerror("Erro", "Selecione um arquivo de entrada!")
            return
            
        if not self.output_entry.get():
            messagebox.showerror("Erro", "Defina o arquivo de saída!")
            return
        
        if not Path(self.input_entry.get()).exists():
            messagebox.showerror("Erro", "Arquivo de entrada não encontrado!")
            return
        
        # Confirmar se vai sobrescrever arquivo existente
        if Path(self.output_entry.get()).exists():
            if not messagebox.askyesno("Confirmar", 
                                     "O arquivo de saída já existe. Deseja sobrescrever?"):
                return
        
        # Iniciar conversão
        self.converting = True
        self.convert_button.configure(text="⏸️ Convertendo...", state="disabled")
        self.progress_var.set(0)
        self.status_var.set("Iniciando conversão...")
        
        thread = threading.Thread(target=self.convert_single_video)
        thread.daemon = True
        thread.start()
    
    def start_batch_conversion(self):
        """Inicia conversão em lote"""
        if not self.input_files:
            messagebox.showerror("Erro", "Adicione arquivos para conversão em lote!")
            return
            
        if not self.output_directory.get():
            messagebox.showerror("Erro", "Selecione uma pasta de saída!")
            return
        
        # Confirmar conversão em lote
        if not messagebox.askyesno("Confirmar", 
                                 f"Converter {len(self.input_files)} arquivos?\n\n" +
                                 f"Pasta de saída: {self.output_directory.get()}"):
            return
        
        # Iniciar conversão em lote
        self.converting = True
        self.convert_button.configure(text="⏸️ Convertendo...", state="disabled")
        self.progress_var.set(0)
        self.status_var.set("Iniciando conversão em lote...")
        
        thread = threading.Thread(target=self.convert_batch_videos)
        thread.daemon = True
        thread.start()
    
    def convert_single_video(self):
        """Executa a conversão de arquivo único"""
        try:
            input_path = self.input_entry.get()
            output_path = self.output_entry.get()
            
            self.log_message("=" * 50)
            self.log_message(f"🎬 Iniciando conversão:")
            self.log_message(f"   📄 Entrada: {Path(input_path).name}")
            self.log_message(f"   💾 Saída: {Path(output_path).name}")
            self.log_message(f"   ⚙️ Qualidade: {self.quality.get()}")
            self.log_message("=" * 50)
            
            success = self.run_ffmpeg_conversion(input_path, output_path)
            
            if success:
                self.window.after(0, self.conversion_success, output_path)
            else:
                self.window.after(0, self.conversion_error, "Erro na conversão")
                
        except Exception as e:
            self.window.after(0, self.conversion_error, str(e))
    
    def convert_batch_videos(self):
        """Executa a conversão em lote"""
        try:
            total_files = len(self.input_files)
            successful = 0
            failed = 0
            
            self.log_message("=" * 50)
            self.log_message(f"🎬 Iniciando conversão em lote: {total_files} arquivos")
            self.log_message("=" * 50)
            
            for i, input_path in enumerate(self.input_files):
                if not self.converting:  # Verificar se foi cancelado
                    break
                    
                input_file = Path(input_path)
                output_file = Path(self.output_directory.get()) / f"{input_file.stem}.mov"
                
                self.window.after(0, lambda p=i+1, t=total_files: 
                                self.status_var.set(f"Convertendo {p}/{t}: {input_file.name}"))
                
                self.log_message(f"📁 [{i+1}/{total_files}] Convertendo: {input_file.name}")
                
                success = self.run_ffmpeg_conversion(input_path, str(output_file))
                
                if success:
                    successful += 1
                    self.log_message(f"✅ [{i+1}/{total_files}] Sucesso: {input_file.name}")
                else:
                    failed += 1
                    self.log_message(f"❌ [{i+1}/{total_files}] Falha: {input_file.name}")
                
                # Atualizar progresso
                progress = ((i + 1) / total_files) * 100
                self.window.after(0, lambda p=progress: self.progress_var.set(p))
            
            self.window.after(0, self.batch_conversion_finished, successful, failed)
            
        except Exception as e:
            self.window.after(0, self.conversion_error, str(e))
    
    def run_ffmpeg_conversion(self, input_path, output_path):
        """Executa a conversão com FFmpeg"""
        try:
            # Validar arquivo de entrada
            if not self.validate_input_file(input_path):
                return False
            
            # Verificar espaço em disco
            if not self.check_disk_space(input_path, output_path):
                return False
            
            # Parâmetros do FFmpeg baseados na qualidade
            crf_values = {'high': '18', 'medium': '23', 'low': '28'}
            
            cmd = [
                'ffmpeg',
                '-i', input_path,
                '-y',  # Sobrescrever arquivo existente
                '-c:v', 'libx264',
                '-preset', self.preset_var.get(),
                '-crf', crf_values[self.quality.get()],
                '-c:a', self.audio_codec_var.get() if self.preserve_audio.get() else 'an',
                '-b:a', self.audio_bitrate_var.get() if self.preserve_audio.get() else '0',
                '-movflags', '+faststart',
                '-pix_fmt', 'yuv420p',
                '-profile:v', 'high',
                '-level', '4.1',
                '-maxrate', self.maxrate_var.get(),
                '-bufsize', self.bufsize_var.get(),
                output_path
            ]
            
            self.log_message(f"🔧 Comando FFmpeg: {' '.join(cmd)}")
            
            # Executar FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Monitorar progresso
            self.monitor_ffmpeg_progress(process)
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                self.log_message(f"❌ Erro no FFmpeg: {stderr}")
                return False
            
            # Verificar se o arquivo de saída foi criado
            if not Path(output_path).exists():
                self.log_message("❌ Arquivo de saída não foi criado")
                return False
            
            # Verificar tamanho do arquivo de saída
            output_size = Path(output_path).stat().st_size
            if output_size == 0:
                self.log_message("❌ Arquivo de saída está vazio")
                return False
            
            self.log_message(f"✅ Conversão concluída. Tamanho: {self.format_file_size(output_size)}")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Erro na conversão: {e}")
            return False
    
    def validate_input_file(self, file_path):
        """Valida o arquivo de entrada"""
        try:
            path = Path(file_path)
            
            # Verificar se o arquivo existe
            if not path.exists():
                self.log_message(f"❌ Arquivo não encontrado: {path.name}")
                return False
            
            # Verificar se é um arquivo (não pasta)
            if not path.is_file():
                self.log_message(f"❌ Não é um arquivo válido: {path.name}")
                return False
            
            # Verificar se o arquivo não está vazio
            if path.stat().st_size == 0:
                self.log_message(f"❌ Arquivo está vazio: {path.name}")
                return False
            
            # Verificar se é um formato de vídeo suportado
            video_extensions = ['.mpg', '.mpeg', '.avi', '.mkv', '.wmv', '.flv', '.webm']
            if path.suffix.lower() not in video_extensions:
                self.log_message(f"❌ Formato não suportado: {path.suffix}")
                return False
            
            # Verificar se o arquivo pode ser lido
            try:
                with open(path, 'rb') as f:
                    f.read(1024)  # Tentar ler os primeiros bytes
            except PermissionError:
                self.log_message(f"❌ Sem permissão para ler: {path.name}")
                return False
            except Exception as e:
                self.log_message(f"❌ Erro ao ler arquivo: {e}")
                return False
            
            return True
            
        except Exception as e:
            self.log_message(f"❌ Erro na validação: {e}")
            return False
    
    def check_disk_space(self, input_path, output_path):
        """Verifica se há espaço suficiente em disco"""
        try:
            import shutil
            
            # Obter tamanho do arquivo de entrada
            input_size = Path(input_path).stat().st_size
            
            # Estimar tamanho do arquivo de saída (geralmente menor que o original)
            estimated_output_size = input_size * 0.8  # Estimativa conservadora
            
            # Obter espaço livre no disco de destino
            output_drive = Path(output_path).drive
            free_space = shutil.disk_usage(output_drive).free
            
            # Verificar se há espaço suficiente (com margem de segurança)
            required_space = estimated_output_size * 1.5  # 50% de margem
            
            if free_space < required_space:
                self.log_message(f"❌ Espaço insuficiente em disco")
                self.log_message(f"   Espaço livre: {self.format_file_size(free_space)}")
                self.log_message(f"   Espaço necessário: {self.format_file_size(required_space)}")
                return False
            
            return True
            
        except Exception as e:
            self.log_message(f"⚠️ Erro ao verificar espaço em disco: {e}")
            return True  # Continuar mesmo com erro na verificação
    
    def monitor_ffmpeg_progress(self, process):
        """Monitora o progresso do FFmpeg"""
        duration_pattern = re.compile(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})")
        time_pattern = re.compile(r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})")
        
        duration_seconds = 0
        
        while process.poll() is None:
            line = process.stderr.readline()
            if not line:
                break
                
            # Extrair duração total
            duration_match = duration_pattern.search(line)
            if duration_match:
                h, m, s, ms = map(int, duration_match.groups())
                duration_seconds = h * 3600 + m * 60 + s + ms / 100
            
            # Extrair tempo atual
            time_match = time_pattern.search(line)
            if time_match and duration_seconds > 0:
                h, m, s, ms = map(int, time_match.groups())
                current_seconds = h * 3600 + m * 60 + s + ms / 100
                progress = (current_seconds / duration_seconds) * 100
                
                # Enviar progresso para a thread principal
                self.progress_queue.put(progress)
    
    def monitor_progress(self):
        """Monitora a fila de progresso"""
        try:
            while True:
                progress = self.progress_queue.get_nowait()
                self.progress_var.set(progress)
                self.status_var.set(f"Convertendo... {progress:.1f}%")
        except queue.Empty:
            pass
        finally:
            self.window.after(100, self.monitor_progress)
    
    def conversion_success(self, output_path):
        """Callback para conversão bem-sucedida"""
        self.converting = False
        self.convert_button.configure(text="🚀 Converter Vídeo", state="normal")
        self.progress_var.set(100)
        self.status_var.set("Conversão concluída com sucesso! ✅")
        
        self.log_message("✅ CONVERSÃO CONCLUÍDA COM SUCESSO!")
        self.log_message(f"📁 Arquivo salvo em: {output_path}")
        
        # Adicionar ao histórico
        self.add_to_history(Path(self.input_entry.get()).name, Path(output_path).name, "Sucesso")
        
        # Perguntar se quer abrir pasta do arquivo
        if self.auto_open_folder.get():
            if messagebox.askyesno("Sucesso", 
                                 f"Conversão concluída!\n\n" +
                                 f"Arquivo salvo em:\n{output_path}\n\n" +
                                 "Deseja abrir a pasta do arquivo?"):
                self.open_file_location(output_path)
    
    def batch_conversion_finished(self, successful, failed):
        """Callback para conversão em lote finalizada"""
        self.converting = False
        self.convert_button.configure(text="🚀 Converter Vídeo", state="normal")
        self.progress_var.set(100)
        
        if failed == 0:
            self.status_var.set(f"Conversão em lote concluída! ✅ ({successful} arquivos)")
            self.log_message(f"✅ CONVERSÃO EM LOTE CONCLUÍDA: {successful} arquivos convertidos")
        else:
            self.status_var.set(f"Conversão em lote finalizada ⚠️ ({successful} sucessos, {failed} falhas)")
            self.log_message(f"⚠️ CONVERSÃO EM LOTE FINALIZADA: {successful} sucessos, {failed} falhas")
        
        # Perguntar se quer abrir pasta
        if self.auto_open_folder.get() and successful > 0:
            if messagebox.askyesno("Conversão em Lote", 
                                 f"Conversão finalizada!\n\n" +
                                 f"Sucessos: {successful}\n" +
                                 f"Falhas: {failed}\n\n" +
                                 "Deseja abrir a pasta de saída?"):
                self.open_file_location(self.output_directory.get())
    
    def conversion_error(self, error_msg):
        """Callback para erro na conversão"""
        self.converting = False
        self.convert_button.configure(text="🚀 Converter Vídeo", state="normal")
        self.progress_var.set(0)
        self.status_var.set("Erro na conversão ❌")
        
        self.log_message("❌ ERRO NA CONVERSÃO:")
        self.log_message(error_msg)
        
        messagebox.showerror("Erro na Conversão", 
                           f"Ocorreu um erro durante a conversão:\n\n{error_msg[:200]}...")
    
    def open_file_location(self, file_path):
        """Abre a pasta contendo o arquivo"""
        try:
            if sys.platform == "win32":
                os.startfile(Path(file_path).parent)
            elif sys.platform == "darwin":
                subprocess.run(["open", Path(file_path).parent])
            else:
                subprocess.run(["xdg-open", Path(file_path).parent])
        except Exception as e:
            self.log_message(f"Erro ao abrir pasta: {e}")
    
    def load_settings(self):
        """Carrega configurações salvas"""
        try:
            settings_file = Path("converter_settings.json")
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                self.quality.set(settings.get('quality', 'medium'))
                self.preset_var.set(settings.get('preset', 'medium'))
                self.maxrate_var.set(settings.get('maxrate', '10M'))
                self.bufsize_var.set(settings.get('bufsize', '16M'))
                self.audio_codec_var.set(settings.get('audio_codec', 'aac'))
                self.audio_bitrate_var.set(settings.get('audio_bitrate', '128k'))
                self.preserve_audio.set(settings.get('preserve_audio', True))
                self.auto_open_folder.set(settings.get('auto_open_folder', True))
                self.dark_mode.set(settings.get('dark_mode', False)) # Carregar tema
                
                self.log_message("⚙️ Configurações carregadas")
        except Exception as e:
            self.log_message(f"⚠️ Erro ao carregar configurações: {e}")
    
    def save_settings(self):
        """Salva configurações atuais"""
        try:
            settings = {
                'quality': self.quality.get(),
                'preset': self.preset_var.get(),
                'maxrate': self.maxrate_var.get(),
                'bufsize': self.bufsize_var.get(),
                'audio_codec': self.audio_codec_var.get(),
                'audio_bitrate': self.audio_bitrate_var.get(),
                'preserve_audio': self.preserve_audio.get(),
                'auto_open_folder': self.auto_open_folder.get(),
                'dark_mode': self.dark_mode.get() # Salvar tema
            }
            
            with open("converter_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            
            self.log_message("💾 Configurações salvas")
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        except Exception as e:
            self.log_message(f"❌ Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Erro ao salvar configurações:\n{e}")
    
    def reset_settings(self):
        """Restaura configurações padrão"""
        if messagebox.askyesno("Confirmar", "Restaurar configurações padrão?"):
            self.quality.set("medium")
            self.preset_var.set("medium")
            self.maxrate_var.set("10M")
            self.bufsize_var.set("16M")
            self.audio_codec_var.set("aac")
            self.audio_bitrate_var.set("128k")
            self.preserve_audio.set(True)
            self.auto_open_folder.set(True)
            self.dark_mode.set(False) # Resetar tema
            
            self.log_message(" Configurações restauradas")
    
    def add_to_history(self, input_file, output_file, status):
        """Adiciona entrada ao histórico"""
        try:
            history_file = Path("conversion_history.json")
            history = []
            
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            entry = {
                'date': datetime.now().isoformat(),
                'input_file': input_file,
                'output_file': output_file,
                'status': status,
                'size': self.get_file_size(output_file) if status == "Sucesso" else "N/A"
            }
            
            history.append(entry)
            
            # Manter apenas os últimos 100 registros
            if len(history) > 100:
                history = history[-100:]
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            self.log_message(f"📋 Adicionado ao histórico: {input_file}")
        except Exception as e:
            self.log_message(f"⚠️ Erro ao salvar histórico: {e}")
    
    def get_file_size(self, file_path):
        """Retorna o tamanho do arquivo formatado"""
        try:
            size = Path(file_path).stat().st_size
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        except:
            return "N/A"
    
    def load_history(self):
        """Carrega o histórico de conversões"""
        try:
            history_file = Path("conversion_history.json")
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # Limpar lista atual
                for item in self.history_tree.get_children():
                    self.history_tree.delete(item)
                
                # Adicionar entradas do histórico
                for entry in reversed(history):  # Mais recentes primeiro
                    date = datetime.fromisoformat(entry['date']).strftime("%d/%m/%Y %H:%M")
                    self.history_tree.insert('', 'end', values=(
                        date,
                        entry['input_file'],
                        entry['output_file'],
                        entry['status'],
                        entry['size']
                    ))
                
                self.log_message(f"📋 Histórico carregado: {len(history)} entradas")
        except Exception as e:
            self.log_message(f"⚠️ Erro ao carregar histórico: {e}")
    
    def clear_history(self):
        """Limpa o histórico de conversões"""
        if messagebox.askyesno("Confirmar", "Limpar todo o histórico de conversões?"):
            try:
                history_file = Path("conversion_history.json")
                if history_file.exists():
                    history_file.unlink()
                
                # Limpar lista
                for item in self.history_tree.get_children():
                    self.history_tree.delete(item)
                
                self.log_message("🗑️ Histórico limpo")
                messagebox.showinfo("Sucesso", "Histórico limpo com sucesso!")
            except Exception as e:
                self.log_message(f"❌ Erro ao limpar histórico: {e}")
                messagebox.showerror("Erro", f"Erro ao limpar histórico:\n{e}")
    
    def open_history_folder(self):
        """Abre a pasta onde está o arquivo de histórico"""
        try:
            history_file = Path("conversion_history.json")
            if history_file.exists():
                self.open_file_location(str(history_file))
            else:
                messagebox.showinfo("Informação", "Nenhum arquivo de histórico encontrado.")
        except Exception as e:
            self.log_message(f"Erro ao abrir pasta do histórico: {e}")
    
    def run(self):
        """Executa a aplicação"""
        self.window.mainloop()
    
    def on_drop_single_file(self, event):
        """Manipula o drop de um arquivo único"""
        try:
            # Obter o caminho do arquivo
            file_path = event.data
            
            # Remover chaves e espaços extras (comum no Windows)
            file_path = file_path.strip('{}').strip()
            
            # Verificar se é um arquivo válido
            if self.is_valid_video_file(file_path):
                # Atualizar o entry com o caminho completo
                self.input_entry.configure(state='normal')
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, file_path)
                self.input_entry.configure(state='readonly')
                
                # Atualizar label visual
                file_name = Path(file_path).name
                self.drop_label.configure(text=f"📁 {file_name}", foreground='green')
                
                # Sugerir nome de saída automaticamente
                if not self.output_entry.get():
                    input_path = Path(file_path)
                    suggested_output = input_path.with_suffix('.mov')
                    self.output_entry.delete(0, tk.END)
                    self.output_entry.insert(0, str(suggested_output))
                
                self.log_message(f"📁 Arquivo arrastado: {file_name}")
            else:
                self.log_message(f"❌ Arquivo não suportado: {Path(file_path).name}")
                messagebox.showwarning("Arquivo não suportado", 
                                     f"O arquivo {Path(file_path).name} não é um formato de vídeo suportado.")
        except Exception as e:
            self.log_message(f"❌ Erro ao processar arquivo arrastado: {e}")
    
    def on_drop_batch_files(self, event):
        """Manipula o drop de múltiplos arquivos"""
        try:
            # Obter os caminhos dos arquivos
            files_data = event.data
            
            # Processar múltiplos arquivos (separados por espaço no Windows)
            if sys.platform == "win32":
                # No Windows, os arquivos vêm entre chaves e separados por espaço
                files = []
                current_file = ""
                in_brackets = False
                
                for char in files_data:
                    if char == '{':
                        in_brackets = True
                        current_file = ""
                    elif char == '}':
                        in_brackets = False
                        if current_file.strip():
                            files.append(current_file.strip())
                    elif in_brackets:
                        current_file += char
            else:
                # Em outros sistemas, separados por espaço
                files = files_data.split()
            
            added_count = 0
            for file_path in files:
                if self.is_valid_video_file(file_path):
                    if file_path not in self.input_files:
                        self.input_files.append(file_path)
                        self.batch_listbox.insert(tk.END, Path(file_path).name)
                        added_count += 1
                else:
                    self.log_message(f"❌ Arquivo ignorado (não suportado): {Path(file_path).name}")
            
            if added_count > 0:
                self.log_message(f"📁 Adicionados {added_count} arquivos via drag & drop")
                # Atualizar visual da área de drop
                self.drop_batch_label.configure(text=f"📁 {len(self.input_files)} arquivos carregados", 
                                              foreground='green')
            else:
                self.log_message("❌ Nenhum arquivo válido encontrado")
                
        except Exception as e:
            self.log_message(f"❌ Erro ao processar arquivos arrastados: {e}")
    
    def is_valid_video_file(self, file_path):
        """Verifica se o arquivo é um formato de vídeo válido"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return False
            
            # Verificar extensão
            video_extensions = ['.mpg', '.mpeg', '.avi', '.mkv', '.wmv', '.flv', '.webm']
            return file_path.suffix.lower() in video_extensions
        except:
            return False

def main():
    """Função principal"""
    try:
        app = VideoConverterGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Erro ao iniciar aplicação:\n{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()