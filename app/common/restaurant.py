class RestaurantInfo:
    
    def __init__(self, info, link):
        self.deal = info[0]
        self.name = info[1]
        self.link = link
        self.fee = find_delivery_fee(info)
        self.time = find_delivery_time(info)
    
    @staticmethod
    def is_satisfied(info):
        return rewards(info[0])
    
    def print_info(self):
        print('The restaurant {0} has deal {1} with fee {2} and delivery time {3}'.format(self.name, self.deal, self.fee, self.time))

def find_delivery_time(list_of_info):
    time = 'Not Found'
    for info in list_of_info:
        if "Min" in info:
            time = info
    return time

def find_delivery_fee(list_of_info):
    fee = 'Not Found'
    for info in list_of_info:
        if "Delivery Fee" in info:
            fee = info
    return fee

def rewards(x):
    return True if x == 'Buy 1, Get 1 Free' else False