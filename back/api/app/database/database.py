import mysql.connector


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(user='root',
                                                  password='akemih32',
                                                  host='localhost',
                                                  database='mercadolivre',
                                                  auth_plugin='mysql_native_password')
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, parametros=None, retornar_insert_id=False):

        try:

            if parametros:
                self.cursor.execute(query, parametros)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith("INSERT") or query.strip().upper().startswith("UPDATE") or query.strip().upper().startswith("DELETE"):
                self.connection.commit()
            print(f'Query executada com sucesso: {query}\n')
            if retornar_insert_id:
                insert_id = self.cursor.lastrowid
                return insert_id
            else:
                results = self.cursor.fetchall()
                return results

        except mysql.connector.Error as err:
            print(f'Erro na consulta {query}: {err}')

        finally:
            self.cursor.close()

        def close_connection(self):
            self.cursor.close()
            self.connection.close()
