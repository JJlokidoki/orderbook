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


class Order(NamedTuple):
    """ 
    Набор параметров заявки:
    1. type (bid/ask) 
    2. price
    3. volume
    4. placement time
    5. action (0 - come, 1 - delete)
    """
    trans_type: str
    price: float
    volume: int
    placement_time: str
    action: int

    def __str__(self):
        return f"Transaction type is: {self.trans_type}; Price: {self.price}; Volume of order: {self.volume}"


class OrderBook:
    """
    Orders book parametrs
    1. item - lot (e.g. AAPL)
    2. order - place for preservation
    3. date 
    """
    def __init__(self, item):
        self.item = item
        self.order = {}
        self.order_id = 0
        self.date = datetime.now().strftime("%d/%m/%Y")

    def create_order(self, trans_type, price, volume):
        new_id = 1
        place_time = datetime.now().strftime("%H:%M:%S")
        self.order.update({new_id: Order(trans_type, price, volume, place_time, 0)})

    def remove_order(self, id_to_del):
        if id_to_del in self.order:
            self.order.update({id_to_del: self.order[id_to_del]._replace(action = 1)})
            return 1
        raise UndefinedID(id_to_del)

    def get_order_data(self, id_for_get):
        if id_to_del in self.order:
            return self.order[id_for_get]
        raise UndefinedID(id_for_get)

    def snapshot(self):
        """
        template = {"asks": [{
            "price": 123,
            "volume": 1000
        }]
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
        return  {"asks": asks_list, "bids": bids_list}


    def _sort_orders(self):
        return OrderedDict(sorted(self.order.items(), key = lambda t: t[1].price))



if __name__ == "__main__":
    a = OrderBook('AAPL')
    a.create_order('bid', 12.12, 123)
    print(a.snapshot())
    