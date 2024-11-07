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
    closest_gu_gdf.plot(ax=ax, color='green')  # 가장 가까운 구를 녹색으로 표시
    
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

    # 아파트 클릭 이벤트 함수 정의 및 연결
    def on_apartment_click(event):
        # 클릭된 좌표 가져오기
        click_point = Point(event.xdata, event.ydata)

        # 클릭된 위치와 가장 가까운 아파트 찾기
        apartment_gdf['distance'] = apartment_gdf['geometry'].distance(click_point)
        closest_apartment = apartment_gdf.loc[apartment_gdf['distance'].idxmin()]
        print(f"가장 가까운 아파트: {closest_apartment['k-아파트명']}, 거리: {closest_apartment['distance']:.2f}")

        # 해당 구 내의 교육시설 표시
        schools_near_apartment = school_gdf[school_gdf.within(closest_gu['geometry'])]

        # 교육시설 지도 표시 (확대 추가)
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='lightgray')
        closest_gu_gdf.plot(ax=ax, color='gray')
        apartments_in_gu.plot(ax=ax, color='blue', markersize=80, label='아파트')
        schools_near_apartment.plot(ax=ax, color='green', markersize=50, label='교육시설')

        # 해당 아파트 주변으로 확대
        minx, miny, maxx, maxy = closest_apartment['geometry'].bounds
        ax.set_xlim(minx - 0.01, maxx + 0.01)
        ax.set_ylim(miny - 0.01, maxy + 0.01)

        plt.title(f"가장 가까운 아파트: {closest_apartment['k-아파트명']} 주변 교육시설")
        plt.legend()
        plt.show()

    # 클릭 이벤트 연결 시 변경된 부분
    fig.canvas.mpl_connect("button_press_event", on_apartment_click)

    # 교육시설 클릭 이벤트 함수 정의 및 연결
    # 등급에 따른 색상 맵핑 함수
    def get_color_by_grade(grade):
        if grade == 2:
            return 'purple'  # 높은 등급
        elif grade == 1:
            return 'yellow'  # 중간 등급
        else:
            return 'gray'    # 낮은 등급

    # 구 내 교육시설을 등급별로 다른 색상으로 표시하는 함수
    def plot_schools_by_grade(ax, schools_in_gu):
        # 등급별로 다른 색상을 적용하여 plot
        colors = schools_in_gu['등급'].apply(get_color_by_grade)
        schools_in_gu.plot(ax=ax, color=colors, markersize=50, label='교육시설')

    # 교육시설 클릭 이벤트 함수 수정
    def on_school_click(event):
        # 클릭된 좌표 가져오기
        click_point = Point(event.xdata, event.ydata)

        # 클릭된 위치와 가장 가까운 교육시설 찾기
        school_gdf['distance'] = school_gdf['geometry'].distance(click_point)
        closest_school = school_gdf.loc[school_gdf['distance'].idxmin()]
        print(f"가장 가까운 교육시설: {closest_school['학교명']}, 등급: {closest_school['등급']}, 거리: {closest_school['distance']:.2f}")

        # 선택한 교육시설 주변의 아파트와 다른 교육시설 필터링 (예: 0.01도 이내)
        buffer_distance = 0.01  # 적절한 거리로 설정
        apartments_near_school = apartment_gdf[apartment_gdf.distance(closest_school['geometry']) < buffer_distance]
        schools_near_school = school_gdf[school_gdf.distance(closest_school['geometry']) < buffer_distance]

        # 교육시설 지도 표시 (선택된 교육시설 주변 확대)
        fig, ax = plt.subplots(figsize=(10, 10))
        gdf.plot(ax=ax, color='lightgray')  # 모든 구 표시
        apartments_near_school.plot(ax=ax, color='blue', markersize=80, label='아파트')  # 아파트 표시
        plot_schools_by_grade(ax, schools_near_school)  # 등급별 색상으로 교육시설 표시

        # 선택한 교육시설 주변으로 확대
        minx, miny, maxx, maxy = closest_school['geometry'].buffer(buffer_distance).bounds
        ax.set_xlim(minx, maxx)
        ax.set_ylim(miny, maxy)

        plt.title(f"{closest_school['학교명']} 주변 아파트 및 교육시설")
        plt.legend()
        plt.show()

    # 교육시설 클릭 이벤트 연결
    fig.canvas.mpl_connect("button_press_event", on_school_click)

# 지도 그리기
fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax, column="name", legend=True)
plt.title("서울특별시 구 경계 지도")

# 클릭 이벤트 연결
fig.canvas.mpl_connect("button_press_event", on_click)
plt.show()
