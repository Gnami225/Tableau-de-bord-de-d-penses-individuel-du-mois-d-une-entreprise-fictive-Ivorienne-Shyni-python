from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
df = pd.read_excel(app_dir / "Classeur1v.xlsx", sheet_name="Classeur1")
df_depenses = pd.read_excel(app_dir / "Classeur1v.xlsx", sheet_name="Feuil1")
