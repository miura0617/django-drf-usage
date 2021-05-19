from django.db import models

# Create your models here.

class ItemCategoryModel(models.Model):
    item_category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.item_category_name
    
class ItemModel(models.Model):
    item_name = models.CharField(max_length=255)
    item_category_id = models.ForeignKey(
        ItemCategoryModel,
        on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name
    


