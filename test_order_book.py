import pytest
import datetime
from typing import List
from random import uniform, randint, choice

import orderbook


@pytest.fixture(scope='session')
def new_orderbook():
    """
    Create new orders book and empty list for created orders
    """
    return orderbook.OrderBook('AAPL'), []

class TestOrdersBook:
    @pytest.fixture(autouse=True)
    def setup(self, new_orderbook):
        """
        Setup order book instance
        """
        self.new_orderbook, self.created_orders = new_orderbook

    @pytest.mark.parametrize("trans_type_p, price_p, volume_p", [
        ('bid', round(uniform(0, 99999), 2), randint(0, 9999)),
        ('ask', round(uniform(0, 99999), 3), randint(0, 9999)),
        ('ask', round(uniform(0, 99999), 1), randint(0, 9999))
    ], ids = ['correct bid', 'correct ask', 'correct ask'])
    def test_creating_orders(self, trans_type_p, price_p, volume_p):
        """
        Test creating orders
        """
        ord_num = self.new_orderbook.create_order(trans_type_p, price_p, volume_p)
        self.created_orders.append(ord_num)
        try:
            time = datetime.datetime.strptime(self.new_orderbook.order[ord_num].placement_time, '%H:%M:%S')
        except ValueError:
            time = None
        assert self.new_orderbook.order[ord_num].trans_type == trans_type_p, "Incorrect type"
        assert self.new_orderbook.order[ord_num].price == price_p, "Incorrect price"
        assert self.new_orderbook.order[ord_num].volume == volume_p, "Incorrect volume"
        assert self.new_orderbook.order[ord_num].status == 0, "Incorrect status"
        assert isinstance(time, datetime.datetime), "Incorrect time format"

    @pytest.mark.parametrize("trans_type_p, price_p, volume_p", [
        ('inc', round(uniform(0, 99999), 2), 1),
        ('bid', 'str', randint(0, 9999)), 
        ('bid', 1, 0),
        ('ask', 2, -1)
    ], ids = ['incorrect type', 'incorrect price', 'incorrect volume', 'incorrect volume'])
    def test_neg_creating_orders(self, trans_type_p, price_p, volume_p):
        """
        Negative tests creating orders
        """
        with pytest.raises((orderbook.UndefinedType, AssertionError)):
            ord_num = self.new_orderbook.create_order(trans_type_p, price_p, volume_p)

    def test_remove_orders(self):
        """
        Test removing orders
        """
        id_to_del = choice(self.created_orders)
        self.created_orders.remove(id_to_del)
        res = self.new_orderbook.remove_order(id_to_del)
        assert res == 0
        assert self.new_orderbook.order.get(id_to_del) is None, "Order doesn't deleted"
        assert self.new_orderbook.deleted_orders.get(id_to_del), "Order doesn't exist in list of deleted orders"

    @pytest.mark.parametrize("id_to_del", [
        (-1), (0), ('123')
    ], ids = ['incorrect id (neg int)', 'incorrect id (zero)', 'incorrect id (str)'])
    def test_neg_remove_orders(self, id_to_del):
        """
        Negative tests removing orders
        """
        with pytest.raises(orderbook.UndefinedID):
            res = self.new_orderbook.remove_order(id_to_del)

    def test_getting_order_data(self):
        """
        Test getting data of orders
        """
        id_for_get = choice(self.created_orders)
        data = self.new_orderbook.get_order_data(id_for_get)
        template = "Transaction type is: {}; Price: {}; Volume of order: {}; Status: {}"
        assert template.format(self.new_orderbook.order[id_for_get].trans_type, \
                               self.new_orderbook.order[id_for_get].price, \
                               self.new_orderbook.order[id_for_get].volume, \
                               self.new_orderbook.order[id_for_get].status) == data, "Incorrect formatting"

    @pytest.mark.parametrize("id_for_get", [
        (-1), (0), ('123')
    ], ids = ['incorrect id (neg int)', 'incorrect id (zero)', 'incorrect id (str)'])
    def test_neg_getting_order_data(self, id_for_get):
        """
        Negative tests getting data of orders
        """
        with pytest.raises(orderbook.UndefinedID):
            res = self.new_orderbook.remove_order(id_for_get)

    def test_snapshot(self):
        """
        Test snapshot
        """
        snap = self.new_orderbook.snapshot()
        assert sorted([i for i in snap]) == ['asks', 'bids'], "Incorrect keys"
        assert not [i['quantity'] for i in snap['asks'] if i['quantity'] < 1], "Snapshot has incorrect quantity value for asks"
        assert not [i['quantity'] for i in snap['bids'] if i['quantity'] < 1], "Snapshot has incorrect quantity value for bids"
        assert len([n['price'] for n in snap['asks']]) == len(set([n['price'] for n in snap['asks']])), "Snapshot has duplicate price value for asks"
        assert len([n['price'] for n in snap['bids']]) == len(set([n['price'] for n in snap['bids']])), "Snapshot has duplicate price value for bids"
