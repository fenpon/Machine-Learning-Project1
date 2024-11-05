import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우

def lookCount(lookdf, looks):
    """
    주어진 DataFrame의 특정 컬럼에 대한 값 분포를 시각화합니다.
    
    Parameters:
    lookdf : pd.DataFrame
        분석할 DataFrame
    looks : list
        분석할 컬럼의 이름 리스트
    """
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
    """
    주어진 DataFrame의 두 변수 간의 관계를 선 그래프로 나타냅니다.

    Parameters:
    lookdf : pd.DataFrame
        분석할 DataFrame
    x : str
        x축으로 사용할 컬럼 이름
    y : str
        y축으로 사용할 컬럼 이름
    """
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


