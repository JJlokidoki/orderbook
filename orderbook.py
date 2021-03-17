from typing import NamedTuple
from datetime import datetime
from collections import OrderedDict


class UndefinedID(Exception):
    """
    Custom exception for unknown ids
    """
    def __init__(self, und_id):
        self.msg = f"{und_id} doesn't exist in order book"
        super().__init__(self.msg)


class UndefinedType(Exception):
    """
    Custom exception for unknown transaction type
    """
    def __init__(self, t_type):
        self.msg = f"{t_type} unknown transaction type. Use 'bid' or 'ask' "
        super().__init__(self.msg)


class Order(NamedTuple):
    """ 
    Order params:
    1. type (bid/ask) 
    2. price
    3. volume
    4. placement time
    5. status (0 - come, 1 - delete)
    """
    trans_type: str
    price: float
    volume: int
    placement_time: str
    status: int

    def __str__(self):
        return f"Transaction type is: {self.trans_type}; Price: {self.price}; Volume of order: {self.volume}; Status: {self.status}"


class OrderBook:
    """
    Orders book parametrs
    1. item - lot (e.g. AAPL)
    2. order - place for preservation
    3. date 
    """
    def __init__(self, item: str):
        self.item = item
        self.order = {}
        self.order_id = 0
        self.date = datetime.now().strftime("%d/%m/%Y")
        self.deleted_orders = {}

    def create_order(self, trans_type: str, price: float, volume: int):
        """
        Create new order in orders book
        """
        assert isinstance(price, float)
        assert isinstance(volume, int)
        if trans_type != 'bid' and trans_type != 'ask':
            raise UndefinedType(trans_type)
        self.order_id += 1
        place_time = datetime.now().strftime("%H:%M:%S")
        self.order.update({self.order_id: Order(trans_type, price, volume, place_time, 0)})
        return self.order_id

    def remove_order(self, id_to_del: int):
        """
        Change status of order to 'delete'
        """
        if id_to_del in self.order:
            self.deleted_orders.update({id_to_del: self.order[id_to_del]._replace(status = 1)})
            self.order.pop(id_to_del)
            return 0
        raise UndefinedID(id_to_del)

    def get_order_data(self, id_for_get: int):
        """
        Getting data of order
        """
        if id_for_get in self.order:
            return str(self.order[id_for_get])
        raise UndefinedID(id_for_get)

    def snapshot(self):
        """
        Getting snapshot of order book
        """
        tmp_dict = self._sort_orders()
        bids_list = []
        asks_list = []
        print(tmp_dict)
        for i, o in tmp_dict.items():
            if o.trans_type == 'bid':
                if o.price not in bids_list:
                    bids_list.append({"price": o.price, 
                                      "quantity": 0})
                else:
                    bids_list[-1].update({"quantity": bids_list[-1]["quantity"] + o.volume})
            elif o.trans_type == 'ask':
                if o.price not in asks_list:
                    asks_list.append({"price": o.price, 
                                      "quantity": 0})
                else:
                    asks_list[-1].update({"quantity": asks_list[-1]["quantity"] + o.volume})
        return {"asks": asks_list, "bids": bids_list}


    def _sort_orders(self):
        return OrderedDict(sorted(self.order.items(), key = lambda t: t[1].price))


if __name__ == "__main__":
    a = OrderBook('AAPL')
    a.create_order('bid', 12.12, 123)
    print(a.snapshot())
    