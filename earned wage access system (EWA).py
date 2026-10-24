import tkinter as tk
from tkinter import messagebox, ttk

# --- DATOS INICIALES ---
personal = {
    "Emiro": {"cargo": "Desarrollador Junior", "salario": 2000000},
    "Karla": {"cargo": "Analista de Datos", "salario": 2000000},
    "Sofia": {"cargo": "Soporte Técnico", "salario": 2000000},
    "Misael": {"cargo": "Control de Calidad", "salario": 2000000}
}

personal_SM = {
    "Roberto": {"cargo": "Gerente de Proyectos", "salario": 5000000},
    "Ezequiel": {"cargo": "Director de Finanzas", "salario": 5000000},
    "Liliana": {"cargo": "Jefe de Operaciones", "salario": 5000000}
}

pr_insumedical = 500000000
limite_presupuesto = 50000000
historial_pagos = []

# --- LÓGICA DE PROCESAMIENTO ---


def procesar_pago():
    global pr_insumedical

    # 1. Verificar si el software está "Abierto"
    if combo_estado.get() != "Abierto":
        messagebox.showwarning(
            "Sistema Cerrado", "El estado del software debe estar en 'Abierto' para procesar pagos.")
        return

    # 2. Verificar presupuesto disponible
    if pr_insumedical <= limite_presupuesto:
        lbl_resultado.config(
            text="[ALERTA] Presupuesto insuficiente para continuar con la nómina.",
            fg="#d9534f"
        )
        messagebox.showerror("Presupuesto Insuficiente",
                             "El saldo de Insumedical ha alcanzado el límite mínimo.")
        btn_pagar.config(state="disabled")
        return

    nombre = entry_nombre.get().strip().capitalize()

    # 3. Validar entrada de texto
    if not nombre:
        messagebox.showwarning(
            "Campo Vacío", "Por favor ingrese el nombre del empleado.")
        return

    # 4. Asignación, deducción y registro detallado
    if nombre in personal:
        info = personal[nombre]
        monto = info["salario"]
        cargo = info["cargo"]
    elif nombre in personal_SM:
        info = personal_SM[nombre]
        monto = info["salario"]
        cargo = info["cargo"]
    else:
        lbl_resultado.config(
            text=f"El colaborador '{nombre}' no pertenece a la entidad o el nombre es incorrecto.",
            fg="#d9534f"
        )
        return

    # Validar que el pago no exceda el saldo actual
    if pr_insumedical - monto < limite_presupuesto:
        messagebox.showerror(
            "Límite de Presupuesto", "Este pago dejaría a la empresa por debajo del límite mínimo permitido.")
        return

    # Actualizar presupuesto
    pr_insumedical -= monto

    # Registrar en el historial global
    historial_pagos.append((nombre, cargo, monto, pr_insumedical))

    # Actualizar interfaz
    lbl_saldo.config(text=f"${pr_insumedical:,.0f} COP")
    lbl_resultado.config(
        text=f"============ Pago Exitoso: {nombre} ============\n"
        f"> Cargo: {cargo}\n"
        f"> Pago Total: ${monto:,.0f} COP\n"
        f"> Saldo Restante Insumedical: ${pr_insumedical:,.0f} COP",
        fg="#2e7d32"
    )

    # Actualizar la tabla visual
    actualizar_tabla()

    # Limpiar campo de texto y enfocar
    entry_nombre.delete(0, tk.END)
    entry_nombre.focus()


def actualizar_tabla():
    # Limpiar elementos actuales del Treeview
    for item in tree_historial.get_children():
        tree_historial.delete(item)

    # Insertar los registros actualizados (orden inverso para ver los más recientes arriba)
    for pago in reversed(historial_pagos):
        tree_historial.insert("", "end", values=(
            pago[0], pago[1], f"${pago[2]:,.0f}", f"${pago[3]:,.0f}"))


