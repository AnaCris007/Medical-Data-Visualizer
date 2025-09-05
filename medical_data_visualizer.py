import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 - Importa o csv
df = pd.read_csv('medical_examination.csv')

# 2 - Cria a coluna overweigth
df['overweight'] = None
#2.1 - Eu não queria fazer calculando o BMI diretamente na 
# definição da coluna. Então, eu tentei a abordagem abaixo, mas não deu certo
""" # for row in df:
    # Multiplica por 0.01 pra converter a altura de cm para metros
    BMI = df['weight']/(df['height']*0.01)**2
    # If pra verificar se a pessoa está ou não acima do peso
    # Se o BMI for maior do que 25 ela está acima do peso
    if BMI > 25:
        df['overweight'] = 1
    else:
        # A pessoa não está overweight
        df['overweight'] = 0 """
# por isso eu resolvi pesquisar como eu poderia mudar o valor da coluna pra cada linha
# Eu olhei a documentação do Pandas e achei o método .apply() no site:
# https://pandas.pydata.org/docs/dev/reference/api/pandas.DataFrame.apply.html
# O .apply() te permite aplicar 
# uma função a cada valor de uma coluna ou de uma linha.
# Eu criei a função BMI pra calcular o BMI de cada pessoa
# A função recebe uma linha do dataframe
def BMI(row):
            # Essa anotação de if e else, é uma forma simplificada que ocupa menos espaço
            #Nesse caso se o BMI da pessoa for maior que 25
            # vai retornar 1 e se não for vai retornar 0
            # exatamente como o exercício pede
            return 1 if row['weight']/(row['height']*0.01)**2 > 25 else 0

# Aplica a função BMI a cada linha(axis = 1) do dataframe. Se eu quisesse
# que aplicasse a função a cada coluna era só usar axis = 0.
df['overweight'] = df.apply(BMI, axis= 1)

# 3
# Seguindo o mesmo padrão do que eu já tinha feito antes, eu criei uma função
# pro colesterol que recebe cada linha do dataframe e retorna um valor,
# dependendo se o valor se encaixa ou não em uma condição
def cholesterol(row):
    if row['cholesterol'] == 1:
        return 0
    elif row['cholesterol'] > 1:
        return 1

df['cholesterol'] = df.apply(cholesterol, axis = 1)

# Eu queria aprender ainda mais e por isso eu pesquisei por mais métodos que eu 
# poderia usar, além do apply e descobri na documentação do pandas o .astype(). No site:
# https://www.geeksforgeeks.org/python/python-pandas-dataframe-astype/
# When you use .astype you can pass the type you want the values in the 
# dataframe to have. In this specific case, we will filter for columns that have
# a gluc of more than 1. That will return a bollean series that we can apply 
# the .astype() to it. Then it will automatically convert the true values
# to 1 and the false values to 0.

df['gluc'] = (df['gluc'] > 1).astype(int)

