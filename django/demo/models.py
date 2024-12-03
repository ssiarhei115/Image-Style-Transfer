from django.db import models

# Create your models here.
# Create your models here.
class StyleModel(models.Model):
    styles = (
        ('anonymous_fuxi', 'anonymous_fuxi'),
        ('askim_andersson', 'askim_andersson'), 
        ('bcbey_han', 'bcbey_han'),
        ('darkspirit_ninakossman', 'darkspirit_ninakossman'),
        ('laluna_bajo', 'laluna_bajo'),
        ('lights_in_india', 'lights_in_india'),
        ('monsternavajo_sandd', 'monsternavajo_sandd'),
        ('pastorale_jansen', 'pastorale_jansen'),
        ('tegelveld_springendedieren', 'tegelveld_springendedieren'),
        ('tingatinga_daudi', 'tingatinga_daudi')
        )
    content = models.ImageField('Content image', upload_to = "media/images/%Y/%m/%d", blank=False)
    style_input = models.CharField('Style input', choices=(('my style', 'my style'), ('preloaded style','preloaded style')), max_length=15, default='preloaded style')
    style = models.ImageField('Style image', upload_to = "media/images/%Y/%m/%d", blank=True)
    mixed = models.ImageField('Mixed image', upload_to = "media/output/%Y/%m/%d", blank=True)
    strength = models.CharField('Style effect', choices=(('0.2', 'low'),('0.5', 'medium'), ('0.8', 'high')), max_length = 100, default='0.8')
    preloaded_styles = models.CharField('Preloaded styles', choices=styles, max_length = 100, default='tingatinga_daudi')    
    
    #def __str__(self):
    #    return self.name

class TestModel(models.Model):
    my_style = models.ImageField('Style_image', upload_to = "static/images/", blank=False, name='Style_image')
    style_choice = models.CharField(choices=(('anonymous_fuxi', 'anonymous_fuxi'),
        ('askim_andersson', 'askim_andersson'), 
        ('bcbey_han', 'bcbey_han'),
        ('darkspirit_ninakossman', 'darkspirit_ninakossman'),
        ('laluna_bajo', 'laluna_bajo'),
        ('lights_in_india', 'lights_in_india'),
        ('monsternavajo_sandd', 'monsternavajo_sandd'),
        ('pastorale_jansen', 'pastorale_jansen'),
        ('tegelveld_springendedieren', 'tegelveld_springendedieren'),
        ('tingatinga_daudi', 'tingatinga_daudi')), max_length = 100, default='0.5', name='Choose_style'
        )

#class SModel(models.Model):
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name