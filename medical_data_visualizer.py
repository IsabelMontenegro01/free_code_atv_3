# medical_data_visualizer.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 1. Importe os dados medical_examination.csv e atribua-os à variável df

df = pd.read_csv("medical_examination.csv")


# 2. Adicione uma coluna 'overweight' (IMC > 25 → 1, caso contrário 0)

df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2 > 25).astype(int)


# 3. Normalize cholesterol e gluc (1 = bom → 0, >1 = ruim → 1)

df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# 4. Desenhe o gráfico categórico na função draw_cat_plot

def draw_cat_plot():
    
    # 5. Crie DataFrame em formato "long" com pd.melt()
    
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    )

    
    # 6. Agrupe e reformate os dados para contar valores por cardio
    
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    
    # 7. Converta para long format → já está no formato adequado
    

    
    # 8. Crie o gráfico categórico com sns.catplot
    
    fig = sns.catplot(
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        data=df_cat,
        kind='bar'
    ).fig

    
    # 9. Retorne a figura
    
    return fig



# 10. Desenhe o mapa de calor na função draw_heat_map

def draw_heat_map():
    
    # 11. Limpe os dados aplicando os filtros especificados
    
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    
    # 12. Calcule a matriz de correlação
    
    corr = df_heat.corr()

    
    # 13. Gere uma máscara para o triângulo superior
    
    mask = np.triu(np.ones_like(corr, dtype=bool))

    
    # 14. Monte a figura matplotlib
    
    fig, ax = plt.subplots(figsize=(12, 8))

    
    # 15. Trace a matriz de correlação com sns.heatmap
    
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        center=0,
        vmax=0.3,
        vmin=-0.1,
        square=True,
        cbar_kws={"shrink": 0.5}
    )

    
    # 16. Retorne a figura
    
    return fig


if __name__ == "__main__":
    # Gera o gráfico categórico e salva
    fig1 = draw_cat_plot()
    fig1.savefig("catplot.png")
    print("✅ catplot.png gerado!")

    # Gera o mapa de calor e salva
    fig2 = draw_heat_map()
    fig2.savefig("heatmap.png")
    print("✅ heatmap.png gerado!")