# print(df) - It was only for testing
# 4
def draw_cat_plot():
    # 5 The exercise says to use pd.melt. I wasn't sure how to use it, so
    # I searched on the pandas documentation for it, and I found it in:
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.melt.html
    # O .melt() é usado pra transformar um dataframe. Ele basicamente tranforma colunas em linhas.
    # Assim, invés do seu dataframe ser muito largo, ele fica mais estreito e longo.
    # O resultado final depende do que vocÊ passa pros parâmetros da função. Para entender .melt()
    # Eu coloquei um print() antes e depois de aplicar essa função ao dataframe.
    # Nesse caso, eu quis que as colunas que fosse ser unpivot, ou seja, aquelas passadas
    # no argumento de value_vars fossem  cholesterol, gluc, smoke, alco, active, and overweight
    # porque foi o que o exercício pediu. Looking at the figure of examples in the repository
    # you can see that cardio is going to be the id, column. The one that identifies all the other rows.
    # Então, id_vars = cardio
    df_cat = pd.melt(df, id_vars = ['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    # 6 In this step I have to split the data using the cardio column. In order to do that
    # I searched for what I could use, and found the .group by method. In the site:
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html
    # This method allows me to split the dataframe based on one or more columns
    # In this case I will divided by the cardio column, the variable columns that are all the columns 
    # i previoulsy selected in value_vars and value that is 0 or 1 in this case. 
    # Depois eu uso o método .size() pra conseguir contar a ocorr^encia de cada valor.
    # Além disso eu uso o método .reset_index() porque no passo 6 eu tinha definido o index como
    # cardio e agora o eu coloquei que o index deve ser uma nova coluna chamada total. 
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name = 'total')
    # print(df_cat) # It was only for testing

    # 7 The data is already in the long format so what i have to do is plot the chart.
    # For it I used the sns.catplot() method as the exercise required.
    # To know exactly what parameters to choose I used the site:
    # https://seaborn.pydata.org/generated/seaborn.catplot.html#seaborn.catplot
    # In this site, I learned that to do a countplot I need to use 'count' as a
    # parameter for kind. I tried using count, but then I discovered that count doesn't accept a y argument.
    # It assingns it automatically. Because of that I changed the kind to bar, becuase the bar kind acepts the 
    # y-axis argumeny, and I was finally able to pass column total, that we created before,
    # as a parameter. As in the example, I defined that the x axis would be for the categoricql
    # variables we defined in pass 6 and the y axis would be for the total.
    # And i also defined that the hue would be value. The hue adds an additional variable to plot via color mapping. 
    #So the values 0 or 1, will have different colors in the plot to indicate
    # which one it is. As the docuementation says to create sub-plots as in the example
    # you need to assign a variable to col or row. In this case, I assigned cardio to 
    # the parameter col so I could obtain a result exactly as the one gaved in the example. 
    cat_plot = sns.catplot(data = df_cat, x = 'variable', y='total', hue = 'value', col = 'cardio', kind='bar')

    # 8 - I found in StackOberflow: https://stackoverflow.com/questions/32244753/how-to-save-a-seaborn-plot-into-a-file 
    # That i could use .fig to Get the figure, but when i tried usig the .fig
    # The VsCode sugested that is deprecated and that I should
    # use The .figure attribute 
    fig = cat_plot.figure


    # 9
    fig.savefig('catplot.png')
    return fig

# draw_cat_plot() # This was only for testing

# 10
def draw_heat_map():
    # 11 - To use multiples filters as the exercise requires
    # we can use the operator &. In this step we are cleaning 
    # all the incorrect data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & #filters for when the diastolic pressure is lower than the systolic
        ((df['height'] >= df['height'].quantile(0.025))) & #filters for when the height is greater than the 2.5th percentile
        (df['height'] <= df['height'].quantile(0.975)) & #filters for when height is equal or less than the 97.5th percentile
        (df['weight'] >= df['weight'].quantile(0.025)) & #filters for when weight is equal or more than the 2.5th percentile
        (df['weight'] <= df['weight'].quantile(0.975)) #filters for when the weight is less or equal to the 97.5th percentile
    ]

    # 12 - To create the correlation matrix i searched the internet and found this site:
    # https://www.geeksforgeeks.org/python/how-to-create-a-seaborn-correlation-heatmap-in-python/
    #There I learned that I only needed to use the .corr() method in the filtered dataframe.
    corr = df_heat.corr()

    # 13 - I had no idea to how to create this mask. Because of that I searched for 
    # a site that explained this and found: https://www.geeksforgeeks.org/data-visualization/plotting-only-the-upperlower-triangle-of-a-heatmap-in-matplotlib/
    # The example to create a upper mask was
    #mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    # The numpy method .triu returns is used to get a copy of a matrix with the elements below the k-th diagonal zeroed. 
    # It means you get the upper triangle. the .ones_like() method Return an array of ones with the same shape and type as a given array.
    # Finally we use the dtype = bool to crate a bollean mask that will be used to filter the dataframe.
    mask = np.triu(np.ones_like(corr, dtype=bool))
    # 
    # 14 - I didn't knew what to do here so I searched on Google for 'fig, ax = None' and
    # found a StackOverFlow discussion about it, in: https://stackoverflow.com/questions/34162443/why-do-many-examples-use-fig-ax-plt-subplots
    # There i discovered that I should use plt.subplots(), because it returns a tuple
    #containing the figure object and it's important if you want to save the figure later as 
    # we will here. ANd the ax is the axes object, which can be usefull to plot specific axes 
    # if you want to.
    fig, ax = plt.subplots()

    # 15 - To plot the map I searched in the seaborn documentation to see the parameters I would use.
    # I found it in the website: https://seaborn.pydata.org/generated/seaborn.heatmap.html
    # I passed the data as corr, because that was the correlation matrix we created. 
    # And I passed the mask as mask, because mask is the boolean array we created before
    # to filter the upper traingle and just show the lower one.
    # I tried creating the heatmap only with those 2 parameters, but they were 
    # failing on the test]

    # sns.heatmap(corr, mask = mask)

    # To discover what was worng I looked at the Figure_2 example and noticed that the values were 
    # written inside the heatmap, and with only one decimal place. The I hitted back to the documentation
    # and discovered that I should use the parameter annot=True to write the values on the heatmap.
    # and the parameter fmt=".1f", so I could format the decimal numbers, as strings with only
    # one decimal place as in the example.
    sns.heatmap(corr, mask = mask, annot=True, fmt='.1f')


    # 16
    fig.savefig('heatmap.png')
    return fig

# draw_heat_map() # This was only for testing