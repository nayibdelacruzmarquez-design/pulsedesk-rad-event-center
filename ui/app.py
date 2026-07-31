import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class PulseDeskApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PULSEDESK RAD · Centro de Control de Eventos")
        self.geometry("900x600")

        # Configuración de Grid Principal
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="⚡ PULSEDESK RAD — Control Center",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(side="left", padx=15, pady=10)

        self.status_badge = ctk.CTkLabel(
            self.header_frame,
            text="● SISTEMA ACTIVO",
            text_color="#2ecc71",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.status_badge.pack(side="right", padx=15, pady=10)

        # --- PANEL DE TELEMETRÍA (Izquierda) ---
        self.telemetry_frame = ctk.CTkFrame(self, corner_radius=10)
        self.telemetry_frame.grid(row=1, column=0, padx=(15, 7), pady=(0, 15), sticky="nsew")

        self.telemetry_title = ctk.CTkLabel(
            self.telemetry_frame,
            text="📊 Telemetría de Vehículos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.telemetry_title.pack(anchor="w", padx=15, pady=10)

        self.telemetry_text = ctk.CTkTextbox(self.telemetry_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.telemetry_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.telemetry_text.insert("1.0", "[16:45:00] VEH-01 | Vel: 85 km/h | Combustible: 72% | Temp: 90°C\n")

        # --- PANEL DE ALERTAS (Derecha) ---
        self.alerts_frame = ctk.CTkFrame(self, corner_radius=10)
        self.alerts_frame.grid(row=1, column=1, padx=(7, 15), pady=(0, 15), sticky="nsew")

        self.alerts_title = ctk.CTkLabel(
            self.alerts_frame,
            text="🚨 Cola de Alertas en Tiempo Real",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.alerts_title.pack(anchor="w", padx=15, pady=10)

        self.alerts_text = ctk.CTkTextbox(self.alerts_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.alerts_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.alerts_text.insert("1.0", "[16:45:01] [WARNING] Nivel de combustible bajo en VEH-04\n")

    def update_telemetry(self, data: str):
        """Método helper para agregar líneas al panel de telemetría."""
        self.telemetry_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {data}\n")
        self.telemetry_text.see("end")

    def update_alerts(self, alert: str):
        """Método helper para agregar líneas al panel de alertas."""
        self.alerts_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {alert}\n")
        self.alerts_text.see("end")


if __name__ == "__main__":
    app = PulseDeskApp()
    app.mainloop()