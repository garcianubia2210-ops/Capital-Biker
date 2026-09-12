from django.db import models


class Categoria(models.Model):

    nombre = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    imagen = models.ImageField(
        upload_to="categorias/",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Color(models.Model):

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Talla(models.Model):

    nombre = models.CharField(
        max_length=20,
        unique=True
    )

    class Meta:
        verbose_name = "Talla"
        verbose_name_plural = "Tallas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="productos"
    )

    nombre = models.CharField(max_length=150)

    marca = models.CharField(max_length=100)

    descripcion = models.TextField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    precio_anterior = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    opiniones = models.PositiveIntegerField(default=0)

    envio_gratis = models.BooleanField(default=True)

    imagen = models.ImageField(
        upload_to="productos/"
    )

    disponible = models.BooleanField(default=True)

    nuevo = models.BooleanField(default=False)

    oferta = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class VarianteProducto(models.Model):

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="variantes"
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        related_name="variantes"
    )

    talla = models.ForeignKey(
        Talla,
        on_delete=models.PROTECT,
        related_name="variantes"
    )

    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Variante de producto"
        verbose_name_plural = "Variantes de productos"
        unique_together = ("producto", "color", "talla")

    def __str__(self):
        return f"{self.producto.nombre} - {self.color.nombre} - {self.talla.nombre}"


class Carrito(models.Model):

    creado = models.DateTimeField(auto_now_add=True)

    actualizado = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(
            item.subtotal()
            for item in self.items.all()
        )

    def __str__(self):
        return f"Carrito #{self.id}"


class ItemCarrito(models.Model):

    carrito = models.ForeignKey(
        Carrito,
        on_delete=models.CASCADE,
        related_name="items"
    )

    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.CASCADE,
        related_name="items_carrito"
    )

    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.variante.producto.precio * self.cantidad

    def __str__(self):
        return (
            f"{self.variante.producto.nombre} "
            f"- {self.variante.color.nombre} "
            f"- {self.variante.talla.nombre}"
        )
        
       
class Pedido(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("confirmado", "Confirmado"),
        ("preparando", "En preparación"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    METODOS_PAGO = [
        ("efectivo", "Efectivo contra entrega"),
        ("transferencia", "Transferencia bancaria"),
    ]

    nombre = models.CharField(max_length=150)

    telefono = models.CharField(max_length=30)

    correo = models.EmailField()

    direccion = models.TextField()

    metodo_pago = models.CharField(
        max_length=20,
        choices=METODOS_PAGO
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre}"


class DetallePedido(models.Model):

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.precio * self.cantidad

    def __str__(self):
        return (
            f"Pedido #{self.pedido.id} - "
            f"{self.variante.producto.nombre}"
        )
