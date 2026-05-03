import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import threading
import time
import json
import os
from pynput import keyboard
from pynput.keyboard import Controller, Key
import numpy as np
import cv2
import mss

CONFIG_FILE = "config.json"

# Diccionario de traducciones
TRANSLATIONS = {
    "es": {
        "title": "🎣 Bot de Pesca - v2.1",
        "main_title": "🎣 Bot de Pesca",
        "keys_title": "⌨️ TECLAS (clic para cambiar)",
        "cast": "LANZAR",
        "reel": "RECOGER",
        "toggle": "INICIAR",
        "region_title": "🎯 REGIÓN",
        "region_not_set": "● NO CONFIGURADA",
        "region_set": "● CONFIGURADA",
        "select_region": "📐 Seleccionar región",
        "region_not_configured": "Sin configurar",
        "color_title": "🎨 COLOR",
        "no_color": "Sin color",
        "palette": "🎨 Paleta",
        "screen": "👁️ Pantalla",
        "tolerance": "Tolerancia:",
        "slider_label": "Preciso ← → Amplio",
        "start_bot": "▶ INICIAR BOT",
        "stop_bot": "⏹  DETENER BOT",
        "stopped": "⏹ DETENIDO",
        "active": "▶ ACTIVO",
        "save": "💾 Guardar",
        "language": "� Idioma:",
        "key_capture_title": "Presiona una tecla",
        "key_capture_msg": "Presiona cualquier tecla...",
        "cancel": "Cancelar",
        "save_success_title": "Guardado",
        "save_success_msg": "Configuración guardada correctamente",
        "error_title": "Error",
        "region_first": "Primero selecciona una región de pantalla",
        "config_incomplete_title": "Configuración incompleta",
        "region_required": "Primero selecciona la región donde aparece el icono de pesca.",
        "color_required": "Selecciona el color del icono que indica cuando pica el pez.",
        "color_picker_title": "Selecciona el color del icono",
        "overlay_title": "Selecciona la región - Arrastra para dibujar",
        "overlay_instructions": "Arrastra para seleccionar la región del icono | ESC para cancelar",
        "colorpicker_title": "Selecciona el color - Mueve el mouse y haz clic",
        "colorpicker_instructions": "Mueve el mouse sobre el color del icono y haz clic | ESC para cancelar"
    },
    "en": {
        "title": "🎣 Fishing Bot - v2.1",
        "main_title": "🎣 Fishing Bot",
        "keys_title": "⌨️ KEYS (click to change)",
        "cast": "CAST",
        "reel": "REEL",
        "toggle": "TOGGLE",
        "region_title": "🎯 REGION",
        "region_not_set": "● NOT SET",
        "region_set": "● CONFIGURED",
        "select_region": "📐 Select region",
        "region_not_configured": "Not configured",
        "color_title": "🎨 COLOR",
        "no_color": "No color",
        "palette": "🎨 Palette",
        "screen": "👁️ Screen",
        "tolerance": "Tolerance:",
        "slider_label": "Precise ← → Wide",
        "start_bot": "▶ START BOT",
        "stop_bot": "⏹  STOP BOT",
        "stopped": "⏹ STOPPED",
        "active": "▶ ACTIVE",
        "save": "💾 Save",
        "language": "� Language:",
        "key_capture_title": "Press a key",
        "key_capture_msg": "Press any key...",
        "cancel": "Cancel",
        "save_success_title": "Saved",
        "save_success_msg": "Configuration saved successfully",
        "error_title": "Error",
        "region_first": "First select a screen region",
        "config_incomplete_title": "Incomplete Configuration",
        "region_required": "First select the region where the fishing icon appears.",
        "color_required": "Select the color of the icon that indicates when fish bites.",
        "color_picker_title": "Select the icon color",
        "overlay_title": "Select region - Drag to draw",
        "overlay_instructions": "Drag to select the icon region | ESC to cancel",
        "colorpicker_title": "Select color - Move mouse and click",
        "colorpicker_instructions": "Move mouse over the icon color and click | ESC to cancel"
    }
}

