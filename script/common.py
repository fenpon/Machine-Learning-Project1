import matplotlib.pyplot as plt
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우

def lookCount(lookdf,looks):
    #int 몇개나오는지 그래프 그림
    num_cols = 3
    num_rows = (len(looks) + num_cols - 1) 
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10,5 * num_rows))
    axes = axes.flatten()  # Flatten the 2D array of axes to 1D

    for i,now in enumerate(looks):
        ax = axes[i]
        lookdf[now].value_counts().plot(kind='bar', ax=ax)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x()+ p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom')  # ha: horizontal alignment, va: vertical alignment
        
        ax.set_title('Value Distribution in Column A')
        ax.set_xlabel('Values')
        ax.set_ylabel('Counts')

    # Hide any remaining empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
        
    plt.show()

def lookLine(lookdf,x,y):
    #데이터 프레임 선그려줌
    plt.figure(figsize=(4, 2))
    plt.plot(lookdf[x], lookdf[y], marker='o', linestyle='-', color='b')  # Line plot with markers
    for i, value in enumerate(lookdf[y]):
        plt.annotate(f'{value:.4f}', 
                    (lookdf[x].iloc[i], value), 
                    textcoords="offset points",  # Position the text
                    xytext=(0,5),  # 5 points vertical offset
                    ha='center')
    plt.title('Levels Over Time')
    plt.xlabel('x : '+x)
    plt.ylabel('y : '+y)
    plt.xticks(rotation=45)  # Rotate x labels for better readability
    plt.grid()  # Add a grid for better visibility
    plt.tight_layout()  # Adjust layout to make room for labels
    plt.show()
