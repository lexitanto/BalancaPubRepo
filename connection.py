import time
import sqlite3

DB_PATH = "meubanco.db"

class database_connection():
    def __init__(self):
        self.conexao = None
        self.cursor = None

    def __enter__(self):
        self.connect_to_db()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def connect_to_db(self):
        while True:
            try:
                self.conexao = sqlite3.connect(DB_PATH)
                self.cursor = self.conexao.cursor()
                print("✅ Conexão com o banco estabelecida.")
                break
            except sqlite3.Error as e:
                print(f"❌ Erro ao conectar ao banco: {e}")
                print(f"🔄 Tentando novamente em 90 segundos...")
                time.sleep(90)

    def close_connection(self):
        self.conexao.close() 

    def get_cursor(self):        
        return self.cursor 
    
    def salvar_transmissoes(self, data):    
        try:                      
            self.cursor.execute("""
                INSERT INTO TB_UltimasTransmissoes (data)
                VALUES (?)
                """, (data,))
            self.commit()  # Confirma a operação
            print(f"⚠️ Última trasmissão '{data.decode('utf-8')}' salva no banco!")

        except sqlite3.Error as e:
            print(f"❌ Erro ao salvar localização: {e}")

    def fetch_data(self):
        try:
            self.cursor.execute("SELECT * FROM TB_UltimasTransmissoes")  # Pega todos os registros
            registros = self.cursor.fetchall()  # Retorna uma lista de tuplas        
            return registros
        
        except sqlite3.Error as e:
            print(f"❌ Erro ao buscar dados: {e}")
            return None
    
    def delete_at_index(self, id):
        try:
            self.cursor.execute("""
                DELETE FROM TB_UltimasTransmissoes 
                WHERE id = ? """, (id,))
            self.commit()
            print(f"⚠️ Indíce [{id}] deletado da tabela.")

        except sqlite3.Error as e:
            print(f"❌ Erro ao deletar na tabela: {e}")

    def commit(self):
	    self.conexao.commit()   
    
    

    