def limpiar_historial():
    global pr_insumedical
    if messagebox.askyesno("Confirmar Reinicio", "¿Desea reiniciar el sistema y limpiar el historial de pagos?"):
        pr_insumedical = 500000000
        historial_pagos.clear()
        lbl_saldo.config(text=f"${pr_insumedical:,.0f} COP")
        lbl_resultado.config(
            text="Sistema reiniciado. Ingrese un nombre para procesar el pago.", fg="#333333")
        btn_pagar.config(state="normal")
        actualizar_tabla()


# --- CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (TKINTER) ---
root = tk.Tk()
root.title("Sistema de Autocancelación de Salarios - INSUMEDICAL S.A")
root.geometry("640x680")
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
lbl_titulo.pack(pady=(15, 2))

lbl_subtitulo = tk.Label(
    root,
    text="Control y Autocancelación de Nómina",
    font=("Arial", 10),
    bg="#f4f6f9",
    fg="#555555"
)
lbl_subtitulo.pack(pady=(0, 10))

# Marco principal (Configuración)
frame_control = tk.LabelFrame(root, text=" Configuración del Sistema ", font=(
    "Arial", 9, "bold"), bg="#ffffff", padx=12, pady=10)
frame_control.pack(padx=20, pady=5, fill="x")

tk.Label(frame_control, text="Estado del Software:", bg="#ffffff",
         font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=3)
combo_estado = ttk.Combobox(frame_control, values=[
                            "Abierto", "Cerrado"], state="readonly", width=12)
combo_estado.current(0)
combo_estado.grid(row=0, column=1, padx=10, pady=3, sticky="w")

tk.Label(frame_control, text="Saldo Insumedical:", bg="#ffffff",
         font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=3)
lbl_saldo = tk.Label(frame_control, text=f"${pr_insumedical:,.0f} COP", font=(
    "Arial", 10, "bold"), bg="#ffffff", fg="#2e7d32")
lbl_saldo.grid(row=1, column=1, sticky="w", padx=10, pady=3)

# Marco para la entrada del empleado
frame_empleado = tk.LabelFrame(root, text=" Registro de Pago ", font=(
    "Arial", 9, "bold"), bg="#ffffff", padx=12, pady=10)
frame_empleado.pack(padx=20, pady=8, fill="x")

tk.Label(frame_empleado, text="Nombre del Empleado:", bg="#ffffff",
         font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=3)
entry_nombre = tk.Entry(frame_empleado, font=("Arial", 10), width=18)
entry_nombre.grid(row=0, column=1, padx=8, pady=3)
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
btn_pagar.grid(row=0, column=2, padx=5, pady=3)

# Área de mensajes de salida rápida
lbl_resultado = tk.Label(
    root,
    text="Ingrese un nombre para procesar el pago.",
    font=("Arial", 9),
    bg="#f4f6f9",
    fg="#333333",
    justify="center"
)
lbl_resultado.pack(pady=8)

# Marco para el Historial de Pagos (Tabla con Treeview)
frame_historial = tk.LabelFrame(root, text=" Historial de Transacciones de Nómina ", font=(
    "Arial", 9, "bold"), bg="#ffffff", padx=10, pady=10)
frame_historial.pack(padx=20, pady=5, fill="both", expand=True)

# Configuración de la tabla (Treeview)
columnas = ("Empleado", "Cargo", "Monto", "Saldo Restante")
tree_historial = ttk.Treeview(
    frame_historial, columns=columnas, show="headings", height=5)

for col in columnas:
    tree_historial.heading(col, text=col)
    tree_historial.column(col, width=120, anchor="center")

tree_historial.pack(side="top", fill="both", expand=True, pady=(0, 8))

# Botón de reinicio
btn_reiniciar = tk.Button(
    frame_historial,
    text="Reiniciar Sistema",
    command=limpiar_historial,
    bg="#d9534f",
    fg="white",
    font=("Arial", 8, "bold"),
    padx=8,
    pady=2,
    relief="flat"
)
btn_reiniciar.pack(side="right")

root.mainloop()
