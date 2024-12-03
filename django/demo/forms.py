from django import forms
from .models import StyleModel, TestModel, Contact
from django.utils.safestring import mark_safe



class UserForm(forms.Form):
    #name = forms.CharField(label='Name', required=True)
    #mood = forms.ChoiceField(label='Mood',choices=(('good','good'),('bad','bad'),('excellent','excellent'),('fed up with work','fed up with work'),('exhausted','exhausted')))
    
    house_type = forms.ChoiceField(choices=(('дача','дача'),('дом','дом'),('коттедж','коттедж'),('таунхаус','таунхаус')))
    house_area = forms.FloatField(label='House area', required=True, max_value=200, min_value=1)
 
    house_levels = forms.ChoiceField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),))

    water = forms.ChoiceField(choices=(('сезонная','сезонная'),('водопровод','водопровод'),('колодец','колодец'),('рядом колодец','рядом колодец'),))
    walls = forms.ChoiceField(choices=(('дерево','дерево'),('кирпич','кирпич'),('блок г/с','блок г/с'),('блок','блок'),('брус клеен.','брус клеен.'),('каркасн. монол.','каркасн. монол.')))    
    roof = forms.ChoiceField(choices=(('шифер','шифер'),('черепица мет.','черепица мет.'),('ондулин','ондулин'),('черепица мяг.','черепица мяг.'),
                                      ('черепица','черепица')))
    heating = forms.ChoiceField(choices=(('нет','нет'),('паровое г.','паровое г.'),('паровое т.','паровое т.'),('печь','печь'),('электрич.','электрич.')))
    sewerage = forms.ChoiceField(choices=(('нет','нет'),('местная','местная'),('с/у наружн.','с/у наружн.'),('центральн.','центральн.')))
    #electricity = forms.ChoiceField(choices=(('нет','нет'),('есть','есть')))
    gas = forms.ChoiceField(choices=(('нет','нет'),('есть','есть')))
    repair = forms.ChoiceField(choices=(('нет','нет'),('евроотделка','евроотделка'),('отделка дер.','отделка дер.')))
    district = forms.ChoiceField(choices=(('Минский','Минский'), ('Брестский','Брестский'),('другой','другой')))
    year_group = forms.ChoiceField(choices=(('2000+','2000+'),('другой','другой')))
    city = forms.ChoiceField(choices=(('г Минск','г Минск'), ('г Брест','г Брест'),('другой','другой')),label='Locality',)
       
    garage = forms.BooleanField(required=False)
    elite_cottage = forms.BooleanField(required=False)
    new_build = forms.BooleanField(required=False)
    in_city = forms.BooleanField(required=False)
    distance_house_district_city = forms.FloatField(label='To district city, km', required=True, max_value=80, min_value=0)
    distance_house_region_min = forms.FloatField(label='To region city, km', required=True, max_value=210, min_value=0)
    distance_house_minsk = forms.FloatField(label='To Minsk, km', required=True, max_value=380, min_value=0)
    #garden = forms.BooleanField(required=False)
    #outbuildings = forms.BooleanField(required=False)
    #forrest_near = forms.BooleanField(required=False)
    #swimming_pool = forms.BooleanField(required=False)
    
#class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=100)
#   file = forms.FileField()

class StyleForm(forms.ModelForm):
#class StyleForm(forms.Form):
    #style_radio = forms.ChoiceField(widget=forms.RadioSelect(choices=('1','2')),label="") 
    class Meta:
        model = StyleModel
        widgets = {'style_input': forms.RadioSelect(attrs={'class': 'form-check-inline', 'id': 'radio'})}
        fields = ['content', 'style', 'preloaded_styles', 'style_input'] #"__all__"
        #fields = "__all__"
        
#    content = forms.ImageField('Content_image', upload_to = "static/images/", blank=False)
#    style = forms.ImageField('Style_image', upload_to = "static/images/", blank=False)
#   strength = forms.CharField(choices=(('1','1'),('2','2'), ('3', '3')), widget=forms.RadioSelect())

class TestForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = "__all__"
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']