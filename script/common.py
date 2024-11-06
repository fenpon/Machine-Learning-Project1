import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우

def lookCount(lookdf, looks):
    num_cols = 3
    num_rows = (len(looks) + num_cols - 1) // num_cols  # 나누기 연산자 수정
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 5 * num_rows))
    axes = axes.flatten()  # Flatten the 2D array of axes to 1D

    for i, now in enumerate(looks):
        ax = axes[i]
        lookdf[now].value_counts().plot(kind='bar', ax=ax)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom')
        
        ax.set_title(f'{now} 값 분포')
        ax.set_xlabel('값')
        ax.set_ylabel('빈도')

    # Hide any remaining empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
        
    plt.show()

def lookLine(lookdf, x, y):
    plt.figure(figsize=(4, 2))
    plt.plot(lookdf[x], lookdf[y], marker='o', linestyle='-', color='b')
    for i, value in enumerate(lookdf[y]):
        plt.annotate(f'{value:.4f}', 
                     (lookdf[x].iloc[i], value), 
                     textcoords="offset points", 
                     xytext=(0, 5), 
                     ha='center')
    plt.title('시간에 따른 수준 변화')
    plt.xlabel('x : ' + x)
    plt.ylabel('y : ' + y)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.show()
def look3D(df, colPlot, texts, color_map,name):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.scatter(
        df[colPlot[0]] ,
        df[colPlot[1]],
        df["score"],
        c=color_map, marker='o'
    )
    
    if(len(texts) != 0):
        for idx, row in pd.concat(texts).iterrows():
            x_coord =  df[colPlot[0]]
            y_coord =  df[colPlot[1]]

            ax.text(
                x_coord,
                y_coord,
                row['score'],
                row[name],
                fontsize=8
            )

    
    ax.set_xlabel(colPlot[0] + " = x")
    ax.set_ylabel(colPlot[1] + " = y")
    ax.set_zlabel("score")
    ax.set_title('주석이 포함된 3D 산점도')

    plt.tight_layout()
    plt.show()
def look3ND(df, colPlot, texts, color_map,name):

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    middleIndex = int(len(colPlot) / 2)
    xtag = [colPlot[:middleIndex],colPlot[middleIndex:]]
   

    pca = PCA(n_components=1)
    xVals = []
    
    for i in range(2):
        xx = pca.fit_transform(df[xtag[i]])
        xVals.append(xx.flatten())
 

    ax.scatter(
        xVals[0] ,
        xVals[1],
        df["score"],
        c=color_map, marker='o'
    )
    
    if(len(texts) != 0):
        for idx, row in pd.concat(texts).iterrows():
            ax.text(
                xVals[0],
                xVals[1],
                row['score'],
                row[name],
                fontsize=8
            )

    col_0 = ' + '.join(map(str, colPlot[:middleIndex]))
    col_1 = ' + '.join(map(str, colPlot[middleIndex:]))
    ax.set_xlabel(col_0 + " = x")
    ax.set_ylabel(col_1 + " = y")
    ax.set_zlabel("score")
    ax.set_title('주석이 포함된 3D 산점도')

    plt.tight_layout()
    plt.show()

def lookOne(df,tag,color_map):
    # 진학률의 히스토그램 그리기
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(df)), df[tag], color=color_map, alpha=0.7)
    plt.title(f'{tag} 산포도')
    plt.xlabel('데이터 인덱스')
    plt.ylabel(tag)
    plt.grid(True)
    plt.show()