class FishingBot:
    def __init__(self, root):
        self.root = root
        # El título se establecerá después de cargar el idioma en apply_config_to_ui
        self.root.geometry("420x650")
        self.root.resizable(False, False)
        
        # Colores del tema
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'accent': '#0f3460',
            'highlight': '#e94560',
            'text': '#eaeaea',
            'text_dim': '#a0a0a0',
            'success': '#00d9ff',
            'warning': '#ffa500'
        }
        
        self.root.config(bg=self.colors['bg'])
        
        self.running = False
        self.bot_thread = None
        self.monitor_region = None
        self.target_color = None
        self.color_tolerance = 20
        
        self.keyboard_controller = Controller()
        
        self.cast_key = "1"
        self.reel_key = "2"
        self.toggle_key = "f9"
        self.language = "es"  # Idioma por defecto
        
        self.setup_styles()
        self.load_config()
        self.setup_ui()
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame de tarjeta
        style.configure('Card.TFrame', 
                      background=self.colors['card'],
                      relief='flat')
        
        # Labels
        style.configure('Title.TLabel',
                       background=self.colors['bg'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 20, 'bold'))
        
        style.configure('CardTitle.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['success'],
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Normal.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        
        style.configure('Dim.TLabel',
                       background=self.colors['card'],
                       foreground=self.colors['text_dim'],
                       font=('Segoe UI', 9))
        
        # Botones
        style.configure('Accent.TButton',
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        style.map('Accent.TButton',
                  background=[('active', self.colors['highlight'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['bg'],
                       font=('Segoe UI', 12, 'bold'),
                       padding=12)
        style.map('Success.TButton',
                  background=[('active', '#00b8d4')])
        
        style.configure('Stop.TButton',
                       background=self.colors['highlight'],
                       foreground=self.colors['text'],
                       font=('Segoe UI', 12, 'bold'),
                       padding=12)
        style.map('Stop.TButton',
                  background=[('active', '#d63050')])
        
        # Entries
        style.configure('Custom.TEntry',
                       fieldbackground=self.colors['accent'],
                       foreground=self.colors['text'],
                       insertcolor=self.colors['text'])
        
        # Spinbox
        style.configure('Custom.TSpinbox',
                       fieldbackground=self.colors['accent'],
                       foreground=self.colors['text'])
        
        # Combobox (selector de idioma)
        style.configure('TCombobox',
                       fieldbackground=self.colors['accent'],
                       background=self.colors['accent'],
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['text'])
        style.map('TCombobox',
                  fieldbackground=[('readonly', self.colors['accent'])],
                  selectbackground=[('readonly', self.colors['highlight'])])
    
    def setup_ui(self):
        # Frame principal simple
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Título
        self.title_label = tk.Label(main, text=self.t("main_title"), bg=self.colors['bg'], 
                fg=self.colors['text'], font=('Segoe UI', 20, 'bold'))
        self.title_label.pack()
        
        # === TECLAS ===
        keys_card = tk.Frame(main, bg=self.colors['card'], padx=10, pady=8)
        keys_card.pack(fill=tk.X, pady=5)
        
        self.keys_title_label = tk.Label(keys_card, text=self.t("keys_title"), bg=self.colors['card'],
                fg=self.colors['success'], font=('Segoe UI', 10, 'bold'))
        self.keys_title_label.pack(anchor=tk.W)
        
        keys_row = tk.Frame(keys_card, bg=self.colors['card'])
        keys_row.pack(fill=tk.X, pady=5)
        
        # Las 3 teclas como labels clickeables
        self.key_labels = {}
        key_configs = [
            (self.t("cast"), "cast_key", self.cast_key),
            (self.t("reel"), "reel_key", self.reel_key),
            (self.t("toggle"), "toggle_key", self.toggle_key)
        ]
        
        for i, (label_text, var_name, default) in enumerate(key_configs):
            # Frame para cada tecla
            kf = tk.Frame(keys_row, bg=self.colors['accent'], padx=5, pady=3)
            kf.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0 if i==0 else 3, 0))
            
            tk.Label(kf, text=label_text, bg=self.colors['accent'],
                    fg=self.colors['text_dim'], font=('Segoe UI', 7)).pack()
            
            lbl = tk.Label(kf, text=default.upper(), bg=self.colors['accent'],
                         fg=self.colors['text'], font=('Segoe UI', 11, 'bold'),
                         cursor='hand2')
            lbl.pack()
            lbl.bind("<Button-1>", lambda e, v=var_name: self.capture_key_simple(v))
            self.key_labels[var_name] = lbl
        
        # === REGIÓN ===
        region_card = tk.Frame(main, bg=self.colors['card'], padx=10, pady=8)
        region_card.pack(fill=tk.X, pady=5)
        
        top_row = tk.Frame(region_card, bg=self.colors['card'])
        top_row.pack(fill=tk.X)
        
        self.region_title_label = tk.Label(top_row, text=self.t("region_title"), bg=self.colors['card'],
                fg=self.colors['success'], font=('Segoe UI', 10, 'bold'))
        self.region_title_label.pack(side=tk.LEFT)
        
        self.region_status = tk.Label(top_row, text=self.t("region_not_set"), bg=self.colors['card'],
                                     fg=self.colors['highlight'], font=('Segoe UI', 9, 'bold'))
        self.region_status.pack(side=tk.RIGHT)
        
        self.select_region_btn = tk.Button(region_card, text=self.t("select_region"), command=self.select_region,
                 bg=self.colors['accent'], fg=self.colors['text'], font=('Segoe UI', 10, 'bold'),
                 relief=tk.FLAT, pady=6, cursor='hand2')
        self.select_region_btn.pack(fill=tk.X, pady=5)
        
        self.region_label = tk.Label(region_card, text=self.t("region_not_configured"), bg=self.colors['card'],
                                    fg=self.colors['text_dim'], font=('Segoe UI', 9))
        self.region_label.pack(anchor=tk.W)
        
        # === COLOR ===
        color_card = tk.Frame(main, bg=self.colors['card'], padx=10, pady=8)
        color_card.pack(fill=tk.X, pady=5)
        
        self.color_title_label = tk.Label(color_card, text=self.t("color_title"), bg=self.colors['card'],
                fg=self.colors['success'], font=('Segoe UI', 10, 'bold'))
        self.color_title_label.pack(anchor=tk.W)
        
        # Preview y botones
        color_row = tk.Frame(color_card, bg=self.colors['card'])
        color_row.pack(fill=tk.X, pady=5)
        
        # Preview
        self.color_frame = tk.Frame(color_row, width=50, height=40, bg="#333333",
                                   highlightbackground=self.colors['accent'], highlightthickness=2)
        self.color_frame.pack(side=tk.LEFT)
        self.color_frame.pack_propagate(False)
        
        self.color_info = tk.Label(color_row, text=self.t("no_color"), bg=self.colors['card'],
                                  fg=self.colors['text_dim'], font=('Segoe UI', 9))
        self.color_info.pack(side=tk.LEFT, padx=(10, 0))
        
        # Botones
        btn_row = tk.Frame(color_card, bg=self.colors['card'])
        btn_row.pack(fill=tk.X)
        
        self.palette_btn = tk.Button(btn_row, text=self.t("palette"), command=self.select_color,
                 bg=self.colors['accent'], fg=self.colors['text'], font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, pady=5, cursor='hand2')
        self.palette_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 3))
        
        self.screen_btn = tk.Button(btn_row, text=self.t("screen"), command=self.pick_color_from_screen,
                 bg=self.colors['accent'], fg=self.colors['text'], font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, pady=5, cursor='hand2')
        self.screen_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(3, 0))
        
        # Tolerancia simple
        tol_frame = tk.Frame(color_card, bg=self.colors['card'])
        tol_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.tolerance_label = tk.Label(tol_frame, text=self.t("tolerance"), bg=self.colors['card'],
                fg=self.colors['text'], font=('Segoe UI', 9))
        self.tolerance_label.pack(side=tk.LEFT)
        
        self.tol_label = tk.Label(tol_frame, text=str(self.color_tolerance), bg=self.colors['card'],
                                 fg=self.colors['success'], font=('Segoe UI', 10, 'bold'))
        self.tol_label.pack(side=tk.LEFT, padx=5)
        
        # Slider simple
        self.slider_canvas = tk.Canvas(color_card, bg=self.colors['card'], highlightthickness=0, 
                                      height=25, width=300)
        self.slider_canvas.pack(fill=tk.X, pady=3)
        self.slider_canvas.bind("<Button-1>", self.on_slider_click)
        self.slider_canvas.bind("<B1-Motion>", self.on_slider_drag)
        
        self.slider_label = tk.Label(color_card, text=self.t("slider_label"), bg=self.colors['card'],
                fg=self.colors['text_dim'], font=('Segoe UI', 8))
        self.slider_label.pack(anchor=tk.W)
        
        # === BOTÓN ===
        self.toggle_button = tk.Button(main, text=self.t("start_bot"), command=self.toggle_bot,
                                      bg=self.colors['success'], fg=self.colors['bg'],
                                      font=('Segoe UI', 16, 'bold'), relief=tk.FLAT,
                                      pady=12, cursor='hand2')
        self.toggle_button.pack(fill=tk.X, pady=10)
        
        # === IDIOMA Y GUARDAR ===
        status_frame = tk.Frame(main, bg=self.colors['bg'])
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Label de idioma (guardar referencia para actualizar)
        self.lang_label = tk.Label(status_frame, text=self.t("language"), bg=self.colors['bg'],
                fg=self.colors['text_dim'], font=('Segoe UI', 10, 'bold'))
        self.lang_label.pack(side=tk.LEFT)
        
        # Selector de idioma
        self.language_var = tk.StringVar(value=self.language)
        self.language_combo = ttk.Combobox(status_frame, textvariable=self.language_var,
                                          values=["es", "en"], width=8, state="readonly",
                                          font=('Segoe UI', 10, 'bold'))
        self.language_combo.pack(side=tk.LEFT, padx=(8, 0))
        self.language_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Botón guardar a la derecha
        self.save_btn = tk.Button(status_frame, text=self.t("save"), command=self.save_config,
                 bg=self.colors['accent'], fg=self.colors['text'], font=('Segoe UI', 9, 'bold'),
                 relief=tk.FLAT, cursor='hand2', padx=10)
        self.save_btn.pack(side=tk.RIGHT)
        
        # Dibujar slider inicial
        self.root.after(100, self.draw_tolerance_slider)
        self.apply_config_to_ui()
        # Establecer título con idioma cargado
        self.root.title(self.t("title"))
    
    def capture_key_simple(self, var_name):
        """Captura una tecla simple"""
        cap = tk.Toplevel(self.root)
        cap.title(self.t("key_capture_title"))
        cap.geometry("250x100")
        cap.attributes('-topmost', True)
        cap.resizable(False, False)
        cap.config(bg=self.colors['card'])
        cap.transient(self.root)
        cap.grab_set()
        
        # Centrar
        cap.geometry(f"+{self.root.winfo_x() + 275}+{self.root.winfo_y() + 250}")
        
        tk.Label(cap, text=self.t("key_capture_msg"), bg=self.colors['card'],
                fg=self.colors['text'], font=('Segoe UI', 12, 'bold')).pack(expand=True)
        
        def on_key(k):
            key_str = k.char.upper() if hasattr(k, 'char') and k.char else str(k).replace('Key.', '').upper()
            
            # Actualizar variable
            if var_name == 'cast_key':
                self.cast_key = key_str
            elif var_name == 'reel_key':
                self.reel_key = key_str
            elif var_name == 'toggle_key':
                self.toggle_key = key_str
            
            # Actualizar label
            if var_name in self.key_labels:
                self.key_labels[var_name].config(text=key_str)
            
            listener.stop()
            cap.destroy()
        
        from pynput import keyboard
        listener = keyboard.Listener(on_press=on_key)
        listener.start()
        
        tk.Button(cap, text=self.t("cancel"), command=lambda: [listener.stop(), cap.destroy()],
                 bg=self.colors['highlight'], fg=self.colors['text']).pack(pady=5)
    
    
    def select_region(self):
        OverlaySelector(self.root, self.on_region_selected, self)
    
    def on_region_selected(self, region):
        self.monitor_region = region
        self.region_status.config(text=self.t("region_set"), fg=self.colors['success'])
        self.region_label.config(
            text=f"{region['left']},{region['top']} | {region['width']}x{region['height']}px",
            fg=self.colors['text']
        )
    
    def pick_color_from_screen(self):
        ColorPicker(self.root, self.on_color_picked, self)
    
    def on_color_picked(self, color):
        self.target_color = color
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        self.color_frame.config(bg=hex_color)
        self.color_info.config(text=f"RGB: {color}", fg=self.colors['text'])
    
    def select_color(self):
        color = colorchooser.askcolor(title=self.t("color_picker_title"), 
                                      color=self.color_frame.cget('bg') if self.target_color else '#333333')
        if color[0]:
            self.target_color = tuple(int(c) for c in color[0])
            self.color_frame.config(bg=color[1])
            self.color_info.config(text=f"RGB: {self.target_color}", fg=self.colors['text'])
    
    def capture_color(self):
        if not self.monitor_region:
            messagebox.showwarning(self.t("error_title"), self.t("region_first"))
            return
        
        with mss.mss() as sct:
            screenshot = np.array(sct.grab(self.monitor_region))
            # Promedio del color en la región
            mean_color = np.mean(screenshot[:, :, :3], axis=(0, 1))
            self.target_color = tuple(int(c) for c in mean_color)
            hex_color = '#{:02x}{:02x}{:02x}'.format(*self.target_color)
            self.color_frame.config(bg=hex_color)
    
    
    def on_key_press(self, key):
        try:
            key_str = key.char if hasattr(key, 'char') and key.char else str(key).replace('Key.', '')
            if key_str.lower() == self.toggle_key.lower().replace('f', 'f'):
                self.toggle_bot()
        except:
            pass
    
    def toggle_bot(self):
        if self.running:
            self.stop_bot()
        else:
            # Solo iniciar si la configuración es válida
            if self.start_bot():
                self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
                self.bot_thread.start()
    
    def start_bot(self):
        # Verificar configuración
        if not self.monitor_region:
            messagebox.showwarning(self.t("config_incomplete_title"), 
                                 self.t("region_required"))
            return False
        if not self.target_color:
            messagebox.showwarning(self.t("config_incomplete_title"),
                                 self.t("color_required"))
            return False
        
        self.running = True
        self.toggle_button.config(text=self.t("stop_bot"), bg=self.colors['highlight'],
                                 activebackground='#d63050', command=self.stop_bot)
        return True
    
    def stop_bot(self):
        self.running = False
        self.toggle_button.config(text=self.t("start_bot"), bg=self.colors['success'],
                                 activebackground='#00b8d4', command=self.start_bot)
    
    def bot_loop(self):
        with mss.mss() as sct:
            while self.running:
                try:
                    # Lanzar sedal
                    self.press_key(self.cast_key)
                    time.sleep(0.5)  # Espera mínima para animación de lanzar
                    
                    # Esperar a que pique (detectar color)
                    fish_caught = False
                    start_time = time.time()
                    
                    while self.running and not fish_caught and time.time() - start_time < 15:
                        screenshot = np.array(sct.grab(self.monitor_region))
                        if self.detect_color(screenshot):
                            fish_caught = True
                            break
                        time.sleep(0.02)  # Verificar más frecuentemente
                    
                    if fish_caught:
                        self.press_key(self.reel_key)
                        time.sleep(0.5)  # Espera mínima para recoger
                    else:
                        # Recoger si no picó
                        self.press_key(self.reel_key)
                        time.sleep(0.3)
                    
                    time.sleep(0.2)  # Pausa mínima entre ciclos
                    
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(1)
    
    def detect_color(self, img):
        """Detección de color mejorada usando HSV"""
        try:
            # Convertir a RGB si es necesario
            if img.shape[2] == 4:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            else:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convertir color objetivo RGB a HSV
            target_bgr = np.uint8([[self.target_color[::-1]]])  # RGB a BGR para OpenCV
            target_hsv = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2HSV)[0][0]
            h, s, v = int(target_hsv[0]), int(target_hsv[1]), int(target_hsv[2])
            
            # Convertir imagen a HSV
            hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
            
            # Calcular tolerancias
            tol = self.color_tolerance
            h_tol = min(90, tol)  # Máximo 90 (la mitad del rango H)
            s_tol = min(255, tol * 2)  # Más amplio para saturación
            v_tol = min(255, tol * 2)  # Más amplio para valor
            
            # Calcular rangos con manejo especial para H (circular)
            h_lower = (h - h_tol) % 180
            h_upper = (h + h_tol) % 180
            s_lower = max(0, s - s_tol)
            s_upper = min(255, s + s_tol)
            v_lower = max(0, v - v_tol)
            v_upper = min(255, v + v_tol)
            
            # Crear máscara HSV
            if h_lower <= h_upper:
                # Rango normal
                lower = np.array([h_lower, s_lower, v_lower])
                upper = np.array([h_upper, s_upper, v_upper])
                mask = cv2.inRange(hsv, lower, upper)
            else:
                # Rango circular (cruza por 0/179, ej: rojo)
                lower1 = np.array([0, s_lower, v_lower])
                upper1 = np.array([h_upper, s_upper, v_upper])
                lower2 = np.array([h_lower, s_lower, v_lower])
                upper2 = np.array([179, s_upper, v_upper])
                mask1 = cv2.inRange(hsv, lower1, upper1)
                mask2 = cv2.inRange(hsv, lower2, upper2)
                mask = cv2.bitwise_or(mask1, mask2)
            
            # Contar píxeles que coinciden
            matching_pixels = cv2.countNonZero(mask)
            
            # Umbral: mínimo 5 píxeles o 2% del área
            total_pixels = mask.shape[0] * mask.shape[1]
            min_threshold = max(5, int(total_pixels * 0.02))
            
            detected = matching_pixels >= min_threshold
            
            if detected or matching_pixels > 0:
                percent = (matching_pixels / total_pixels) * 100
                print(f"Detección: {matching_pixels}px ({percent:.1f}%) HSV=({h},{s},{v}) tol={tol}")
            
            return detected
            
        except Exception as e:
            print(f"Error detección: {e}")
            return False
    
    def press_key(self, key):
        """Presiona una tecla usando SendInput de Windows (más confiable para juegos)"""
        try:
            # Intentar usar SendInput de Windows (mejor para juegos)
            if self.send_input_key(key):
                return
        except Exception as e:
            print(f"Error con SendInput, usando pynput: {e}")
        
        # Fallback a pynput
        try:
            # Convertir a minúscula
            key_lower = key.lower()
            
            if len(key) == 1:
                self.keyboard_controller.press(key_lower)
                self.keyboard_controller.release(key_lower)
            else:
                # Teclas especiales
                key_map = {
                    'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
                    'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
                    'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
                    'space': Key.space, 'enter': Key.enter, 'tab': Key.tab,
                    'shift': Key.shift, 'ctrl': Key.ctrl, 'alt': Key.alt
                }
                if key_lower in key_map:
                    self.keyboard_controller.press(key_map[key_lower])
                    self.keyboard_controller.release(key_map[key_lower])
            
            print(f"Tecla enviada (pynput): {key_lower}")
        except Exception as e:
            print(f"Error al presionar tecla: {e}")
    
    def send_input_key(self, key):
        """Usa SendInput de Windows para enviar teclas (funciona mejor en juegos)"""
        import ctypes
        from ctypes import wintypes
        
        # Convertir a minúscula (la mayoría de juegos esperan minúsculas)
        key = key.lower()
        
        # Constantes de Windows
        INPUT_KEYBOARD = 1
        KEYEVENTF_EXTENDEDKEY = 0x0001
        KEYEVENTF_KEYUP = 0x0002
        
        # Mapa de teclas a códigos virtuales (VK)
        vk_map = {
            '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35,
            '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, '0': 0x30,
            'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
            'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
            'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
            'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
            'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
            'z': 0x5A,
            'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73,
            'f5': 0x74, 'f6': 0x75, 'f7': 0x76, 'f8': 0x77,
            'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B,
            'space': 0x20, 'enter': 0x0D, 'tab': 0x09,
            'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
            'esc': 0x1B, 'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27
        }
        
        if key in vk_map:
            vk_code = vk_map[key]
        elif len(key) == 1:
            # Intentar como código ASCII
            vk_code = ord(key.upper())
        else:
            return False
        
        # Estructura INPUT
        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_void_p)
            ]
        
        class INPUT_I(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]
        
        class INPUT(ctypes.Structure):
            _fields_ = [
                ("type", wintypes.DWORD),
                ("_input", INPUT_I)
            ]
        
        user32 = ctypes.windll.user32
        
        # Enviar tecla presionada
        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp._input.ki.wVk = vk_code
        inp._input.ki.wScan = 0
        inp._input.ki.dwFlags = 0
        inp._input.ki.time = 0
        inp._input.ki.dwExtraInfo = 0
        
        result = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
        if result != 1:
            return False
        
        # Enviar tecla liberada inmediatamente
        inp._input.ki.dwFlags = KEYEVENTF_KEYUP
        result = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
        
        if result == 1:
            print(f"Tecla enviada (SendInput): {key}")
            time.sleep(0.01)  # Pausa mínima para que el juego registre
            return True
        return False
    
    def save_config(self):
        config = {
            "cast_key": self.cast_key,
            "reel_key": self.reel_key,
            "toggle_key": self.toggle_key,
            "region": self.monitor_region,
            "color": self.target_color,
            "tolerance": self.color_tolerance,
            "language": self.language
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        messagebox.showinfo(self.t("save_success_title"), self.t("save_success_msg"))
    
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                self.cast_key = config.get("cast_key", "1")
                self.reel_key = config.get("reel_key", "2")
                self.toggle_key = config.get("toggle_key", "f9")
                self.monitor_region = config.get("region")
                self.target_color = tuple(config.get("color")) if config.get("color") else None
                self.color_tolerance = config.get("tolerance", 20)
                self.language = config.get("language", "es")
            except:
                pass
    
    def t(self, key):
        """Obtener traducción para la clave dada en el idioma actual"""
        return TRANSLATIONS.get(self.language, TRANSLATIONS["es"]).get(key, key)
    
    def on_language_change(self, event=None):
        """Cambia el idioma y actualiza toda la UI"""
        self.language = self.language_var.get()
        
        # Actualizar título de ventana
        self.root.title(self.t("title"))
        self.title_label.config(text=self.t("main_title"))
        
        # Actualizar sección de teclas
        self.keys_title_label.config(text=self.t("keys_title"))
        key_labels = [self.t("cast"), self.t("reel"), self.t("toggle")]
        for i, var_name in enumerate(["cast_key", "reel_key", "toggle_key"]):
            # Obtener frame del label
            lbl = self.key_labels[var_name]
            parent = lbl.winfo_parent()
            key_frame = lbl.nametowidget(parent)
            # Actualizar label superior
            for child in key_frame.winfo_children():
                if isinstance(child, tk.Label) and child != lbl:
                    child.config(text=key_labels[i])
                    break
        
        # Actualizar sección de región
        self.region_title_label.config(text=self.t("region_title"))
        if self.monitor_region:
            self.region_status.config(text=self.t("region_set"))
        else:
            self.region_status.config(text=self.t("region_not_set"))
        self.select_region_btn.config(text=self.t("select_region"))
        if not self.monitor_region:
            self.region_label.config(text=self.t("region_not_configured"))
        
        # Actualizar sección de color
        self.color_title_label.config(text=self.t("color_title"))
        if not self.target_color:
            self.color_info.config(text=self.t("no_color"))
        self.palette_btn.config(text=self.t("palette"))
        self.screen_btn.config(text=self.t("screen"))
        self.tolerance_label.config(text=self.t("tolerance"))
        self.slider_label.config(text=self.t("slider_label"))
        
        # Actualizar botón principal
        if self.running:
            self.toggle_button.config(text=self.t("stop_bot"))
        else:
            self.toggle_button.config(text=self.t("start_bot"))
        
        # Actualizar botón guardar, selector y label de idioma
        self.save_btn.config(text=self.t("save"))
        self.lang_label.config(text=self.t("language"))
    
    def draw_tolerance_slider(self):
        """Dibuja el slider de tolerancia en el canvas"""
        try:
            canvas = self.slider_canvas
            canvas.delete("all")
            
            # Forzar update para obtener tamaño correcto
            canvas.update_idletasks()
            
            width = max(canvas.winfo_width(), 150)
            height = max(canvas.winfo_height(), 35)
            
            # Track (barra de fondo) - color más visible
            track_y = height // 2
            canvas.create_line(15, track_y, width - 15, track_y, 
                              fill='#0f3460', width=10, capstyle='round')
            
            # Calcular posición del thumb (5-100 range)
            min_val, max_val = 5, 100
            ratio = (self.color_tolerance - min_val) / (max_val - min_val)
            thumb_x = 15 + ratio * (width - 30)
            
            # Thumb (círculo deslizante) - más grande y visible
            canvas.create_oval(thumb_x - 12, track_y - 12, thumb_x + 12, track_y + 12,
                              fill='#00d9ff', outline='white', width=3)
            
            # Marca de ticks pequeñas
            for i in range(0, 11, 2):
                tick_x = 15 + (i / 10) * (width - 30)
                canvas.create_line(tick_x, track_y + 14, tick_x, track_y + 18, 
                                  fill='#a0a0a0', width=1)
        except:
            pass  # Si hay error, no crashear
    
    def update_slider_from_x(self, x):
        """Actualiza tolerancia desde posición X del mouse"""
        width = max(self.slider_canvas.winfo_width(), 100)
        
        # Calcular valor desde posición
        min_val, max_val = 5, 100
        ratio = max(0, min(1, (x - 10) / (width - 20)))
        self.color_tolerance = int(min_val + ratio * (max_val - min_val))
        
        # Actualizar UI
        self.tol_label.config(text=str(self.color_tolerance))
        self.draw_tolerance_slider()
    
    def on_slider_click(self, event):
        self.update_slider_from_x(event.x)
    
    def on_slider_drag(self, event):
        self.update_slider_from_x(event.x)
    
    def apply_config_to_ui(self):
        # Aplicar teclas (labels clickeables)
        for var_name, value in [('cast_key', self.cast_key), 
                                ('reel_key', self.reel_key), 
                                ('toggle_key', self.toggle_key)]:
            if var_name in self.key_labels:
                self.key_labels[var_name].config(text=value.upper())
        
        # Aplicar tolerancia
        self.tol_label.config(text=str(self.color_tolerance))
        self.root.after(100, self.draw_tolerance_slider)
        
        # Aplicar región
        if self.monitor_region:
            self.region_status.config(text=self.t("region_set"), fg=self.colors['success'])
            self.region_label.config(
                text=f"{self.monitor_region['left']},{self.monitor_region['top']} | "
                     f"{self.monitor_region['width']}x{self.monitor_region['height']}px",
                fg=self.colors['text']
            )
        else:
            self.region_label.config(text=self.t("region_not_configured"))
        
        # Aplicar color
        if self.target_color:
            hex_color = '#{:02x}{:02x}{:02x}'.format(*self.target_color)
            self.color_frame.config(bg=hex_color)
            self.color_info.config(text=f"RGB: {self.target_color}", fg=self.colors['text'])
    
    def on_closing(self):
        self.running = False
        self.keyboard_listener.stop()
        self.root.destroy()


class OverlaySelector:
    def __init__(self, parent, callback, bot=None):
        self.callback = callback
        self.bot = bot
        self.start_pos = None
        self.rect = None
        
        # Obtener traducciones si bot está disponible
        title = bot.t("overlay_title") if bot else "Selecciona la región - Arrastra para dibujar"
        instructions = bot.t("overlay_instructions") if bot else "Arrastra para seleccionar la región del icono | ESC para cancelar"
        
        self.overlay = tk.Toplevel(parent)
        self.overlay.title(title)
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-alpha', 0.3)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.config(bg='black')
        
        self.canvas = tk.Canvas(self.overlay, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.instructions = self.canvas.create_text(
            self.overlay.winfo_screenwidth() // 2,
            50,
            text=instructions,
            fill="white",
            font=("Arial", 14, "bold")
        )
        
        self.overlay.bind("<ButtonPress-1>", self.on_press)
        self.overlay.bind("<B1-Motion>", self.on_drag)
        self.overlay.bind("<ButtonRelease-1>", self.on_release)
        self.overlay.bind("<Escape>", lambda e: self.overlay.destroy())
        
        self.overlay.grab_set()
    
    def on_press(self, event):
        self.start_pos = (event.x_root, event.y_root)
        if self.rect:
            self.canvas.delete(self.rect)
    
    def on_drag(self, event):
        if self.start_pos:
            if self.rect:
                self.canvas.delete(self.rect)
            x1, y1 = self.start_pos
            x2, y2 = event.x_root, event.y_root
            self.rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline='red',
                width=3,
                fill='',
                stipple='gray50'
            )
            coords_text = f"X: {min(x1,x2)} Y: {min(y1,y2)} | {abs(x2-x1)}x{abs(y2-y1)}"
            self.canvas.itemconfig(self.instructions, text=coords_text)
    
    def on_release(self, event):
        if self.start_pos:
            x1, y1 = self.start_pos
            x2, y2 = event.x_root, event.y_root
            
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            if width > 10 and height > 10:
                region = {
                    "top": top,
                    "left": left,
                    "width": width,
                    "height": height
                }
                self.callback(region)
            
            self.overlay.destroy()


class ColorPicker:
    def __init__(self, parent, callback, bot=None):
        self.callback = callback
        self.bot = bot
        self.picking = True
        
        # Obtener traducciones si bot está disponible
        title = bot.t("colorpicker_title") if bot else "Modo Cuentagotas - Haz clic para capturar color"
        instructions = bot.t("colorpicker_instructions") if bot else "| CLICK para capturar | ESC para cancelar"
        
        # Ventana principal transparente que cubre toda la pantalla
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.attributes('-topmost', True)
        self.window.attributes('-alpha', 0.01)  # Casi invisible (1% opacidad)
        self.window.attributes('-fullscreen', True)
        self.window.config(bg='black')
        
        # Cursor de cruz para indicar modo picker
        self.window.config(cursor='crosshair')
        
        # Canvas transparente
        self.canvas = tk.Canvas(self.window, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Tooltip flotante que sigue al cursor
        self.tooltip = tk.Toplevel(self.window)
        self.tooltip.attributes('-topmost', True)
        self.tooltip.attributes('-alpha', 0.9)
        self.tooltip.overrideredirect(True)  # Sin bordes
        self.tooltip.config(bg='#1a1a2e')
        
        self.tooltip_frame = tk.Frame(self.tooltip, bg='#1a1a2e', padx=8, pady=5)
        self.tooltip_frame.pack()
        
        self.color_box = tk.Label(self.tooltip_frame, width=3, height=1, bg='gray')
        self.color_box.pack(side=tk.LEFT)
        
        self.rgb_label = tk.Label(self.tooltip_frame, text="RGB: ---", bg='#1a1a2e',
                                 fg='#eaeaea', font=('Segoe UI', 9, 'bold'))
        self.rgb_label.pack(side=tk.LEFT, padx=(5, 0))
        
        self.instruction_label = tk.Label(self.tooltip_frame, text=instructions,
                                         bg='#1a1a2e', fg='#a0a0a0', font=('Segoe UI', 9))
        self.instruction_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Posicionar tooltip en centro pantalla inicialmente
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        self.tooltip.geometry(f"+{screen_w//2 - 150}+{screen_h//2 + 50}")
        
        # Eventos
        self.window.bind("<Motion>", self.on_mouse_move)
        self.window.bind("<Button-1>", self.on_click)
        self.window.bind("<Escape>", self.on_cancel)
        
        self.window.grab_set()
        self.tooltip.grab_release()
    
    def get_pixel_color(self, x, y):
        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": 1, "height": 1}
            pixel = np.array(sct.grab(monitor))
            return (int(pixel[0, 0, 2]), int(pixel[0, 0, 1]), int(pixel[0, 0, 0]))
    
    def on_mouse_move(self, event):
        if self.picking:
            color = self.get_pixel_color(event.x_root, event.y_root)
            hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
            
            # Actualizar tooltip
            self.color_box.config(bg=hex_color)
            self.rgb_label.config(text=f"RGB: {color}")
            
            # Mover tooltip cerca del cursor pero sin taparlo
            tooltip_x = event.x_root + 20
            tooltip_y = event.y_root + 20
            
            # Evitar que salga de pantalla
            screen_w = self.window.winfo_screenwidth()
            screen_h = self.window.winfo_screenheight()
            if tooltip_x + 300 > screen_w:
                tooltip_x = event.x_root - 320
            if tooltip_y + 50 > screen_h:
                tooltip_y = event.y_root - 60
                
            self.tooltip.geometry(f"+{tooltip_x}+{tooltip_y}")
    
    def on_click(self, event):
        color = self.get_pixel_color(event.x_root, event.y_root)
        self.picking = False
        self.tooltip.destroy()
        self.callback(color)
        self.window.destroy()
    
    def on_cancel(self, event=None):
        self.picking = False
        self.tooltip.destroy()
        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FishingBot(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
