from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404 # Not Found

    def post(self,name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400 # Bad Request

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error ocurred while creating the store."}, 500 # Internal Server Error

        return store.json(), 201 # Created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {'Stores': [store.json() for store in StoreModel.query.all()]}    # {'store': list(map(lambda x: x.json(), StoreModel.query.all()))}
