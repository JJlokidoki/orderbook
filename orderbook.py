from typing import NamedTuple, Dict
from datetime import datetime
from collections import OrderedDict


class UndefinedID(Exception):
    """
    Custom exception for unknown ids
    """
    def __init__(self, und_id):
        self.msg = f" {und_id} doesn't exist in order book"
        super().__init__(self.msg)


class UndefinedType(Exception):
    """
    Custom exception for unknown transaction type
    """
    def __init__(self, t_type):
        self.msg = f" {t_type} is unknown transaction type. Use 'bid' or 'ask' "
        super().__init__(self.msg)


class IncorrectVolume(Exception):
    """
    Custom exception for incorrect order volume
    """
    def __init__(self, vol):
        self.msg = f" {vol} is incorrect volume for orders"
        super().__init__(self.msg)

class Order(NamedTuple):
    """ 
    Class of orders
    Params:
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

    def __str__(self) -> str:
        return f"Transaction type is: {self.trans_type}; Price: {self.price}; Volume of order: {self.volume}; Status: {self.status}"


class OrderBook:
    """
    Class of order book
    Parametrs
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

    def create_order(self, trans_type: str, price: float, volume: int) -> int:
        """
        Create new order in orders book
        """
        assert isinstance(price, float)
        assert isinstance(volume, int)
        if volume < 1:
            raise IncorrectVolume(volume)
        if trans_type not in ['bid', 'ask']:
            raise UndefinedType(trans_type)
        self.order_id += 1
        place_time = datetime.now().strftime("%H:%M:%S")
        self.order.update({self.order_id: Order(trans_type, price, volume, place_time, 0)})
        return self.order_id

    def remove_order(self, id_to_del: int) -> int:
        """
        Change status of order to 'delete'
        """
        if id_to_del in self.order:
            self.deleted_orders.update({id_to_del: self.order[id_to_del]._replace(status = 1)})
            self.order.pop(id_to_del)
            return 0
        raise UndefinedID(id_to_del)

    def get_order_data(self, id_for_get: int) -> str:
        """
        Getting data of order
        """
        if id_for_get in self.order:
            return str(self.order[id_for_get])
        raise UndefinedID(id_for_get)

    def snapshot(self) -> Dict:
        """
        Getting snapshot of order book
        """
        tmp_dict = self._sort_orders()
        bids_list = []
        asks_list = []
        for _, o in tmp_dict.items():
            if o.trans_type == 'bid':
                if o.price not in [bid['price'] for bid in bids_list]:
                    bids_list.append({"price": o.price, 
                                      "quantity": o.volume})
                else:
                    bids_list[-1].update({"quantity": bids_list[-1]["quantity"] + o.volume})
            elif o.trans_type == 'ask':
                if o.price not in [ask['price'] for ask in asks_list]:
                    asks_list.append({"price": o.price, 
                                      "quantity": o.volume})
                else:
                    asks_list[-1].update({"quantity": asks_list[-1]["quantity"] + o.volume})
        return {"asks": asks_list, "bids": sorted(bids_list, key = lambda t: t['price'])}


    def _sort_orders(self) -> OrderedDict:
        """
        Sorting orders
        """
        return OrderedDict(sorted(self.order.items(), key = lambda t: t[1].price, reverse=True))


def pretty_snap(snap: Dict, name: str) -> None:
    delim = '|'
    res = []
    for ask in snap['asks']:
        res.append(str(ask['price']).ljust(7) + delim + str(ask['quantity']).rjust(7))
    res.append('')
    for bid in snap['bids']:
        res.append(str(bid['quantity']).ljust(7) + delim + str(bid['price']).rjust(7))

    print(name.center(15))
    print('\n'.join(res))


if __name__ == '__main__':
    O = OrderBook('BTC')
    x = [{'tt': 'bid', 'p': 11.23, 'v': 2}, {'tt': 'bid', 'p': 10.00, 'v': 7}, {'tt': 'bid', 'p': 10.00, 'v': 7}, 
    {'tt': 'ask', 'p': 305.00, 'v': 1}, {'tt': 'ask', 'p': 0.5, 'v': 11}, {'tt': 'ask', 'p': 0.5, 'v': 11}]
    for i in x:
        O.create_order(i['tt'], i['p'], i['v'])
    c = O.snapshot()
    pretty_snap(c, O.item)