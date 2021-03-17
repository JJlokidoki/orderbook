import pytest
import orderbook
from random import uniform, randint
import datetime

"""Fixtures:
1. Create orderbook
2. 

Tests:
1. create order
2. neg create order
3. remove order
4. neg remove order
5. get data
6. neg get data
7. snapshot"""

@pytest.fixture(scope='session')
def new_orderbook():
    """
    Create new orders book and empty list for created orders
    """
    return orderbook.OrderBook('AAPL'), []

class TestOrdersBook:
    @pytest.fixture(autouse=True)
    def setup(self, new_orderbook):
        self.new_orderbook, self.created_orders = new_orderbook

    @pytest.mark.parametrize("trans_type_p, price_p, volume_p", [
        ('bid', round(uniform(0, 99999), 2), randint(0, 9999)),
        ('ask', round(uniform(0, 99999), 3), randint(0, 9999))
    ])
    def test_creating_orders(self, trans_type_p, price_p, volume_p):
        ord_num = self.new_orderbook.create_order(trans_type_p, price_p, volume_p)
        self.created_orders.append(ord_num)
        try:
            time = datetime.datetime.strptime(self.new_orderbook.order[ord_num].placement_time, '%H:%M:%S')
        except ValueError:
            time = None
        assert self.new_orderbook.order[ord_num].trans_type == trans_type_p
        assert self.new_orderbook.order[ord_num].price == price_p
        assert self.new_orderbook.order[ord_num].volume == volume_p
        assert self.new_orderbook.order[ord_num].status == 0
        assert isinstance(time, datetime.datetime), "Incorrect time format"

    def test_neg_creating_orders(self):
        pass

    def test_remove_orders(self):
        pass

    def test_neg_remove_orders(self):
        pass

    def test_getting_order_data(self):
        id_for_get = randint(0, len(self.created_orders))
        data = self.new_orderbook.get_order_data(id_for_get)
        template = "Transaction type is: {}; Price: {}; Volume of order: {}; Status: {}"
        assert template.format(self.new_orderbook.order[id_for_get].trans_type, \
                               self.new_orderbook.order[id_for_get].price, \
                               self.new_orderbook.order[id_for_get].volume, \
                               self.new_orderbook.order[id_for_get].status   ) == data

    def test_neg_getting_order_data(self):
        pass

    def test_snapshot(self):
        pass

