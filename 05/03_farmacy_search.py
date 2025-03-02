import sys
from business import find_businesses
from distance import lonlat_distance
from geocoder import get_coordinates
from mapapi_PG import show_map


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    lat, lon = get_coordinates(toponym_to_find)
    address_ll = f"{lat},{lon}"
    span = "0.01,0.01"  # Расширим область поиска

    # Поиск 10 аптек
    pharmacies = find_businesses(address_ll, span, "аптека", results=10)

    points = []
    for pharmacy in pharmacies:
        point = pharmacy["geometry"]["coordinates"]
        org_lat = float(point[1])
        org_lon = float(point[0])
        name = pharmacy["properties"]["CompanyMetaData"]["name"]
        address = pharmacy["properties"]["CompanyMetaData"]["address"]
        hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "нет данных")
        distance = round(lonlat_distance((lon, lat), (org_lon, org_lat)))

        # Определяем цвет точки
        if "круглосуточно" in hours:
            color = "pm2dgl"
        elif hours == "нет данных":
            color = "pm2grm"
        else:
            color = "pm2blm"

        points.append(f"{org_lon},{org_lat},{color}")

        snippet = f"Название: {name}\nАдрес: {address}\nВремя работы: {hours}\n" \
                  f"Расстояние: {distance}м."
        print(snippet)

    points_param = "~".join(points)
    show_map(f"ll={address_ll}&spn={span}", add_params=f"pt={points_param}")


if __name__ == "__main__":
    main()
