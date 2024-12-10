
# Challenge 3: Data Engineering con PySpark

Este proyecto es parte de un conjunto de retos semanales enfocados en mejorar habilidades de Data Engineering utilizando PySpark. En esta tercera semana, el objetivo es realizar diversas transformaciones y análisis sobre datos estructurados en formato CSV y JSON.

## 🚀 Objetivos del Proyecto

1. Leer y procesar datos desde archivos JSON y CSV.
2. Realizar conversiones de tipos de datos, como `timestamp`, `float` e `integer`.
3. Aplicar agregaciones y operaciones sobre los datos utilizando PySpark.

---

## 🛠️ Requisitos

- **Python** 3.8 o superior.
- **PySpark** 3.x.
- **VS Code** (opcional, para desarrollo).
- **Data Files**:  
  - `clientes_reducido.csv`
  - `transacciones_correcto.json`

---

## 📂 Estructura del Proyecto

```plaintext
├── resources/
│   ├── clientes_reducido.csv        # Datos de clientes
│   ├── transacciones_correcto.json  # Transacciones en formato JSON
├── main.py                          # Código principal del reto
├── README.md                        # Documentación del proyecto
├── libraries/
│   ├── util.py                      # Métodos utiles
│   ├── pyspark_env.py               # Lógica en version PySpark
│   ├── sparksql_env.py              # Lógica en version SparkSql
```

---

## 📦 Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/CrixusVolcanic/Challenge-3-PySpark.git
   cd Challenge-3-PySpark
   ```

2. **Instala las dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Verifica que PySpark esté instalado**:

   ```bash
   pyspark --version
   ```

---

## 🔧 Uso

1. Coloca los archivos `clientes_reducido.csv` y `transacciones_correcto.json` en la carpeta `resources/`.

2. Ejecuta el archivo principal:

   ```bash
   python main.py
   ```

3. **Salida esperada**:
   - Un esquema limpio de datos con los tipos convertidos.
   - Resultados de agrupaciones y transformaciones.

---

## ✨ Funciones Clave

### Lectura de Datos
```python
df = spark.read.format("json").load("resources/transacciones_correcto.json")
```

### Transformaciones de Datos
- Cambiar tipos de datos (`cast`).
- Convertir cadenas en formato de fecha a tipo `timestamp`.

```python
df = df.withColumn("amount", df["amount"].cast(FloatType())) \
       .withColumn("timestamp", to_timestamp(df["timestamp"]))
```

### Agregaciones
- Contar transacciones por moneda:
```python
df.groupBy("currency").count().show()
```

---

## 📝 Notas

- Asegúrate de que los archivos estén en formato esperado. 
  - El JSON debe estar en formato de líneas (`.jsonl`) para una correcta lectura.
- Si tienes problemas con los atajos de teclado en VS Code, revisa las configuraciones de tu terminal.

---

## 📚 Recursos Adicionales

- [Documentación oficial de PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Atajos de teclado de VS Code](https://code.visualstudio.com/shortcuts/keyboard-shortcuts-macos.pdf)

---

## 🧑‍💻 Autor

- **Davian Bermudez**  
  Data Engineer apasionada por aprender y crecer en el ecosistema de Big Data.

---

## 🎯 Próximos Pasos

- Mejorar la gestión de errores al leer datos.
- Añadir más análisis como funciones de ventana y joins avanzados.
