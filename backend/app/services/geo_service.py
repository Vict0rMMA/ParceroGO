from app.utils import calculate_distance, validate_coordinates


class GeoService:
    @staticmethod
    def distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        return calculate_distance(lat1, lng1, lat2, lng2)

    @staticmethod
    def are_valid_for_medellin(lat: float, lng: float) -> bool:
        return validate_coordinates(lat, lng)
