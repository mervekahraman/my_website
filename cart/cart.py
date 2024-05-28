from Shop.models import Product,Profile

class Cart():

    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key']= {}
        self.cart = cart
        # cart = self.session.get('session_key')
        # if 'session_key' not in request.session:
        #     cart = self.session['session_key']= {}
        # self.cart = cart


        # # Retrieve the cart from session or initialize it if it doesn't exist
        # self.cart = self.session.get(self.cart_key, {})
        # if self.cart_key not in self.session:
        #     self.session[self.cart_key] = self.cart
        #     self.session.modified = True

    # def add(self, product, quantity):
    #     product_id = str(product.id)
    #     product_qty = str(quantity)
    #     if product_id in self.cart:
    #         pass
    #     else:
    #         self.cart[product_id] = int(product_qty)
    #
    #     self.session.modified = True
    #     return self.cart
    # def __len__(self):
    #     return len(self.cart)

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carts = str(self.cart)
            carts = carts.replace("'", "\"")
            current_user.update(old_cart_values=str(carts))

    def __len__(self):

        return sum(self.cart.values())
    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        return products

    def get_quantities(self):
        return self.cart

    def update(self,product,quantity):
        product_id = str(product.id)
        product_quantity = int(quantity)

        self.cart[product_id] = product_quantity

        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carts = str(self.cart)
            carts = carts.replace("\'", "\"")
            current_user.update(old_cart_values=str(carts))

        return self.cart

    def delete(self,product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carts = str(self.cart)
            carts = carts.replace("\'", "\"")
            current_user.update(old_cart_values=str(carts))

    def database_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            self.cart[product_id] += int(product_qty)
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carts = str(self.cart)
            carts = carts.replace("'", "\"")
            current_user.update(old_cart_values=str(carts))

    def totals(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for product in products:
            if product.is_Sale:
                total += product.sale_price * quantities[str(product.id)]

        for product in products:
            if not product.is_Sale:
                total += product.price * quantities[str(product.id)]

        return total

        # product_ids = self.cart.keys()
        # products = Product.objects.filter(id__in=product_ids)
        # quantities = self.cart
        #
        #
        # for product in products:
        #     if product.is_Sale:
        #         total += product.sale_price * quantities[str(product.id)]
        #
        # for product in products:
        #     if not product.is_Sale:
        #         total += product.price * quantities[str(product.id)]
        #
        # return total

    def get_items(self):
        items = []
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            item = {
                'product': product,
                'quantity': self.cart[str(product.id)],
                'price': product.sale_price if product.is_Sale else product.price,
            }
            items.append(item)
        return items

    def clear(self):
        self.cart = {}
        self.session['session_key'] = self.cart
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            current_user.update(old_cart_values="{}")




