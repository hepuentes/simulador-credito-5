import streamlit as st

# Datos para cada línea de crédito
LINEAS_DE_CREDITO = {
    "LoansiFlex": {
        "descripcion": "Créditos libre inversión para empleados, independientes, personas naturales y pensionados.",
        "monto_min": 1000000,
        "monto_max": 20000000,
        "plazo_min": 12,
        "plazo_max": 60,
        "tasa_mensual": 1.9715,  # Tasa mensual en %
        "tasa_anual_efectiva": 26.4,  # Tasa E.A. en %
        "aval_porcentaje": 0.10,  # 10% del capital prestado
        "costos_adicionales": 11800  # Suma de costos asociados
    },
    "LoansiMicroFlex": {
        "descripcion": "Crédito rotativo orientado a personas en sectores informales.",
        "monto_min": 50000,
        "monto_max": 300000,
        "plazo_min": 4,
        "plazo_max": 8,
        "tasa_mensual": 2.0718,  # Tasa mensual en %
        "tasa_anual_efectiva": 27.9,  # Tasa E.A. en %
        "aval_porcentaje": 0.12,  # 12% del capital prestado
        "costos_adicionales": 14800  # Suma de costos asociados
    }
}

# Título de la aplicación
st.title("Simulador de Crédito Loansi")

# Selección de línea de crédito
tipo_credito = st.selectbox("Selecciona la Línea de Crédito", options=LINEAS_DE_CREDITO.keys())
detalles = LINEAS_DE_CREDITO[tipo_credito]

# Mostrar descripción del crédito
st.write(f"**Descripción**: {detalles['descripcion']}")

# Selección del monto
monto = st.number_input("Monto Solicitado (COP):", min_value=detalles["monto_min"], max_value=detalles["monto_max"], step=50000)

# Selección de plazo
if tipo_credito == "LoansiFlex":
    plazo = st.slider("Plazo en Meses:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=12)
    frecuencia_pago = "Mensual"
else:
    plazo = st.slider("Plazo en Semanas:", min_value=detalles["plazo_min"], max_value=detalles["plazo_max"], step=1)
    frecuencia_pago = st.selectbox("Frecuencia de Pago", ["Semanal", "Quincenal"])

# Cálculo del aval
aval = monto * detalles["aval_porcentaje"]

# Cálculo de la cuota
if tipo_credito == "LoansiFlex":
    # Calcular la cuota mensual usando la fórmula de amortización
    cuota = (monto + aval) * (detalles["tasa_mensual"] / 100) / (1 - (1 + detalles["tasa_mensual"] / 100) ** -plazo)
else:
    # Conversión de tasa mensual a semanal o quincenal
    tasa_semanal = (1 + detalles["tasa_mensual"] / 100) ** (1/4) - 1 if frecuencia_pago == "Semanal" else (1 + detalles["tasa_mensual"] / 100) ** (1/2) - 1
    cuota = (monto + aval) * tasa_semanal / (1 - (1 + tasa_semanal) ** -plazo)

# Mostrar resultados
st.write("### Resultado de Simulación")
st.write(f"**Monto Solicitado**: COP {monto:,.0f}")
st.write(f"**Tasa de Interés Mensual**: {detalles['tasa_mensual']}%")
st.write(f"**Interés Efectivo Anual (E.A.)**: {detalles['tasa_anual_efectiva']}%")
st.write(f"**Frecuencia de Pago**: {frecuencia_pago}")
st.write(f"**Cuota Estimada**: COP {cuota:,.0f}")

# Detalle adicional en sección desplegable
with st.expander("Ver Detalles del Crédito"):
    total_interes = cuota * plazo - monto
    total_pagar = cuota * plazo + detalles["costos_adicionales"]
    st.write(f"**Número de Cuotas**: {plazo}")
    st.write(f"**Porcentaje del Aval**: {detalles['aval_porcentaje'] * 100}%")
    st.write(f"**Costo del Aval**: COP {aval:,.0f}")
    st.write(f"**Total del Interés a Pagar**: COP {total_interes:,.0f}")
    st.write(f"**Costo del Aval y Otros**: COP {detalles['costos_adicionales']:,.0f}")
    st.write(f"**Total a Pagar**: COP {total_pagar:,.0f}")

# Botón para solicitar el crédito
st.write("---")
st.write("¿Interesado en solicitar este crédito?")
st.write("Para más información, comuníquese con nosotros por WhatsApp:")
st.write("[Hacer solicitud vía WhatsApp](https://wa.me/XXXXXXXXXXX)")
