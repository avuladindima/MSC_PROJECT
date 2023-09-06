from cart.cart import Cart

class CartUpdate(Cart):
    
    def cart_update_add(self,quantity,product,dosage,drug_type,flavour,action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        
        if str(product.id) not in self.cart.keys():

            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.name,
                'quantity': int(quantity) if quantity is not None else 0,
                'price': str(product.price),
                'image': product.drug_url,
                'dosage': dosage,
                "drug_type": drug_type,
                "flavour" : flavour
            }
        else:
            dict(self.cart.items())[str(product.id)]['quantity']+=1
        self.save()