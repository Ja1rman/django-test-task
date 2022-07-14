from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import db
from api.data import *
import json


def get_foods(request):
    def json_normal(food_categories):
        result = []
        for val in food_categories:
            food_cat_node = {
                'id': val[0],
                'name_ru': val[1],
                'name_en': val[2],
                'name_ch': val[3],
                'order_id': val[4],
                'foods': [],
            }
            result.append(food_cat_node)
        return result


    def add_foods(result, foods, additional):
        for val in foods:
            if val[10]:
                food_node = {
                    "internal_code": val[4],
                    "code": val[3],
                    "name_ru": val[5],
                    "description_ru": val[6],
                    "description_en": val[7],
                    "description_ch": val[8],
                    "is_vegan": val[1],
                    "is_special": val[2],
                    "cost": val[9],
                    "additional":[]
                }
                for elem in additional:
                    if elem[0] == food_node["name_ru"]:
                        food_node["additional"].append(elem[1])
                
                for i in range(len(result)):
                    if result[i]["name_ru"] == val[0]:
                        result[i]["foods"].append(food_node)
                        break
        return result


    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM FoodCategory;')
        food_categories = cursor.fetchall()
        result = json_normal(food_categories)
        cursor.execute('SELECT * FROM Food;')
        foods = cursor.fetchall()
        cursor.execute('SELECT * FROM additional;')
        additional = cursor.fetchall()
        result = add_foods(result, foods, additional)
        result_with_filter = []
        for val in result:
            if len(val["foods"]) != 0:
                result_with_filter.append(val)

    finally:
        cursor.close()
    
    #category = FoodCategory()
    #category.name_ru = 'Телефоны'
    #serializer = FoodListSerializer(category)
    #print(serializer.data)

    return HttpResponse(JsonResponse(result_with_filter, safe=False))
