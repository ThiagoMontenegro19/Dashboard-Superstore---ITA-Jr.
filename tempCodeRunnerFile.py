
    if regiao_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Region'] == regiao_sel]
        
    if categoria_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Category'] == catego