import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from shapely.geometry import Point
import os

# 한글 폰트 설정 (맑은 고딕)
rc('font', family='Malgun Gothic')

# GeoJSON URL
url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json"

# GeoJSON 데이터 불러오기
gdf = gpd.read_file(url)

# 각 구의 중심점 계산
gdf['centroid'] = gdf.geometry.centroid

# 아파트 정보 데이터 불러오기
apartment_data = pd.read_csv('./data/aparts.csv')
apartment_gdf = gpd.GeoDataFrame(apartment_data, geometry=gpd.points_from_xy(apartment_data['좌표X'], apartment_data['좌표Y']), crs='EPSG:4326')

# 교육시설 정보 데이터 불러오기
school_data = pd.read_csv('./export/education/final_graded_school_locations.csv')
school_gdf = gpd.GeoDataFrame(school_data, geometry=gpd.points_from_xy(school_data['lon'], school_data['lat']), crs='EPSG:4326')

# 클릭 이벤트 함수 정의
def on_click(event):
    # 클릭된 좌표 가져오기
    click_point = Point(event.xdata, event.ydata)
    
    # 각 구의 중심점과 클릭한 좌표 사이의 거리 계산
    gdf['distance'] = gdf['centroid'].distance(click_point)
    
    # 가장 가까운 구 찾기
    closest_gu = gdf.loc[gdf['distance'].idxmin()]
    print(f"가장 가까운 구: {closest_gu['name']}, 거리: {closest_gu['distance']:.2f}")
    
    # 가장 가까운 구의 지도 확대해서 보여주기
    fig, ax = plt.subplots(figsize=(10, 10))
    gdf.plot(ax=ax, color='lightgray')  # 모든 구의 지도 추가
    closest_gu_gdf = gpd.GeoDataFrame([closest_gu], geometry='geometry')
    closest_gu_gdf.plot(ax=ax, color='red')  # 가장 가까운 구를 빨강으로 표시
    
    # 해당 구 내의 아파트 정보 표시 (점 크기 증가)
    apartments_in_gu = apartment_gdf[apartment_gdf.within(closest_gu['geometry'])]
    apartments_in_gu.plot(ax=ax, color='blue', markersize=80, label='아파트')  # markersize를 더 크게 설정

    # 해당 구의 경계에 맞춰 축 설정 (확대)
    minx, miny, maxx, maxy = closest_gu['geometry'].bounds
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)

    plt.title(f"가장 가까운 구: {closest_gu['name']}")
    plt.legend()
    plt.show()

# 지도 그리기
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column="name", legend=True)
plt.title("서울특별시 구 경계 지도")

# 클릭 이벤트 연결
fig.canvas.mpl_connect("button_press_event", on_click)
plt.show()
