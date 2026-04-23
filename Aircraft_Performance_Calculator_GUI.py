import tkinter as tk
from tkinter import ttk, messagebox
import math

class AircraftCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("✈️ Aircraft Performance Calculator")
        self.root.geometry("900x750")
        self.root.resizable(False, False)
        
        # Configure style
        self.setup_styles()
        
        # Create main container with scrollbar
        self.create_scrollable_frame()
        
        # Create input sections
        self.create_sections()
        
        # Calculate button
        self.create_calculate_button()
        
    def setup_styles(self):
        """Configure modern styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#f0f4f8"
        self.frame_bg = "#ffffff"
        self.accent_color = "#2563eb"
        self.text_color = "#1e293b"
        
        self.root.configure(bg=self.bg_color)
        
        # Style configurations
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground=self.accent_color,
                       background=self.frame_bg)
        
        style.configure('Section.TLabel',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.text_color,
                       background=self.frame_bg)
        
        style.configure('Field.TLabel',
                       font=('Segoe UI', 9),
                       foreground=self.text_color,
                       background=self.frame_bg)
        
        style.configure('Card.TFrame',
                       background=self.frame_bg,
                       relief='flat')
        
    def create_scrollable_frame(self):
        """Create a scrollable container for all inputs"""
        # Canvas and scrollbar
        canvas = tk.Canvas(self.root, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def create_sections(self):
        """Create organized input sections"""
        # Title
        title = ttk.Label(self.scrollable_frame, 
                         text="✈️ Aircraft Performance Calculator",
                         style='Title.TLabel')
        title.pack(pady=(10, 20))
        
        # Flight Performance Section
        self.flight_frame = self.create_section_frame("Flight Performance Parameters")
        self.entries_flight = self.create_input_fields(self.flight_frame, [
            ("Fuel Capacity", "gal", "100"),
            ("Fuel Consumption Rate", "gal/hr", "12"),
            ("True Air Speed", "knots", "150")
        ])
        
        # Weight & Balance Section
        self.weight_frame = self.create_section_frame("Weight & Balance")
        self.entries_weight = self.create_input_fields(self.weight_frame, [
            ("Payload Weight", "lb", "500"),
            ("Fuel Weight", "lb", "600"),
            ("Empty Weight", "lb", "2000"),
            ("Crew Weight", "lb", "340"),
            ("Moments (comma-separated)", "lb-ft", "1000,800,500")
        ])
        
        # Aerodynamic Properties Section
        self.aero_frame = self.create_section_frame("Aerodynamic Properties")
        self.entries_aero = self.create_input_fields(self.aero_frame, [
            ("Lift Coefficient (Cl)", "", "1.2"),
            ("Drag Coefficient (Cd)", "", "0.03"),
            ("Air Density", "kg/m³", "1.225"),
            ("Wing Area", "m²", "16"),
            ("Velocity", "m/s", "75")
        ])
        
        # Dynamics Section
        self.dynamics_frame = self.create_section_frame("Flight Dynamics")
        self.entries_dynamics = self.create_input_fields(self.dynamics_frame, [
            ("Aircraft Mass", "kg", "1500"),
            ("Thrust", "N", "5000"),
            ("Drag Force", "N", "800"),
            ("Initial Velocity", "m/s", "50"),
            ("Time Interval", "s", "10")
        ])
        
    def create_section_frame(self, title):
        """Create a styled frame for a section"""
        frame = ttk.Frame(self.scrollable_frame, style='Card.TFrame', padding=15)
        frame.pack(fill='x', padx=10, pady=10)
        
        # Section title
        title_label = ttk.Label(frame, text=title, style='Section.TLabel')
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x', pady=(0, 10))
        
        return frame
        
    def create_input_fields(self, parent, fields):
        """Create input fields with labels and units"""
        entries = {}
        
        for label_text, unit, default in fields:
            # Container for each field
            field_frame = ttk.Frame(parent, style='Card.TFrame')
            field_frame.pack(fill='x', pady=5)
            
            # Label
            label = ttk.Label(field_frame, 
                            text=f"{label_text}:",
                            style='Field.TLabel',
                            width=30)
            label.pack(side='left', padx=(0, 10))
            
            # Entry
            entry = ttk.Entry(field_frame, width=20, font=('Segoe UI', 9))
            entry.insert(0, default)
            entry.pack(side='left', padx=(0, 5))
            
            # Unit label
            if unit:
                unit_label = ttk.Label(field_frame, 
                                      text=unit,
                                      style='Field.TLabel',
                                      foreground='#64748b')
                unit_label.pack(side='left')
            
            entries[label_text] = entry
            
        return entries
        
    def create_calculate_button(self):
        """Create the calculate button"""
        button_frame = ttk.Frame(self.scrollable_frame, style='Card.TFrame')
        button_frame.pack(pady=20)
        
        calc_btn = tk.Button(button_frame,
                            text="Calculate Performance",
                            command=self.calculate,
                            bg=self.accent_color,
                            fg='white',
                            font=('Segoe UI', 11, 'bold'),
                            padx=40,
                            pady=12,
                            relief='flat',
                            cursor='hand2',
                            activebackground='#1d4ed8',
                            activeforeground='white')
        calc_btn.pack()
        
    def get_value(self, entry, name):
        """Safely get and validate numeric value from entry"""
        try:
            value = entry.get().strip()
            if not value:
                raise ValueError(f"{name} cannot be empty")
            return float(value)
        except ValueError as e:
            raise ValueError(f"Invalid input for {name}: {str(e)}")
            
    def get_list_value(self, entry, name):
        """Safely get and validate list of numeric values"""
        try:
            value = entry.get().strip()
            if not value:
                raise ValueError(f"{name} cannot be empty")
            return [float(x.strip()) for x in value.split(",")]
        except ValueError as e:
            raise ValueError(f"Invalid input for {name}: {str(e)}")
    
    def calculate(self):
        """Perform all calculations and display results"""
        try:
            # Get all input values with validation
            fuel_capacity = self.get_value(self.entries_flight["Fuel Capacity"], "Fuel Capacity")
            fuel_rate = self.get_value(self.entries_flight["Fuel Consumption Rate"], "Fuel Consumption Rate")
            true_air_speed = self.get_value(self.entries_flight["True Air Speed"], "True Air Speed")
            
            payload_wt = self.get_value(self.entries_weight["Payload Weight"], "Payload Weight")
            fuel_wt = self.get_value(self.entries_weight["Fuel Weight"], "Fuel Weight")
            empty_wt = self.get_value(self.entries_weight["Empty Weight"], "Empty Weight")
            crew_wt = self.get_value(self.entries_weight["Crew Weight"], "Crew Weight")
            moments = self.get_list_value(self.entries_weight["Moments (comma-separated)"], "Moments")
            
            cl = self.get_value(self.entries_aero["Lift Coefficient (Cl)"], "Lift Coefficient")
            cd = self.get_value(self.entries_aero["Drag Coefficient (Cd)"], "Drag Coefficient")
            rho = self.get_value(self.entries_aero["Air Density"], "Air Density")
            wing_area = self.get_value(self.entries_aero["Wing Area"], "Wing Area")
            velocity = self.get_value(self.entries_aero["Velocity"], "Velocity")
            
            mass = self.get_value(self.entries_dynamics["Aircraft Mass"], "Aircraft Mass")
            thrust = self.get_value(self.entries_dynamics["Thrust"], "Thrust")
            drag = self.get_value(self.entries_dynamics["Drag Force"], "Drag Force")
            initial_vel = self.get_value(self.entries_dynamics["Initial Velocity"], "Initial Velocity")
            time = self.get_value(self.entries_dynamics["Time Interval"], "Time Interval")
            
            # Validate positive values
            if fuel_rate <= 0:
                raise ValueError("Fuel consumption rate must be positive")
            if time < 0:
                raise ValueError("Time cannot be negative")
            
            # ========== CALCULATIONS ==========
            
            # Flight Performance
            aircraft_range = (fuel_capacity / fuel_rate) * true_air_speed
            endurance = fuel_capacity / fuel_rate
            
            # Weight & Balance
            total_weight = payload_wt + fuel_wt + empty_wt + crew_wt
            if total_weight <= 0:
                raise ValueError("Total weight must be positive")
            cg_position = sum(moments) / total_weight
            
            # Aerodynamic Forces
            lift = 0.5 * cl * rho * velocity**2 * wing_area
            drag_force = 0.5 * cd * rho * velocity**2 * wing_area
            weight = mass * 9.81
            
            # Flight Dynamics
            net_force = thrust - drag_force - weight
            acceleration = net_force / mass
            final_velocity = initial_vel + acceleration * time
            displacement = initial_vel * time + 0.5 * acceleration * time**2
            
            # L/D Ratio
            ld_ratio = lift / drag_force if drag_force > 0 else 0
            
            # Display Results
            self.display_results({
                'Range': (aircraft_range, 'nautical miles'),
                'Endurance': (endurance, 'hours'),
                'Total Weight': (total_weight, 'lb'),
                'CG Position': (cg_position, 'lb-ft/lb'),
                'Lift Force': (lift, 'N'),
                'Drag Force': (drag_force, 'N'),
                'Weight Force': (weight, 'N'),
                'L/D Ratio': (ld_ratio, ''),
                'Net Acceleration': (acceleration, 'm/s²'),
                'Final Velocity': (final_velocity, 'm/s'),
                'Displacement': (displacement, 'm')
            })
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Calculation Error", 
                               f"An unexpected error occurred:\n{str(e)}")
    
    def display_results(self, results):
        """Display calculation results in a formatted window"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Calculation Results")
        result_window.geometry("500x600")
        result_window.configure(bg=self.bg_color)
        result_window.resizable(False, False)
        
        # Title
        title = tk.Label(result_window,
                        text="✈️ Aircraft Performance Results",
                        font=('Segoe UI', 14, 'bold'),
                        bg=self.bg_color,
                        fg=self.accent_color)
        title.pack(pady=20)
        
        # Results frame with scrollbar
        canvas = tk.Canvas(result_window, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        results_frame = tk.Frame(canvas, bg=self.frame_bg, padx=20, pady=20)
        
        results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=results_frame, anchor="nw", width=450)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Display each result
        for i, (param, (value, unit)) in enumerate(results.items()):
            # Alternate row colors
            row_bg = '#f8fafc' if i % 2 == 0 else self.frame_bg
            
            row_frame = tk.Frame(results_frame, bg=row_bg, pady=10, padx=15)
            row_frame.pack(fill='x', pady=2)
            
            # Parameter name
            param_label = tk.Label(row_frame,
                                  text=f"{param}:",
                                  font=('Segoe UI', 10),
                                  bg=row_bg,
                                  fg=self.text_color,
                                  anchor='w',
                                  width=20)
            param_label.pack(side='left')
            
            # Value and unit
            value_text = f"{value:.4f} {unit}" if unit else f"{value:.4f}"
            value_label = tk.Label(row_frame,
                                  text=value_text,
                                  font=('Segoe UI', 11, 'bold'),
                                  bg=row_bg,
                                  fg=self.accent_color,
                                  anchor='e',
                                  width=25)
            value_label.pack(side='right')
        
        # Close button
        close_btn = tk.Button(result_window,
                             text="Close",
                             command=result_window.destroy,
                             bg=self.accent_color,
                             fg='white',
                             font=('Segoe UI', 10, 'bold'),
                             padx=30,
                             pady=8,
                             relief='flat',
                             cursor='hand2')
        close_btn.pack(pady=15)


# ================= Main Application =================
if __name__ == "__main__":
    root = tk.Tk()
    app = AircraftCalculator(root)
    root.mainloop()
