"""
Script para eliminar la columna Base_dinero de la tabla venta
Ejecutar con: python eliminar_base_dinero.py
"""

import os
import django
import mysql.connector
from mysql.connector import Error

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AtleticQ.settings')
django.setup()

from django.conf import settings


def conectar_bd():
    """Conectar a la base de datos MySQL"""
    try:
        db_settings = settings.DATABASES['default']
        
        conexion = mysql.connector.connect(
            host=db_settings['HOST'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            database=db_settings['NAME'],
            port=db_settings.get('PORT', 3306)
        )
        
        if conexion.is_connected():
            print("✅ Conexión exitosa a la base de datos")
            return conexion
        
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None


def verificar_columna(conexion):
    """Verificar si la columna Base_dinero existe"""
    try:
        cursor = conexion.cursor()
        
        query = """
        SELECT COUNT(*) 
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'venta' 
        AND COLUMN_NAME = 'Base_dinero'
        """
        
        cursor.execute(query, (settings.DATABASES['default']['NAME'],))
        resultado = cursor.fetchone()
        
        existe = resultado[0] > 0
        
        if existe:
            print("📋 La columna 'Base_dinero' EXISTE en la tabla 'venta'")
        else:
            print("⚠️ La columna 'Base_dinero' NO EXISTE en la tabla 'venta'")
        
        cursor.close()
        return existe
        
    except Error as e:
        print(f"❌ Error al verificar columna: {e}")
        return False


def mostrar_estructura_tabla(conexion):
    """Mostrar estructura actual de la tabla venta"""
    try:
        cursor = conexion.cursor()
        
        query = "DESCRIBE venta"
        cursor.execute(query)
        
        print("\n" + "="*80)
        print("📊 ESTRUCTURA ACTUAL DE LA TABLA 'venta'")
        print("="*80)
        print(f"{'Campo':<25} {'Tipo':<20} {'Nulo':<8} {'Clave':<10} {'Default':<15}")
        print("-"*80)
        
        for row in cursor.fetchall():
            campo = row[0]
            tipo = row[1]
            nulo = row[2]
            clave = row[3] or ''
            default = str(row[4]) if row[4] is not None else 'NULL'
            
            print(f"{campo:<25} {tipo:<20} {nulo:<8} {clave:<10} {default:<15}")
        
        print("="*80 + "\n")
        
        cursor.close()
        
    except Error as e:
        print(f"❌ Error al mostrar estructura: {e}")


def contar_ventas_con_base(conexion):
    """Contar cuántas ventas tienen Base_dinero > 0"""
    try:
        cursor = conexion.cursor()
        
        query = "SELECT COUNT(*) FROM venta WHERE Base_dinero > 0"
        cursor.execute(query)
        
        resultado = cursor.fetchone()
        count = resultado[0]
        
        print(f"📊 Ventas con Base_dinero > 0: {count}")
        
        cursor.close()
        return count
        
    except Error as e:
        print(f"❌ Error al contar ventas: {e}")
        return 0


def mostrar_ventas_con_base(conexion):
    """Mostrar ventas que tienen Base_dinero registrada"""
    try:
        cursor = conexion.cursor()
        
        query = """
        SELECT Id_venta, id_usuario, DATE(Fecha) as fecha, Total, Base_dinero
        FROM venta 
        WHERE Base_dinero > 0
        ORDER BY Fecha DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        if resultados:
            print("\n" + "="*80)
            print("💰 ÚLTIMAS 10 VENTAS CON BASE DE DINERO")
            print("="*80)
            print(f"{'ID':<8} {'Usuario':<12} {'Fecha':<15} {'Total':<15} {'Base':<15}")
            print("-"*80)
            
            for row in resultados:
                id_venta = row[0]
                usuario = row[1]
                fecha = row[2]
                total = f"${row[3]:,.0f}"
                base = f"${row[4]:,.0f}"
                
                print(f"{id_venta:<8} {usuario:<12} {str(fecha):<15} {total:<15} {base:<15}")
            
            print("="*80 + "\n")
        else:
            print("✅ No hay ventas con Base_dinero > 0\n")
        
        cursor.close()
        
    except Error as e:
        print(f"❌ Error al mostrar ventas: {e}")


def eliminar_columna(conexion):
    """Eliminar la columna Base_dinero de la tabla venta"""
    try:
        cursor = conexion.cursor()
        
        print("\n⚠️ ¡ADVERTENCIA!")
        print("Estás a punto de ELIMINAR PERMANENTEMENTE la columna 'Base_dinero'")
        print("Esta operación NO se puede deshacer.\n")
        
        confirmacion = input("¿Deseas continuar? Escribe 'ELIMINAR' para confirmar: ").strip()
        
        if confirmacion != 'ELIMINAR':
            print("❌ Operación cancelada")
            return False
        
        print("\n🔄 Eliminando columna 'Base_dinero'...")
        
        query = "ALTER TABLE venta DROP COLUMN Base_dinero"
        cursor.execute(query)
        conexion.commit()
        
        print("✅ Columna 'Base_dinero' eliminada exitosamente\n")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"❌ Error al eliminar columna: {e}")
        conexion.rollback()
        return False


def crear_backup(conexion):
    """Crear backup de la tabla antes de eliminar la columna"""
    try:
        cursor = conexion.cursor()
        
        # Verificar si ya existe una tabla de backup
        query_check = """
        SELECT COUNT(*) 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'venta_backup'
        """
        
        cursor.execute(query_check, (settings.DATABASES['default']['NAME'],))
        existe_backup = cursor.fetchone()[0] > 0
        
        if existe_backup:
            print("⚠️ Ya existe una tabla 'venta_backup'")
            sobrescribir = input("¿Deseas sobrescribirla? (si/no): ").lower()
            
            if sobrescribir == 'si':
                cursor.execute("DROP TABLE venta_backup")
                print("🗑️ Backup anterior eliminado")
            else:
                print("❌ Operación de backup cancelada")
                cursor.close()
                return False
        
        print("🔄 Creando backup de la tabla 'venta'...")
        
        query_backup = "CREATE TABLE venta_backup AS SELECT * FROM venta"
        cursor.execute(query_backup)
        conexion.commit()
        
        # Contar registros en backup
        cursor.execute("SELECT COUNT(*) FROM venta_backup")
        count = cursor.fetchone()[0]
        
        print(f"✅ Backup creado exitosamente ({count} registros copiados)\n")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"❌ Error al crear backup: {e}")
        conexion.rollback()
        return False


def menu_principal():
    """Menú principal del script"""
    print("\n" + "="*80)
    print("🗑️ SCRIPT PARA ELIMINAR COLUMNA 'Base_dinero'")
    print("="*80)
    
    conexion = conectar_bd()
    
    if not conexion:
        print("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        while True:
            print("\n" + "-"*80)
            print("OPCIONES:")
            print("1. Verificar si existe la columna 'Base_dinero'")
            print("2. Mostrar estructura de la tabla 'venta'")
            print("3. Contar ventas con Base_dinero > 0")
            print("4. Mostrar ventas con Base_dinero registrada")
            print("5. Crear BACKUP de la tabla 'venta'")
            print("6. ELIMINAR columna 'Base_dinero' (¡PERMANENTE!)")
            print("0. Salir")
            print("-"*80)
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                verificar_columna(conexion)
            
            elif opcion == '2':
                mostrar_estructura_tabla(conexion)
            
            elif opcion == '3':
                if verificar_columna(conexion):
                    contar_ventas_con_base(conexion)
                else:
                    print("⚠️ La columna no existe, no se puede contar")
            
            elif opcion == '4':
                if verificar_columna(conexion):
                    mostrar_ventas_con_base(conexion)
                else:
                    print("⚠️ La columna no existe")
            
            elif opcion == '5':
                crear_backup(conexion)
            
            elif opcion == '6':
                if not verificar_columna(conexion):
                    print("⚠️ La columna 'Base_dinero' no existe")
                    continue
                
                print("\n🔒 RECOMENDACIÓN: Crea un backup antes de eliminar")
                crear_backup_antes = input("¿Deseas crear un backup ahora? (si/no): ").lower()
                
                if crear_backup_antes == 'si':
                    if not crear_backup(conexion):
                        print("❌ No se pudo crear el backup. Operación abortada.")
                        continue
                
                if eliminar_columna(conexion):
                    print("✅ Columna eliminada. Mostrando nueva estructura:")
                    mostrar_estructura_tabla(conexion)
            
            elif opcion == '0':
                print("\n👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida")
            
            input("\n[Presiona ENTER para continuar]")
    
    finally:
        if conexion.is_connected():
            conexion.close()
            print("\n🔌 Conexión cerrada")


if __name__ == '__main__':
    menu_principal()