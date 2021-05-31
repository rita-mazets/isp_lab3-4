# from django.db import models
# from django.contrib.auth import get_user_model
# from django.contrib.contenttypes.models import ContentType#видит все модели, которые есть в проете
# from django.contrib.contenttypes.fields import GenericForeignKey
# from PIL import Image
# from django.urls import  reverse
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# import sys
#
# User = get_user_model()
#
# def get_models_for_count(*model_names):
#     return [models.Count(model_name) for model_name in model_names]
#
#
# def get_product_url(obj, viewname):
#     ct_model= obj.__class__.meta.model_name
#     return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})
#
# class MinResolutionErrorExeption(Exception):
#     pass
#
#
# class MaxResolutionErrorExeption(Exception):
#     pass
#
# #
# class LatestProductsManager:
#
#     @staticmethod
#     def get_products_for_main_page(*args, **kwargs):
#         with_respect_to = kwargs.get('with_respect_to')
#         products = []
#         ct_models = ContentType.objects.filter(model__in=args)
#         for ct_model in ct_models:
#             model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
#             products.extend(model_products)
#         # хотим вывести товары определенной модели
#         if with_respect_to:
#             ct_model = ContentType.objects.filter(model=with_respect_to)
#             if ct_model.exists():
#                 if with_respect_to in args:
#                     return sorted(
#                         products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
#                     )
#         return products
#
# #иметация модели, отвечает за вывод новинок
# class LatestProducts:
#
#     objects = LatestProductsManager()
#
#
# class CategoryManager(models.Manager):
#
#     CATEGORY_NAME_COUNT_NAME = {
#         'Ноутбуки': 'notebook__count',
#         'Смартфоны': 'smartphone__count'
#     }
#
#     def get_queryset(self):
#         return super().get_queryset()
#
#     def get_categories_for_left_sidebar(self):
#         models = get_models_for_count('notebook', 'smartphone')
#         qs = list(self.get_queryset().annotate(*models))
#         print(qs)
#         data = [
#             dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
#             for c in qs
#         ]
#         return data
#
#
# class Category(models.Model):
#
#     name=models.CharField(max_length=255, verbose_name='Имя категории')
#     slug=models.SlugField(unique=True) #конечная точка, чтобы получить объект модели(ноутбук)
#     objects=CategoryManager()
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('category_detail', kwargs={'slug': self.slug})
#
#
# # class Product(models.Model):
# #
# #     MIN_RESOLUTION=(400,400)
# #     MAX_RESOLUTION = (16000, 16000)
# #     MAX_IMAGE_SIZE = 3145728
# #
# #     class Meta:
# #         abstract=True
# #
# #     catecory = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)#удалить все связи
# #     title = models.CharField(max_length=255, verbose_name='Наименование')
# #     slug = models.SlugField(unique=True)
# #     image = models.ImageField(verbose_name='Изображение')
# #     discription = models.TextField(verbose_name='Описание', null=True)
# #     price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
# #
# #     def __str__(self):
# #         return self.title
# #
# #     def save(self, *args, **kwargs):
# #         image = self.image
# #         img = Image.open(image)
# #         min_height, min_width = self.MIN_RESOLUTION
# #         max_height, max_width = self.MAX_RESOLUTION
# #         if img.height < min_height or img.width < min_width:
# #             raise MinResolutionErrorExeption('Разрешение изображения меньше минимального!')
# #         if img.height > max_height or img.width > max_width:
# #             raise MaxResolutionErrorExeption('Разрешение изображения больще максимального!')
# #         # else:
# #         # new_img = img.convert('RGB')
# #         # resizes_new_img = new_img.resize((500,500), Image.ANTIALIAS)
# #         # filestream = BytesIO()
# #         # file = resizes_new_img.save(filestream, 'JPEG', quality=90)
# #         # filestream.seek(0)
# #         # name= '{}.{}'.format(*self.image.name.split('.'))
# #         # print(self.image.name)
# #         # self.image = InMemoryUploadedFile (filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None )
# #         # super().save(*args, **kwargs)
#
#
# class Product(models.Model):
#
#     class Meta:
#         abstract = True
#
#     catecory = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255, verbose_name='Наименование')
#     slug = models.SlugField(unique=True)
#     image = models.ImageField(verbose_name='Изображение')
#     discription = models.TextField(verbose_name='Описание', null=True)
#     price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
#
#     def __str__(self):
#         return self.title
#
#     def get_model_name(self):
#         return self.__class__.__name__.lower()
#
#
#
# class CartProduct(models.Model):
#
#     user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
#     cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()#идентификатор инстансе модели
#     # p=NotebookProduct.object.get(pk=1)
#     # cp= CertProduct.objects.create(content_object)
#     # после создания р content_type, object_id заполяются автоматически:
#     #content_type = NotebookProduct
#     #object_id = 1
#     content_object = GenericForeignKey('content_type', 'object_id')
#     qty = models.PositiveIntegerField(default=1)
#     final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
#
#     def __str__(self):
#         return 'Продукт:{} (для корзины)'.format(self.content_object.title)
#
#
# class Cart(models.Model):
#
#     owner = models.ForeignKey('Customer', verbose_name='', on_delete=models.CASCADE)
#     product = models.ManyToManyField(CartProduct, blank=True, related_name='releted_cart')
#     #cart.related_products.all()- получить все продукты в корзине
#     total_products = models.PositiveIntegerField(default=0)#для отображения вида товара
#     final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
#     in_order = models.BooleanField(default=False)#корзина уже готова
#     for_anonymous_user = models.BooleanField(default=False)#для анонимов
#
#     def __str__(self):
#         return str(self.id)
#
#
# class Customer(models.Model):
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, verbose_name='Номер телефона')
#     address = models.CharField(max_length=255, verbose_name='Адрес')
#
#     def __str__(self):
#         return 'Покупатель:{} {} (для корзины)'.format(self.user.first_name, self.user.last_name)
#
#
# class Notebook(Product):
#
#     diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
#     display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
#     processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
#     ram = models.CharField(max_length=255, verbose_name='Оперативная память')
#     video = models.CharField(max_length=255, verbose_name='Видеокарта')
#     time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')
#
#     def __str__(self):
#         return "{} : {}".format(self.category.name, self.title)
#
#     def get_absolute_url(self):
#         return get_product_url(self, 'product_detail')
#
#
#
# class Smartphone(Product):
#
#     diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
#     display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
#     resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
#     accume_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
#     ram = models.CharField(max_length=255, verbose_name='Оперативная память')
#     sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
#     sd_volume_max = models.CharField(
#         max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
#     )
#     main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
#     frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')
#
#     def __str__(self):
#         return "{} : {}".format(self.category.name, self.title)
#
#     def get_absolute_url(self):
#         return get_product_url(self, 'product_detail')
#
#
#


from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    class Meta:
        abstract = True

    catecory = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    discription = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    video = models.CharField(max_length=255, verbose_name='Видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='Время работы аккумулятора')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
    accume_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True, verbose_name='Наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Максимальный объем встраивамой памяти'
    )
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)