import tkinter as tk
from tkinter import messagebox, ttk

# --- DATOS INICIALES ---
personal = ["Emiro", "Karla", "Sofia", "Misael"]
personal_SM = ["Roberto", "Ezequiel", "Liliana"]

p_personal = 2000000
p_personalSM = 5000000
pr_insumedical = 500000000
limite_presupuesto = 50000000

# --- LÓGICA DE PROCESAMIENTO ---
def procesar_pago():
    global pr_insumedical

    # 1. Verificar si el software está "Abierto"
    if combo_estado.get() != "Abierto":
        messagebox.showwarning("Sistema Cerrado", "El estado del software debe estar en 'Abierto' para procesar pagos.")
        return

    # 2. Verificar presupuesto disponible
    if pr_insumedical <= limite_presupuesto:
        lbl_resultado.config(
            text="[ALERTA] Presupuesto insuficiente para continuar con la nómina.",
            fg="#d9534f"
        )
        messagebox.showerror("Presupuesto Insuficiente", "El saldo de Insumedical ha alcanzado el límite mínimo.")
        btn_pagar.config(state="disabled")
        return

    nombre = entry_nombre.get().strip().capitalize()

    # 3. Validar entrada de texto
    if not nombre:
        messagebox.showwarning("Campo Vacío", "Por favor ingrese el nombre del empleado.")
        return

    # 4. Asignación y deducción del salario
    if nombre in personal:
        monto = p_personal
    elif nombre in personal_SM:
        monto = p_personalSM
    else:
        lbl_resultado.config(
            text="No pertenece a esta entidad o escribió mal su nombre.",
            fg="#d9534f"
        )
        return

    # Actualizar presupuesto y pantalla
    pr_insumedical -= monto
    lbl_saldo.config(text=f"${pr_insumedical:,.0f} COP")
    lbl_resultado.config(
        text=f"============ Hola {nombre}, gracias por tu servicio ============\n"
             f"> Tu pago total es de: ${monto:,.0f} COP\n"
             f"> Saldo restante en Insumedical: ${pr_insumedical:,.0f} COP",
        fg="#2e7d32"
    )

    # Limpiar campo de texto para la siguiente entrada
    entry_nombre.delete(0, tk.END)

# --- CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (TKINTER) ---
root = tk.Tk()
root.title("Sistema de Autocancelación de Salarios - INSUMEDICAL S.A")
root.geometry("520x450")
root.resizable(False, False)
root.config(bg="#f4f6f9")

# Título
lbl_titulo = tk.Label(
    root, 
    text="INSUMEDICAL S.A", 
    font=("Arial", 16, "bold"), 
    bg="#f4f6f9", 
    fg="#1a237e"
)
lbl_titulo.pack(pady=(15, 5))

lbl_subtitulo = tk.Label(
    root, 
    text="Control y Autocancelación de Nómina", 
    font=("Arial", 10), 
    bg="#f4f6f9", 
    fg="#555555"
)
lbl_subtitulo.pack(pady=(0, 15))

# Marco principal (Contenedor de controles)
frame_control = tk.LabelFrame(root, text=" Configuración ", font=("Arial", 10, "bold"), bg="#ffffff", padx=15, pady=15)
frame_control.pack(padx=20, pady=5, fill="x")

# Estado del Software
tk.Label(frame_control, text="Estado del Software:", bg="#ffffff", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
combo_estado = ttk.Combobox(frame_control, values=["Abierto", "Cerrado"], state="readonly", width=12)
combo_estado.current(0)
combo_estado.grid(row=0, column=1, padx=10, pady=5)

# Saldo actual de Insumedical
tk.Label(frame_control, text="Saldo Insumedical:", bg="#ffffff", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
lbl_saldo = tk.Label(frame_control, text=f"${pr_insumedical:,.0f} COP", font=("Arial", 10, "bold"), bg="#ffffff", fg="#2e7d32")
lbl_saldo.grid(row=1, column=1, sticky="w", padx=10, pady=5)

# Marco para la entrada del empleado
frame_empleado = tk.LabelFrame(root, text=" Registro de Pago ", font=("Arial", 10, "bold"), bg="#ffffff", padx=15, pady=15)
frame_empleado.pack(padx=20, pady=10, fill="x")

tk.Label(frame_empleado, text="Nombre del Empleado:", bg="#ffffff", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
entry_nombre = tk.Entry(frame_empleado, font=("Arial", 10), width=22)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)
entry_nombre.focus()

btn_pagar = tk.Button(
    frame_empleado, 
    text="Procesar Pago", 
    command=procesar_pago, 
    bg="#1a237e", 
    fg="white", 
    font=("Arial", 9, "bold"), 
    padx=10, 
    pady=2,
    relief="flat"
)
btn_pagar.grid(row=0, column=2, padx=10, pady=5)

# Áreas de mensajes de salida
lbl_resultado = tk.Label(
    root, 
    text="Ingrese un nombre para procesar el pago.", 
    font=("Arial", 9), 
    bg="#f4f6f9", 
    fg="#333333", 
    justify="center"
)
lbl_resultado.pack(pady=20)

root.mainloop()