class Shop:
    def __init__(self):
        self.available_items = [
        ]

    def purchase_item(self, user, item_name):
        item = next((item for item in self.available_items if item.name == item_name), None)
        if item and user.balance >= item.price:
            user.balance -= item.price
            if item.effect:
                pass
            return True
        return False

    def list_items(self):
        return self.available_items
