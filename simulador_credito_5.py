import streamlit as st

# Datos para cada línea de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Créditos libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_muy_bajo": 1.7125,
        "tasa_moderado": 1.9715,
        "costos_adicionales": 11800,  # Suma de costos asociados
        "perfil": "Personas con ingreso mínimo de 1 SMLMV, score Datacrédito > 650."
    },
    "LoansiMicroFlex": {
        "descripcion": "Crédito rotativo para competir con el crédito gota a gota, orientado a personas en sectores informales.",
        "monto_min": 50000,
        "monto_max": 300000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_moderado": 2.0718,
        "costos_adicionales": 14800,  # Suma de costos asociados
        "perfil": "Personas en sector informal, sin estabilidad laboral formal."
    }
}

# Título de la aplicación
st.title("Simulador de Crédito Loansi")

# Selección de línea de crédito
tipo_credito = st.selectbox("Selecciona la Línea de Crédito", options=LINEAS_DE_CREDITO.keys())
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Mostrar descripción y perfil del crédito
st.write(f"**Descripción**: {detalles['descripcion']}")
st.write(f"**Perfil del Deudor**: {detalles['perfil']}")

# Selección del monto
monto = st.number_input("Monto Solicitado (COP):", min_value=detalles["monto_min"], max_value=detalles["monto_max"], step=50000)

# Selección de plazo
if tipo_credito == "LoansiFlex":
    plazo = st.slider("Plazo en Meses:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    riesgo = st.selectbox("Nivel de Riesgo", ["Muy bajo", "Moderado"])
    tasa_mensual = detalles["tasa_muy_bajo"] if riesgo == "Muy bajo" else detalles["tasa_moderado"]
    frecuencia_pago = "Mensual"
else:
    plazo = st.slider("Plazo en Semanas:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    tasa_mensual = detalles["tasa_moderado"]
    frecuencia_pago = st.selectbox("Frecuencia de Pago", ["Semanal", "Quincenal"])

# Cálculo de la cuota
if tipo_credito == "LoansiFlex":
    cuota = (monto * (tasa_mensual / 100)) / (1 - (1 + (tasa_mensual / 100)) ** -plazo)
else:
    # Conversión de tasa mensual a semanal o quincenal
    tasa_semanal = (1 + tasa_mensual / 100) ** (1/4) - 1 if frecuencia_pago == "Semanal" else (1 + tasa_mensual / 100) ** (1/2) - 1
    cuota = (monto * tasa_semanal) / (1 - (1 + tasa_semanal) ** -plazo)

# Mostrar resultados
st.write("### Resultado de Simulación")
st.write(f"**Monto Solicitado**: COP {monto:,.0f}")
st.write(f"**Tasa de Interés**: {tasa_mensual}% M.V.")
st.write(f"**Frecuencia de Pago**: {frecuencia_pago}")
st.write(f"**Cuota Estimada**: COP {cuota:,.0f}")

# Detalle adicional en sección desplegable
with st.expander("Ver Detalles del Crédito"):
    total_interes = cuota * plazo - monto
    total_pagar = cuota * plazo + detalles["costos_adicionales"]
    st.write(f"**Número de Cuotas**: {plazo}")
    st.write(f"**Total del Interés a Pagar**: COP {total_interes:,.0f}")
    st.write(f"**Costo del Aval y Otros**: COP {detalles['costos_adicionales']:,.0f}")
    st.write(f"**Total a Pagar**: COP {total_pagar:,.0f}")

# Botón para solicitar el crédito
st.write("---")
st.write("¿Interesado en solicitar este crédito?")
st.write("Para más información, comuníquese con nosotros por WhatsApp:")
st.write("[Hacer solicitud vía WhatsApp](https://wa.me/XXXXXXXXXXX)")
