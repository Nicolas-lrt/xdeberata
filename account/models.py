from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from shopping.models import Product


class Account(models.Model):
    user = models.ForeignKey(User, verbose_name='Associated user', on_delete=models.CASCADE)
    userId = models.IntegerField(null=True)
    default_shipping_address = models.ForeignKey("Address",
                                                 related_name="default_shipping_address",
                                                 null=True,
                                                 verbose_name="Adresse de livraison par défaut",
                                                 on_delete=models.CASCADE
                                                 )
    default_invoicing_address = models.ForeignKey("Address",
                                                  related_name="default_invoicing_address",
                                                  null=True,
                                                  verbose_name="Adresse de facturation par défaut",
                                                  on_delete=models.CASCADE
                                                  )
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    def nb_commande(self):
        orders = Order.objects.filter(client=self)
        nb = 0
        for i in orders:
            nb += 1
        return nb


class Address(models.Model):
    """
    Une adresse est liée à un client et pourra être utilisée pour la livraison ou la facturation d'une commande.
    """
    client = models.ForeignKey(Account, verbose_name='Associated account', on_delete=models.CASCADE)
    MISTER = 'MR'
    MISSES = 'MRS'
    GENDER = (
        (MISTER, 'Monsieur'),
        (MISSES, 'Madame'),
    )
    gender = models.CharField(max_length=4, choices=GENDER, default=MISTER, verbose_name="Civilité")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    company = models.CharField(max_length=50, blank=True, verbose_name="Société")
    address = models.CharField(max_length=255, verbose_name="Adresse")
    additional_address = models.CharField(max_length=255, blank=True, verbose_name="Complément d'adresse")
    postcode = models.CharField(max_length=10, verbose_name="Code postal")
    city = models.CharField(max_length=50, verbose_name="Ville")
    phone = models.CharField(max_length=10, verbose_name="Téléphone")
    mobilephone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone portable")
    workphone = models.CharField(max_length=10, blank=True, verbose_name="Téléphone travail")

    class Meta:
        verbose_name = 'Adresse'
        verbose_name_plural = 'Adresses'

    def __str__(self):
        return 'Adresse du client \'' + self.client.user.username + '\''

    def __unicode__(self):
        return self.first_name + " " + self.last_name + " (" + self.address + ", " + self.postcode + " " + self.city + ")"


class CartLine(models.Model):
    """
    Une ligne de panier client.
    """
    client = models.ForeignKey(Account, verbose_name='Associated user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'User cart line'
        verbose_name_plural = 'User cart lines'

    def total(self):
        return round(self.product.price * float(self.quantity), 2)

    def __str__(self):
        return '\'' + self.client.user.username + '\' user cart line'


class Order(models.Model):
    """
    Une commande est passée par un client et comprend des lignes de commandes ainsi que des adresses.
    """
    client = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Client ayant passé commande")
    order_date = models.DateField(verbose_name="Date de la commande")
    WAITING = 'W'
    PAID = 'P'
    SHIPPED = 'S'
    CANCELED = 'C'
    STATUS = (
        (WAITING, 'En attente de validation'),
        (PAID, 'Payée'),
        (SHIPPED, 'Expédiée'),
        (CANCELED, 'Annulée'),
    )
    status = models.CharField(max_length=1, choices=STATUS, default=WAITING, verbose_name="Statut de la commande")
    # stripe_charge_id = models.CharField(max_length=30, verbose_name="Identifiant de transaction Stripe", blank=True)

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def __str__(self):
        return 'Commande du client \'' + self.client.user.username + '\' du ' + str(self.order_date)

    @property
    def total(self):
        total = 0
        order_details = OrderDetail.objects.filter(order_id=self.id)
        for order_detail in order_details:
            total += order_detail.total()
        return round(total, 2)

    def article_qty(self):
        order_details = OrderDetail.objects.filter(order_id=self.id)
        total = 0
        for detail in order_details:
            total += detail.qty
        return total


class OrderDetail(models.Model):
    """
    Une ligne de commande référence un produit, la quantité commandée ainsi que les prix associés.
    Elle est liée à une commande.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Commande associée")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(verbose_name="Quantité")
    product_unit_price = models.FloatField(verbose_name="Prix unitaire du produit")

    class Meta:
        verbose_name = 'Ligne d\'une commande'
        verbose_name_plural = 'Lignes de commandes'

    def total(self):
        return round(self.product_unit_price * float(self.qty), 2)


