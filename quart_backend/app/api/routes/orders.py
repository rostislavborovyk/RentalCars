import jwt
from quart_openapi import Resource
from quart import make_response, jsonify, request, current_app, session

from app.api.utils.reqparsers import OrderReqParser
from app.api.utils.serializers import OrderSerializer
from app.api.utils.response_formers import OrdersResponseFormer
from app.models import Order
from app.api import bp
from app.api.common import get_data_for_table, get_item_from_id, get_num_of_pages, get_items_query_params, \
    get_items_date_query_params


@bp.route("/orders/<string:id_>")
class OrdersResource(Resource):
    async def get(self, id_):
        """
        Returns order by id
        example query http://localhost:5000/api/orders/<some_id> with GET method
        """

        response = await get_item_from_id(id_, Order.select_by_id)
        if response[0] == "error":
            return await response[1]
        serialized = OrderSerializer.to_dict(response[1])
        return await make_response(jsonify(serialized), 200)

    async def put(self, id_):
        return await make_response(jsonify({"status": "not implemented"}), 200)

    async def delete(self, id_):
        """
        Deletes order by id
        example query http://localhost:5000/api/orders/<some_id> with DELETE method
        """

        try:
            status = await Order.delete(id_)
            if status == 0:
                return await make_response(jsonify({"status": "no item with such id"}), 400)
        except Exception as e:
            print(e)
            return await make_response(jsonify({"status": "db error occurred"}), 500)
        return await make_response(jsonify({"status": "ok", "id": id_}), 200)


@bp.route("/orders")
class OrdersListResource(Resource):
    async def post(self):
        """
        Posts order to db
        example query http://localhost:5000/api/orders with POST method

        Example data:
        {
            "id_client": "41914b6550844be386bfb1f20a45dad1",
            "id_car": "876fa87435874d60a77ccfe6b4db1fa8",
            "rental_time": 10
        }
        """

        json_obj = await OrderReqParser.parse_request()
        # print(json_obj["jwt"])
        if "id_client" not in json_obj.keys():
            json_obj.update({
                "id_client": jwt.decode(json_obj["jwt"].encode("utf-8"), current_app.config["SECRET_KEY"])["client_id"]
            })
            json_obj.pop("jwt")
        print(json_obj)
        try:
            id_ = await Order.insert(json_obj)
        except Exception as e:
            print(e)
            return await make_response(jsonify({"status": "db error occurred"}), 500)
        return await make_response(jsonify({"status": "ok", "id": id_}), 200)


@bp.route("/orders/table", methods=["GET"])
async def orders_table():
    db_response = await get_data_for_table(
        select_func=Order.select_for_orders_table,
        **{**get_items_query_params(), **get_items_date_query_params()}
    )
    if len(db_response) == 0:
        return await make_response(jsonify(OrdersResponseFormer.form([], 0)), 200)

    if db_response[0] == "error":
        return await db_response[1]

    params = dict(
        date_filter=True if request.args.get("from_date") else None,
        is_orders=True,
        params=get_items_date_query_params()
    )
    num_of_pages = await get_num_of_pages(Order.count_all, **params)
    return await make_response(jsonify(OrdersResponseFormer.form(db_response, num_of_pages)), 200)
