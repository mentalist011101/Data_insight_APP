import pandas as pd
import duckdb
from datetime import datetime
import re

class DataCleaner:
    def __init__(self, df):
        self.df = df.copy()
        self.conn = duckdb.connect()
        self.conn.register('df', self.df)
    
    def remove_duplicates(self):
        """Suppression des doublons via DuckDB"""
        return self.conn.execute("SELECT DISTINCT * FROM df").df()
    
    def fill_missing(self, strategy="mean"):
        """Remplissage des valeurs manquantes"""
        if strategy == "mean":
            return self.conn.execute("""
                SELECT 
                    * REPLACE (
                        COALESCE(column, AVG(column) OVER()) AS column
                    )
                FROM df
            """).df()
        return self.df.fillna("N/A")
    
    def execute_command(self, natural_cmd):
        """Traduction de commandes naturelles en actions"""
        cmd_map = {
            r"convertir\s+dates": self._convert_dates,
            r"supprimer\s+colonnes\s+(.+)": self._drop_columns,
            r"filtrer\s+(.+)": self._filter_data
        }
        
        for pattern, method in cmd_map.items():
            if match := re.search(pattern, natural_cmd, re.IGNORECASE):
                return method(*match.groups())
        
        return None
    
    def _convert_dates(self):
        """Conversion automatique des colonnes date"""
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                except:
                    continue
        return self.df