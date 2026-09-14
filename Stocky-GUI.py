#!/usr/bin/env python3

import sqlite3
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class StockyApp(QMainWindow):

  def __init__(self):
    super().__init__()
    self.version = "1.6.8"
    self.setWindowTitle(f"Stocky v{self.version} - Gestión de Inventario")
    self.resize(850, 600)

    # Conexión con la base de datos
    self.conexion = sqlite3.connect("stock.db")
    self.cursor = self.conexion.cursor()
    self.crear_tabla()

    # Configuración de la interfaz
    self.init_ui()
    self.cargar_inventario()

  def crear_tabla(self):
    self.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_USD REAL NOT NULL
        )
        """
    )
    self.conexion.commit()

  def init_ui(self):
    # Contenedor principal con pestañas
    self.tabs = QTabWidget()
    self.setCentralWidget(self.tabs)

    # Pestaña 1: Inventario
    self.tab_inventario = QWidget()
    self.tabs.addTab(self.tab_inventario, "📦 Inventario")
    self.configurar_tab_inventario()

    # Pestaña 2: Calculadoras
    self.tab_calculadoras = QWidget()
    self.tabs.addTab(self.tab_calculadoras, "💵 Calculadoras Financieras")
    self.configurar_tab_calculadoras()

  # --- PESTAÑA DE INVENTARIO ---
  def configurar_tab_inventario(self):
    layout_principal = QHBoxLayout()

    # Columna izquierda: Tabla de datos y Panel de Estadísticas
    layout_izquierdo = QVBoxLayout()

    self.tabla = QTableWidget()
    self.tabla.setColumnCount(4)
    self.tabla.setHorizontalHeaderLabels(
        ["ID", "Producto", "Cantidad", "Precio (USD)"]
    )
    self.tabla.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
    )
    self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    self.tabla.itemClicked.connect(self.cargar_datos_seleccionados)
    layout_izquierdo.addWidget(self.tabla)

    # Panel de Estadísticas
    grupo_stats = QGroupBox("Estadísticas del Inventario")
    layout_stats = QVBoxLayout()
    self.label_valor_total = QLabel("💵 Valor total en stock: $0.00")
    self.label_unidades_totales = QLabel("📦 Total de unidades: 0")
    self.label_precio_promedio = QLabel("🏷️ Precio promedio: $0.00")

    layout_stats.addWidget(self.label_valor_total)
    layout_stats.addWidget(self.label_unidades_totales)
    layout_stats.addWidget(self.label_precio_promedio)
    grupo_stats.setLayout(layout_stats)
    layout_izquierdo.addWidget(grupo_stats)

    # Columna derecha: Formulario de ingreso y botones
    layout_derecho = QVBoxLayout()
    grupo_formulario = QGroupBox("Gestión de Producto")
    layout_form = QFormLayout()

    self.input_id = QLineEdit()
    self.input_id.setReadOnly(True)
    self.input_id.setPlaceholderText("Autogenerado")

    self.input_nombre = QLineEdit()
    self.input_nombre.setPlaceholderText("Nombre del producto")

    self.input_cantidad = QSpinBox()
    self.input_cantidad.setRange(0, 1000000)

    self.input_precio = QDoubleSpinBox()
    self.input_precio.setRange(0.0, 1000000.0)
    self.input_precio.setDecimals(2)
    self.input_precio.setPrefix("$ ")

    layout_form.addRow("ID:", self.input_id)
    layout_form.addRow("Nombre:", self.input_nombre)
    layout_form.addRow("Cantidad:", self.input_cantidad)
    layout_form.addRow("Precio (USD):", self.input_precio)
    grupo_formulario.setLayout(layout_form)

    # Botones de Acción
    btn_agregar = QPushButton("➕ Agregar Producto")
    btn_agregar.clicked.connect(self.agregar_producto)

    btn_modificar = QPushButton("✏️ Modificar Seleccionado")
    btn_modificar.clicked.connect(self.modificar_producto)

    btn_eliminar = QPushButton("❌ Eliminar Seleccionado")
    btn_eliminar.clicked.connect(self.eliminar_producto)

    btn_limpiar = QPushButton("🧹 Limpiar Campos")
    btn_limpiar.clicked.connect(self.limpiar_formulario)

    layout_derecho.addWidget(grupo_formulario)
    layout_derecho.addWidget(btn_agregar)
    layout_derecho.addWidget(btn_modificar)
    layout_derecho.addWidget(btn_eliminar)
    layout_derecho.addWidget(btn_limpiar)
    layout_derecho.addStretch()

    layout_principal.addLayout(layout_izquierdo, 2)
    layout_principal.addLayout(layout_derecho, 1)
    self.tab_inventario.setLayout(layout_principal)

  # --- PESTAÑA DE CALCULADORAS ---
  def configurar_tab_calculadoras(self):
    layout_principal = QVBoxLayout()

    # Calculadora 1: Ingreso Neto
    grupo_neto = QGroupBox("Calculadora de Ingreso Neto")
    layout_neto = QFormLayout()

    self.calc_bruto = QDoubleSpinBox()
    self.calc_bruto.setRange(0, 100000000)
    self.calc_bruto.setPrefix("$ ")

    self.calc_egreso = QDoubleSpinBox()
    self.calc_egreso.setRange(0, 100000000)
    self.calc_egreso.setPrefix("$ ")

    self.label_resultado_neto = QLabel("💵 Ingreso NETO: $0.00")
    btn_calcular_neto = QPushButton("Calcular Ingreso Neto")
    btn_calcular_neto.clicked.connect(self.calcular_ingreso_neto)

    layout_neto.addRow("Ingreso BRUTO:", self.calc_bruto)
    layout_neto.addRow("Egreso:", self.calc_egreso)
    layout_neto.addRow(btn_calcular_neto)
    layout_neto.addRow(self.label_resultado_neto)
    grupo_neto.setLayout(layout_neto)

    # Calculadora 2: Ingreso Neto Mensual
    grupo_mensual = QGroupBox("Calculadora de Ingreso Neto Mensual")
    layout_mensual = QFormLayout()

    self.calc_mensual_ingreso = QDoubleSpinBox()
    self.calc_mensual_ingreso.setRange(0, 100000000)
    self.calc_mensual_ingreso.setPrefix("$ ")

    self.calc_mensual_egreso = QDoubleSpinBox()
    self.calc_mensual_egreso.setRange(0, 100000000)
    self.calc_mensual_egreso.setPrefix("$ ")

    self.calc_meses = QSpinBox()
    self.calc_meses.setRange(1, 120)
    self.calc_meses.setValue(1)

    self.label_resultado_mensual = QLabel("Resultado:")
    btn_calcular_mensual = QPushButton("Calcular Proyección Mensual")
    btn_calcular_mensual.clicked.connect(self.calcular_ingreso_mensual)

    layout_mensual.addRow(
        "Ingreso mensual estimado:", self.calc_mensual_ingreso
    )
    layout_mensual.addRow("Egreso mensual estimado:", self.calc_mensual_egreso)
    layout_mensual.addRow("Número de meses:", self.calc_meses)
    layout_mensual.addRow(btn_calcular_mensual)
    layout_mensual.addRow(self.label_resultado_mensual)
    grupo_mensual.setLayout(layout_mensual)

    layout_principal.addWidget(grupo_neto)
    layout_principal.addWidget(grupo_mensual)
    layout_principal.addStretch()
    self.tab_calculadoras.setLayout(layout_principal)

  # --- LÓGICA DE BASE DE DATOS Y EVENTOS ---
  def cargar_inventario(self):
    self.cursor.execute("SELECT * FROM stock")
    productos = self.cursor.fetchall()

    self.tabla.setRowCount(0)
    for fila_idx, (id_prod, nombre, cantidad, precio) in enumerate(productos):
      self.tabla.insertRow(fila_idx)
      self.tabla.setItem(fila_idx, 0, QTableWidgetItem(str(id_prod)))
      self.tabla.setItem(fila_idx, 1, QTableWidgetItem(nombre))
      self.tabla.setItem(fila_idx, 2, QTableWidgetItem(str(cantidad)))
      self.tabla.setItem(fila_idx, 3, QTableWidgetItem(f"${precio:.2f}"))

    self.actualizar_estadisticas()

  def actualizar_estadisticas(self):
    self.cursor.execute(
        "SELECT SUM(cantidad * precio_USD), SUM(cantidad), AVG(precio_USD)"
        " FROM stock"
    )
    total_valor, total_unidades, precio_promedio = self.cursor.fetchone()

    if total_valor is None:
      self.label_valor_total.setText("💵 Valor total en stock: $0.00")
      self.label_unidades_totales.setText("📦 Total de unidades: 0")
      self.label_precio_promedio.setText("🏷️ Precio promedio: $0.00")
    else:
      self.label_valor_total.setText(
          f"💵 Valor total en stock: ${total_valor:.2f}"
      )
      self.label_unidades_totales.setText(
          f"📦 Total de unidades: {int(total_unidades)}"
      )
      self.label_precio_promedio.setText(
          f"🏷️ Precio promedio: ${precio_promedio:.2f}"
      )

  def cargar_datos_seleccionados(self, item):
    fila = self.tabla.currentRow()
    self.input_id.setText(self.tabla.item(fila, 0).text())
    self.input_nombre.setText(self.tabla.item(fila, 1).text())
    self.input_cantidad.setValue(int(self.tabla.item(fila, 2).text()))

    precio_texto = self.tabla.item(fila, 3).text().replace("$", "")
    self.input_precio.setValue(float(precio_texto))

  def agregar_producto(self):
    nombre = self.input_nombre.text().strip()
    cantidad = self.input_cantidad.value()
    precio = self.input_precio.value()

    if not nombre:
      QMessageBox.warning(
          self, "Atención", "El nombre del producto no puede estar vacío."
      )
      return

    self.cursor.execute(
        "INSERT INTO stock (nombre, cantidad, precio_USD) VALUES (?, ?, ?)",
        (nombre, cantidad, precio),
    )
    self.conexion.commit()
    self.cargar_inventario()
    self.limpiar_formulario()

  def modificar_producto(self):
    id_prod = self.input_id.text()
    if not id_prod:
      QMessageBox.warning(
          self,
          "Atención",
          "Selecciona un producto de la tabla para modificarlo.",
      )
      return

    cantidad = self.input_cantidad.value()
    precio = self.input_precio.value()

    self.cursor.execute(
        "UPDATE stock SET cantidad = ?, precio_USD = ? WHERE id = ?",
        (cantidad, precio, int(id_prod)),
    )
    self.conexion.commit()
    self.cargar_inventario()
    self.limpiar_formulario()

  def eliminar_producto(self):
    id_prod = self.input_id.text()
    if not id_prod:
      QMessageBox.warning(
          self,
          "Atención",
          "Selecciona un producto de la tabla para eliminarlo.",
      )
      return

    confirmacion = QMessageBox.question(
        self,
        "Confirmar eliminación",
        f"¿Estás seguro de que deseas eliminar el producto con ID {id_prod}?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )

    if confirmacion == QMessageBox.StandardButton.Yes:
      self.cursor.execute("DELETE FROM stock WHERE id = ?", (int(id_prod),))
      self.conexion.commit()
      self.cargar_inventario()
      self.limpiar_formulario()

  def limpiar_formulario(self):
    self.input_id.clear()
    self.input_nombre.clear()
    self.input_cantidad.setValue(0)
    self.input_precio.setValue(0.0)

  # --- LÓGICA DE CALCULADORAS ---
  def calcular_ingreso_neto(self):
    bruto = self.calc_bruto.value()
    egreso = self.calc_egreso.value()
    neto = bruto - egreso
    self.label_resultado_neto.setText(f"💵 Ingreso NETO es de: ${neto:.2f}")

  def calcular_ingreso_mensual(self):
    ingreso_mensual = self.calc_mensual_ingreso.value()
    egreso_mensual = self.calc_mensual_egreso.value()
    meses = self.calc_meses.value()

    ganancia_mensual = ingreso_mensual - egreso_mensual
    total_acumulado = ganancia_mensual * meses

    self.label_resultado_mensual.setText(
        f"Ganancia neta por mes: ${ganancia_mensual:.2f}\n"
        f"Suma total acumulada en {meses} mes(es): ${total_acumulado:.2f}"
    )

  def closeEvent(self, event):
    self.conexion.close()
    event.accept()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  ventana = StockyApp()
  ventana.show()
  sys.exit(app.exec())