import requests
import json
from decimal import Decimal
from django.conf import settings
from typing import Dict, Optional, Tuple

class YandexDeliveryService:
    """
    Сервис для работы с Яндекс.Доставка API
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'YANDEX_DELIVERY_API_KEY', None)
        self.base_url = "https://delivery.yandex.ru/api/v1"
        self.shop_address = "Кутузовская улица, 25, Одинцово, Московская область"
        
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Геокодирование адреса через Яндекс.Геокодер
        """
        try:
            # Если нет API ключа, используем простую логику для тестирования
            api_key = getattr(settings, 'YANDEX_GEOCODER_API_KEY', '')
            if not api_key:
                return self._simple_geocode(address)
            
            url = "https://geocode-maps.yandex.ru/1.x/"
            params = {
                'apikey': api_key,
                'format': 'json',
                'geocode': address,
                'lang': 'ru_RU'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            features = data['response']['GeoObjectCollection']['featureMember']
            
            if features:
                coords_str = features[0]['GeoObject']['Point']['pos']
                longitude, latitude = map(float, coords_str.split())
                return latitude, longitude
                
        except Exception as e:
            print(f"Ошибка геокодирования: {e}")
            return self._simple_geocode(address)
    
    def _simple_geocode(self, address: str) -> Optional[Tuple[float, float]]:
        """
        Простое геокодирование для тестирования без API
        """
        address_lower = address.lower()
        
        # Координаты для разных городов
        coordinates = {
            'москва': (55.7558, 37.6176),
            'санкт-петербург': (59.9311, 30.3609),
            'одинцово': (55.6789, 37.2639),
            'красногорск': (55.8319, 37.3306),
            'подольск': (55.4289, 37.5447),
            'домодедово': (55.4363, 37.7666),
            'люберцы': (55.6758, 37.8939),
            'реутов': (55.7614, 37.8575),
            'химки': (55.8977, 37.4298),
            'мытищи': (55.9104, 37.7364),
            'королев': (55.9142, 37.8255),
            'балашиха': (55.8094, 37.9581),
        }
        
        for city, coords in coordinates.items():
            if city in address_lower:
                return coords
        
        # Если город не найден, возвращаем координаты Одинцово
        return (55.6789, 37.2639)
            
    def calculate_delivery_cost(self, delivery_address: str, weight: float = 1.0) -> Dict:
        """
        Расчет стоимости доставки
        """
        try:
            # Геокодируем адрес доставки
            delivery_coords = self.geocode_address(delivery_address)
            if not delivery_coords:
                return {
                    'success': False,
                    'error': 'Не удалось определить координаты адреса доставки',
                    'cost': 0
                }
            
            # Геокодируем адрес магазина
            shop_coords = self.geocode_address(self.shop_address)
            if not shop_coords:
                return {
                    'success': False,
                    'error': 'Не удалось определить координаты магазина',
                    'cost': 0
                }
            
            # Если есть API ключ Яндекс.Доставки, используем его
            if self.api_key:
                return self._calculate_with_yandex_api(
                    shop_coords, delivery_coords, weight
                )
            else:
                # Простой расчет по расстоянию
                return self._calculate_simple_cost(
                    shop_coords, delivery_coords, weight
                )
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка расчета доставки: {str(e)}',
                'cost': 0
            }
    
    def _calculate_with_yandex_api(self, shop_coords: Tuple[float, float], 
                                 delivery_coords: Tuple[float, float], 
                                 weight: float) -> Dict:
        """
        Расчет через официальное API Яндекс.Доставки
        """
        try:
            url = f"{self.base_url}/delivery/calculate"
            
            payload = {
                "shop_address": {
                    "latitude": shop_coords[0],
                    "longitude": shop_coords[1]
                },
                "delivery_address": {
                    "latitude": delivery_coords[0],
                    "longitude": delivery_coords[1]
                },
                "weight": weight,
                "dimensions": {
                    "length": 20,
                    "width": 20,
                    "height": 10
                }
            }
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'success': True,
                'cost': data.get('cost', 0),
                'delivery_time': data.get('delivery_time', '1-2 дня'),
                'distance': data.get('distance', 0)
            }
            
        except Exception as e:
            print(f"Ошибка API Яндекс.Доставки: {e}")
            # Fallback к простому расчету
            return self._calculate_simple_cost(shop_coords, delivery_coords, weight)
    
    def _calculate_simple_cost(self, shop_coords: Tuple[float, float], 
                             delivery_coords: Tuple[float, float], 
                             weight: float) -> Dict:
        """
        Простой расчет стоимости доставки по расстоянию
        """
        try:
            # Расчет расстояния по формуле гаверсинуса
            import math
            
            lat1, lon1 = shop_coords
            lat2, lon2 = delivery_coords
            
            R = 6371  # Радиус Земли в км
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c
            
            # Расчет стоимости доставки
            base_cost = 200  # Базовая стоимость
            cost_per_km = 15  # Стоимость за км
            weight_multiplier = 1 + (weight - 1) * 0.1  # Коэффициент веса
            
            delivery_cost = (base_cost + distance * cost_per_km) * weight_multiplier
            
            # Округляем до 50 рублей
            delivery_cost = round(delivery_cost / 50) * 50
            
            return {
                'success': True,
                'cost': delivery_cost,
                'delivery_time': '1-2 дня',
                'distance': round(distance, 1)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Ошибка расчета: {str(e)}',
                'cost': 0
            }

# Создаем экземпляр сервиса
delivery_service = YandexDeliveryService()
