import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item need a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
        
        # item = next(filter(lambda x : x['name'] == name, items), None)
        # return {'item' : item}, 200 if item else 404
    
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name '{}' already exists.".format(name)}, 400
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}
        return item.json(), 201
    
    # 这里有个 primary key 单独制定 一个item obj的问题， 非常重要
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item deleted'}
#返回table里面所有的item
class ItemList(Resource):
    def get(self):
        return {'item' : [x.json() for x in ItemModel.query.all()]}

        #ItemModel.query[it's query builder now!].all()[return every rows as object!]