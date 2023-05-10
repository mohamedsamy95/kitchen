'''
Written by Samy <m.elsisi1995@gmail.com> on Wed 09.05.2023
Version 1.0
'''
from django.db import models
from utils.basemodels import BaseModel
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Recipe(BaseModel):
    recipe_name = models.CharField(
        max_length=200, 
        db_index=True, 
        verbose_name=_('Recipe name'),
        help_text=_('Description of recipe')
    )
    ingredients = models.JSONField()
    instructions = models.TextField(
        verbose_name=_('Instructions'),
        help_text=_('Instructions to cook recipe')
        )
    label = models.CharField(max_length=30, blank=True, null=True)
    created_by = models.ForeignKey(
        to='auth.User', 
        on_delete=models.CASCADE,
        related_name='recipes', 
        verbose_name=_('Created by')
        )

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
    
    def __str__(self) -> str:
        return self.recipe_name



