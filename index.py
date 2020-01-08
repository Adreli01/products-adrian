from tkinter import ttk
from tkinter import *

import sqlite3

class Product:

    # Funcion para llamar a la base de datos en SQLite
    db_name = 'databaseadrian.db'

    def __init__(self, window):
        self.wind = window
        self.wind.title('Aplicacion de Productos')
        
        # Creando un Frame
        frame = LabelFrame(self.wind, text = 'Registrar un nuevo producto')
        frame.grid(row = 0, column = 0, columnspan = 2, pady = 20)

        # Name input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid (row = 1, column = 1)

        # Price input
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid (row = 2, column = 1)

        # Supplier input
        Label(frame, text = 'Proveedor: ').grid(row = 3, column = 0)
        self.supplier = Entry(frame)
        self.supplier.grid (row = 3, column = 1)

        # Button Add Product
        ttk.Button(frame, text = 'Guardar Producto', command = self.add_product).grid(row = 4, columnspan = 2, sticky = W + E)

        # Output Messages
        self.message = Label(text = '', fg = 'red')
        self.message.grid (row = 4, column = 0, columnspan = 2, sticky = W + E)


        # Table

        self.tree = ttk.Treeview(height = 15, columns = ('Precio', 'Proveedor'))
        # self.tree['columns']=('#0', '#1')  # Controla el numero de columnas
        self.tree.grid(row = 5, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)
        self.tree.heading('#2', text = 'Proveedor', anchor = CENTER)
                
        # Buttons
        ttk.Button (text = 'BORRAR', command = self.delete_product).grid(row = 6, column = 0, sticky = W + E)
        ttk.Button (text = 'EDITAR', command = self.edit_product).grid(row = 6, column = 1, sticky = W + E)


        # Filling the table rows
        self.get_products()

        # Definir funcion para mantener conectada la base de datos SQLite
    
    # Funcion para mantener conectado a la base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # cleaning Table (al conectarse si hay datos en la tabla los va a eliminar para proceder a obtener los nuevos datos)
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # quering data
        query = 'SELECT * FROM product ORDER BY nombre ASC' # nombre es el nombre del campo en la base de datos sqlite 
        db_rows = self.run_query(query)
            # print(db_rows)  -- el resultado es <sqlite3.Cursor object at 0x00CF1520>
        # filling data
        for row in db_rows: 
            # print (row)  # -- Imprime en pantalla el contenido de databaseadrian
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3]))
            

    def validation(self):
        return len(self.name.get()) !=0 and len(self.price.get()) !=0 and len(self.supplier.get()) !=0
            
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES (NULL, ?, ?, ?)'
            parameters = (self.name.get(), self.price.get(), self.supplier.get())
            self.run_query(query, parameters)
            self.message ['text'] = 'El Producto {} ha sido agregado satisfactoriamente'.format(self.name.get())
            self.name.delete(0, END) # El campo name vuelve a su estado inicial, es decir se limpia
            self.price.delete(0, END) # El campo price vuelve a su estado inicial, es decir se limpia
            self.supplier.delete(0, END) # El campo suppluer vuelve a su estado inicial, es decir se limpia
            # print ('Datos guardados')
            # print(self.name.get())
            # print(self.price.get())
            # print(self.supplier.get())
        else:
            self.message ['text'] = 'Nombre, Precio y Proveedor son requeridos'
            # print('Nombre y Precio son requeridos')
        self.get_products()

    def delete_product(self):
        # print(self.tree.item(self.tree.selection())) # Imprime la fila seleccionada
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecciona un registro'
            return
        self.message['text'] = ''
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE nombre = ?'
        self.run_query(query, (nombre, ))
        self.message['text'] = 'El registro {} ha sido borrado satisfactoriamente'.format(nombre)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Porfavor selecciona un registro'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        old_supplier = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind= Toplevel()
        self.edit_wind.title = 'Editar Producto'

        # Old Name
        Label(self.edit_wind, text = 'Nombre anterior: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'Nombre nuevo: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price
        Label(self.edit_wind, text = 'Precio anterior: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'Precio nuevo: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

         # Old Supplier
        Label(self.edit_wind, text = 'Proveedor anterior: ').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_supplier), state = 'readonly').grid(row = 4, column = 2)
        # New Supplier
        Label(self.edit_wind, text = 'Proveedor nuevo: ').grid(row = 5, column = 1)
        new_supplier = Entry(self.edit_wind)
        new_supplier.grid(row = 5, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records(new_name.get(), old_name, new_price.get(), old_price, new_supplier.get(), old_supplier)).grid(row = 6, column = 2, sticky = W)

    def edit_records(self, new_name, old_name, new_price, old_price, new_supplier, old_supplier):
        nombre = self.tree.item(self.tree.selection())['text']
        query = 'UPDATE product SET nombre = ?, precio = ?, proveedor = ? WHERE nombre = ? AND precio = ? AND proveedor = ?'
        parameters = (new_name, new_price, new_supplier, old_name, old_price, old_supplier)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Registro {} actualizado satisfactoriamente'.format(nombre)
        self.get_products()

        
         

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()