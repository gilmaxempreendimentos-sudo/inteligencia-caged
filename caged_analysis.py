import pandas as pd
import os
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

class AnaliseMercado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estado: str = Field(index=True)
    setor_economico: str = Field(index=True) # ---> NOVA COLUNA DE PESQUISA RÁPIDA
    cbo: str = Field(index=True)
    titulo_cbo: str
    amostra: int
    media_salarial: float
    dispersao_std: float
    junior_p25: float
    pleno_p50: float
    senior_p75: float
    master_p90: float
    data_geracao: datetime = Field(default_factory=datetime.utcnow)

def inicializar_banco():
    if os.path.exists(sqlite_file_name):
        try:
            os.remove(sqlite_file_name)
            print(f"--- Banco antigo removido para receber nova estrutura de Setores ---")
        except Exception as e:
            print(f"Aviso: Não consegui apagar o arquivo: {e}")
            
    SQLModel.metadata.create_all(engine)
    print("--- Novo banco de dados (com Setor Econômico) criado ---")

def salvar_analise_no_banco(df_final):
    inicializar_banco()
    df_final.columns = df_final.columns.str.strip()
    df_final = df_final.fillna(0)
    
    with Session(engine) as session:
        print(f"Processando e integrando {len(df_final)} registros...")
        
        for _, row in df_final.iterrows():
            novo_registro = AnaliseMercado(
                estado=str(row['Estado']),
                setor_economico=str(row['Setor_Economico']), # ---> MAPEANDO A NOVA COLUNA
                cbo=str(row['cbo2002ocupação']),
                titulo_cbo=str(row['Nome_da_Ocupação']),
                amostra=int(row['Amostra']),
                media_salarial=float(row['Média_Salarial']),
                dispersao_std=float(row['Dispersão_Std']),
                junior_p25=float(row['Junior_P25']),
                pleno_p50=float(row['Pleno_P50']),
                senior_p75=float(row['Senior_P75']),
                master_p90=float(row['Master_P90'])
            )
            session.add(novo_registro)
        
        session.commit()
    print(f"\n✅ SUCESSO ABSOLUTO! {len(df_final)} registros salvos com sucesso.")

def executar():
    try:
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_csv = os.path.join(diretorio_atual, "data", "analise_nacional_traduzida.csv")
        
        if os.path.exists(caminho_csv):
            print(f"Lendo: {caminho_csv}")
            df_para_salvar = pd.read_csv(caminho_csv, sep=';', decimal=',')
            salvar_analise_no_banco(df_para_salvar)
        else:
            print(f"❌ Erro: Arquivo não encontrado em {caminho_csv}")

    except Exception as e:
        print(f"❌ Erro técnico: {e}")

if __name__ == "__main__":
    executar()