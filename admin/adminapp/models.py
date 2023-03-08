from django.db import models

# Create your models here.


class User(models.Model):
    full_name = models.CharField(verbose_name="Ism", max_length=100)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True, blank=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    latitude = models.CharField(max_length=30, null=True, blank=True)
    longitude = models.CharField(max_length=30, null=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True, blank=True)
    bool = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.telegram_id} - {self.full_name}"


class Product(models.Model):
    STATUS = [
        ("300 gr", "300 gr"),
        ("600 gr", "600 gr"),
        ("1 kg", "1 kg"),
    ]
    Name = [
        ("Qoy", "Qoy"),
        ("Mol", "Mol"),
        ("Ot", "Ot"),
        ("Tovuq", "Tovuq"),
        ("Kalbasa", "Kalbasa"),
        ("Tushonka", "Tushonka"),
    ]
    Category = [
        ("🐑Qo\'y go\'sht mahsulotlari", "🐑Qo\'y go\'sht mahsulotlari"),
        ("🐄Mol go\'sht mahsulotlari", "🐄Mol go\'sht mahsulotlari"),
        ("🐴Ot go\'sht mahsulotlari", "🐴Ot go\'sht mahsulotlari"),
        ("🐓Tovuq go\'sht mahsulotlari", "🐓Tovuq go\'sht mahsulotlari"),
        ("🍖Kalbasa mahsulotlari", "🍖Kalbasa mahsulotlari"),
        ("🥩Tushonka", "🥩Tushonka"),

    ]
    Subcategory = [
        ("DUDLANGAN_KURKA", "DUDLANGAN_KURKA"),
        ("TOVUQ_TANDIR_RULET", "TOVUQ_TANDIR_RULET"),
        ("DUDLANGAN_TOVUQ", "DUDLANGAN_TOVUQ"),
        ("MOL_QOY_RULET", "MOL_QOY_RULET"),
        ("QOY_TOSH_RULET", "QOY_TOSH_RULET"),
        ("QOY_TANDIR_RULET", "QOY_TANDIR_RULET"),
        ("QAZI", "QAZI"),
        ("OT_BOYIN_RULET", "OT_BOYIN_RULET"),
        ("OT_KACHALKA_RULET", "OT_KACHALKA_RULET"),
        ("TOY_TARASH_RULET", "TOY_TARASH_RULET"),
        ("QARTA_GOSHTLI", "QARTA_GOSHTLI"),
        ("QARTA", "QARTA"),
        ("MOL_TIL_RULET", "MOL_TIL_RULET"),
        ("MOL_PRESS", "MOL_PRESS"),
        ("MOL_ARCHA_RULET", "MOL_ARCHA_RULET"),
        ("MOL_RULET", "MOL_RULET"),
        ("MOL_TARASH_RULET", "MOL_TARASH_RULET"),
        ("MOL_TOVUQ_PRESS", "MOL_TOVUQ_PRESS"),
        ("DUDLANGAN_KOLBASA", "DUDLANGAN_KOLBASA"),
        ("QAYNATMA_KOLBASA", "QAYNATMA_KOLBASA"),
        ("SOSISKA", "SOSISKA"),
        ("OXOTNICHI_SOSISKA", "OXOTNICHI_SOSISKA"),
        ("MOL_TIL_TUSHONKA", "MOL_TIL_TUSHONKA"),
        ("MOL_TUSHONKA", "MOL_TUSHONKA"),
        ("QOY_TIL_TUSHONKA", "QOY_TIL_TUSHONKA"),
        ("QUYON_TUSHONKA", "QUYON_TUSHONKA"),
    ]
    category_code = models.CharField(
        max_length=30,
        choices=Name,
    )
    category_name = models.CharField(
        choices=Category,
        max_length=50,
    )
    subcategory_code = models.CharField(
        max_length=50,
        choices=Subcategory
    )
    subcategory_name = models.CharField(verbose_name="Mahsulot nomi", max_length=50)
    photo = models.ImageField(blank=True, upload_to='product_images')
    price = models.IntegerField()
    description = models.TextField(verbose_name="Mahsulot haqida", max_length=3000, null=True)
    weight = models.CharField(
        choices=STATUS,
        max_length=50,
    )

    def __str__(self):
        return self.category_code + self.weight


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    create_dt = models.DateTimeField(auto_now_add=True)
    type = models.BooleanField(default=False)

    def __str__(self):
        return self.product + self.count