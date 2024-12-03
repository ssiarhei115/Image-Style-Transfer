from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import *
import pandas as pd
import category_encoders as ce
import numpy as np
import pickle
#import tensorflow_hub as hub
import matplotlib.pyplot as plt
import tensorflow._api.v2.compat.v1 as tf
#import tensorflow as tf
#from utils.ais_with_weights import *
import io
import base64
from PIL import Image 


def to_data_uri(pil_img):
    data = io.BytesIO()
    pil_img.save(data, "JPEG") # pick your format
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8') 
  
def save_np_image(image):
    """ """
    image = np.uint8(image * 255.0)
    image = np.squeeze(image, 0)
    image = Image.fromarray(image, 'RGB')
    image_uri = to_data_uri(image)
    return image_uri

def mixer(content_path, style_path, strength):
    params = {
        'checkpoint': 'arbitrary_style_transfer/model.ckpt',
        'style_images_paths': style_path,
        'content_images_paths': '/home/sv/Documents/git/demopyt/ws/media' + content_path, 
        #'instance': obj, 
        'image_size': 256,
        'content_square_crop': False, 
        'style_image_size': 256,
        'style_square_crop': False,
        #'maximum_styles_to_evaluate': 1024,
        'interpolation_weights': f"[{strength}]",
        #'interpolation_weights': '[0.1, 0.4, 0.7]',
        }
    #console_entry_point(params)
    return params

premenu = ['home', 'contact', 'about']
menu = ['style_transfer', 'price_prediction', 'word_helper']
best_features = ['Гараж', 'Новостройка', 'Элитный коттедж', 'house_area', 'house_levels', 'in_city', 'distance_house_region_min',
       'distances_multiply', 'Материал стен_дерево', 'Материал стен_блок г/с', 'Материал стен_блок',
       'Материал крыши_шифер', 'Материал крыши_черепица мет.', 'Материал крыши_черепица мяг.', 'Отопление_печь',
       'Отопление_электрич.', 'Отопление_паровое г.', 'Канализация_местная', 'Канализация_нет',
       'Канализация_с/у наружн.', 'Канализация_центральн.', 'Вода_сезонная', 'Вода_водопровод', 'Вода_колодец',
       'Вода_рядом колодец', 'Газ_нет', 'Газ_есть', 'Ремонт_отделка дер.', 'Ремонт_евроотделка', 'Район_Брестский', 'Район_другой',
       'Район_Минский', 'year_group_2000+', 'Тип объекта_дача', 'Тип объекта_дом', 'Тип объекта_коттедж', 'Тип объекта_таунхаус',
       'Населенный пункт_другой', 'Населенный пункт_г Минск', 'Населенный пункт_г Брест']

def index(request):
    
    return render(request, 'demo/index.html', context={
            'menu':menu, 
            'premenu':premenu,
            'title':'ML DEMOs',
            'intro': 'Here you can find some examples of powerfull ML-algorithms',
            })

def prediction(request):

    if request.method == "POST":
        params = {
            #'name': request.POST.get("name", 'Unknown user'),
            #'mood': request.POST.get("mood", 'good'),

            'Гараж': 1 if request.POST.get("garage")=='on' else 0, 
            'new_build': 1 if request.POST.get("new_build")=='on' else 0, 
            'Элитный коттедж': 1 if request.POST.get("elite_cottage")=='on' else 0,
            'in_city': 1 if request.POST.get("elite_cottage")=='on' else 0, 
            'house_area': request.POST.get("house_area"), 
            'house_levels': request.POST.get("house_levels"), 
            'distance_house_district_city': float(request.POST.get("distance_house_district_city")),  
            'distance_house_region_min': float(request.POST.get("distance_house_region_min")), 
            'distance_house_minsk': float(request.POST.get("distance_house_minsk")), 
            'Материал стен': request.POST.get("walls"), 
            'Материал крыши': request.POST.get("roof"), 
            'Отопление': request.POST.get("heating"), 
            'Канализация': request.POST.get("sewerage"), 
            'Вода': request.POST.get("water"), 
            'Район': request.POST.get("district"), 
            'Газ': request.POST.get("gas"), 
            'Ремонт': request.POST.get("repair"),
            'year_group': request.POST.get("year_group"),
            'Тип объекта': request.POST.get("house_type"),
            'Населенный пункт': request.POST.get("city"),            
        }
        params['distances_multiply'] = params["distance_house_district_city"]*params["distance_house_region_min"]*params["distance_house_minsk"]
        user_df = pd.DataFrame(params, index=['user'])
        user_df.to_csv('user_data.csv')
        user_df = pd.read_csv('user_data.csv', index_col=0)

        ohe_list = ['Материал стен', 'Материал крыши', 'Отопление', 'Канализация', 'Вода','Газ',  'Ремонт', 'Район','year_group', 'Тип объекта', 'Населенный пункт']
        encoder = ce.OneHotEncoder(cols=ohe_list, use_cat_names=True)
        add = encoder.fit_transform(user_df.loc[:,ohe_list])
        user_df = pd.concat([user_df,add], axis=1)#.drop(ohe_list, axis=1)

        default_dict = {i:0 for i in best_features}
        for col in user_df.columns:
            if col not in default_dict.keys():
                user_df = user_df.drop([col], axis=1)
        
        concat_df =pd.concat([pd.DataFrame(default_dict, index=['default']), user_df], axis=0).fillna(0)
        concat_df.loc['result', :] = concat_df.sum()

        with open('demo/model37.pkl', 'rb') as pkl_file:
            model = pickle.load(pkl_file)

        predict = round(model.predict(concat_df.loc['result', best_features].values.reshape(1,-1))[0],1)
        
        return render(request, 'demo/predict.html', context={
            'params':params, 
            'menu':menu, 
            'premenu': premenu,
            'title':'CountryHouse Price Predictor',
            'params_entered': 'PARAMETERS ENTERED:',
            'prediction_text': 'PRICE PREDICTED:',
            'predict':predict})
    else:
        params = {
            'title': "Predict a price for your house",
            'menu': menu,
            'premenu': premenu,
            'form': UserForm(),
            'submit_button': "<input type='submit' value='Submit' />",
            'params_enter': 'Choose your house parameters',
        }
        return render(request, "demo/predict.html", context=params)


def stylize(request):
    """"""
    with tf.device('/cpu:0'):
        model = tf.keras.models.load_model('demo/model/')
    if request.method == "POST":
        form = StyleForm(request.POST, request.FILES)
        
        if form.is_valid():
            content = form.cleaned_data.get("content")
            strength = form.cleaned_data.get("strength")
            style_input = form.cleaned_data.get("style_input")
            preloaded_style = form.cleaned_data.get("preloaded_styles")
            #obj = StyleModel.objects.create(content = content, style = style, strength = strength)
            #obj.save()
            #print(obj, "uploaded successfuly")
            if style_input=='my style':
                style = form.cleaned_data.get("style")
    
                
                try:
                    obj = StyleModel.objects.create(content = content, style = style)
                    obj.save()
                    #mixed_uri, content_prep, style_prep = main(mixer(obj.content.url, '/home/sv/Documents/git/demopyt/ws/media'+obj.style.url, strength))
                    #content = plt.imread('/home/sv/Documents/git/demopyt/ws/media' + obj.content.url)
                    #style = plt.imread('/home/sv/Documents/git/demopyt/ws/media' + obj.style.url)
                    content = plt.imread('media' + obj.content.url)
                    style = plt.imread('media' + obj.style.url)
                    content = content.astype(np.float32)[np.newaxis, ...] / 255
                    content = tf.image.resize(content, (512, 512))
                    style = style.astype(np.float32)[np.newaxis, ...] / 255
                    style = tf.image.resize(style, (256, 256))
                    outputs = model(tf.constant(content), tf.constant(style))
                    mixed = outputs[0]
                    content_uri = save_np_image(content)
                    style_uri = save_np_image(style)
                    mixed_uri = save_np_image(mixed)
                
                    context = {
                            'menu' : menu,
                            'premenu': premenu,
                            'form' : StyleForm(),
                            'title' : "Make a magic with your picture",
                            'submit_button': "<button type='submit'>Transfer style</button>",#"<input type='submit' value='Submit' />",
                            'content' : content_uri,#obj.content.url,
                            'style' : style_uri,#obj.style.url,
                            'content_inp' : ('CONTENT: ' + obj.content.url.split('/')[-1][:20]),
                            'style_inp' : '  STYLE: ' + obj.style.url.split('/')[-1][:20],
                            'mixed_image': mixed_uri, #mixed[0][1:],
                            'style_transfer_result': "Style transfer result:",
                            'plus' : '+',
                            'your_input ': 'Your input:'
                            }

                    return render(request, "demo/stylize.html", context)
                except:
                    context = {
                        'menu' : menu,
                        'premenu': premenu,
                        'form' : StyleForm(),
                        'title' : "Make a magic with your picture",
                        'style_transfer_result': "<span style='color:red; font-family:Courier New, monospace;'>Upload your style image!</span>",
                        'submit_button': "<button type='submit'>Transfer style</button>"#"<input type='submit' value='Submit' />"
                        }
                    return render(request, "demo/stylize.html", context)
            else:
                obj = StyleModel.objects.create(content = content)
                obj.save()
                #mixed_uri, content_prep, style_prep = main(mixer(obj.content.url, 'static/style_images/' + preloaded_style +'.jpg', strength))
                #mixed, contentt, stylee = main(mixer(obj.content.url, 'static/style_images/' + preloaded_style +'.jpg', strength))
                #content = plt.imread('/home/sv/Documents/git/demopyt/ws/media' + obj.content.url)
                content = plt.imread('media' + obj.content.url)
                style = plt.imread('static/style_images/' + preloaded_style +'.jpg')
                content = content.astype(np.float32)[np.newaxis, ...] / 255
                content = tf.image.resize(content, (512, 512))
                style = style.astype(np.float32)[np.newaxis, ...] / 255
                style = tf.image.resize(style, (256, 256))
                outputs = model(tf.constant(content), tf.constant(style))
                mixed = outputs[0]
                content_uri = save_np_image(content)
                style_uri = save_np_image(style)
                mixed_uri = save_np_image(mixed)
                
                context = {
                            'menu' : menu,
                            'premenu': premenu,
                            'form' : StyleForm(),
                            'title' : "Make a magic with your picture",
                            'submit_button': "<button type='submit'>Transfer style</button>",#"<input type='submit' value='Submit' />",
                            'content' : content_uri,#obj.content.url,
                            'style' : style_uri,#'/static/style_images/' + preloaded_style +'.jpg',
                            'content_inp' : ('CONTENT: ' + obj.content.url.split('/')[-1][:20]),
                            'style_inp' : '  STYLE: ' + preloaded_style.split('.')[0][:20],
                            'mixed_image': mixed_uri,
                            'style_transfer_result': "Style transfer result:",
                            'plus' : '+',
                            'your_input': 'Your input:'
                            }

                return render(request, "demo/stylize.html", context)
            
    
    else:
        context = {
            'menu' : menu,
            'premenu': premenu,
            'form' : StyleForm(),
            'title' : "Make a magic with your picture",
            'style_transfer_result': "<span style='color:blue; font-family:Courier New, monospace;'>Choose images!</span>",
            'submit_button': "<button type='submit'>Transfer style</button>"#"<input type='submit' value='Submit' />"
        }
                
        return render(request, "demo/stylize.html", context)

def about(request):
    params = {
        'title': 'ABOUT',
        'menu': menu,
        'premenu': premenu
        }
    return render(request, 'demo/about.html', context=params)


def postuser(request):
    params = {
        'title': 'Request result',
        'menu': menu,
        'name': request.POST.get("name", 'Unknown user'),
        'mood': request.POST.get("mood", 'good'),
        'water': request.POST.getlist("water", 'колодец'),
    }
    return render(request, 'price/postuser.html', context=params)


def categories(request, cat_id):
    if cat_id > 100:
        #raise Http404()
        uri = reverse('catslug', args=('music',))
        return redirect(uri) #302, permanent=True - 301, redirect('home'), redirect('') 
    return HttpResponse(f'<h3>Categories</h3><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h3>Categories</h3><p>slug: {cat_slug}')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h3>s/th wrong. can't find the page</h3>")

def word(request):
    params = {
            'menu': menu,
            'premenu': premenu,
            }
    return render(request, 'demo/wordhelp.html', context=params)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    params = {
            'menu': menu,
            'premenu': premenu,
            'form': form
            }
    return render(request, 'demo/contact.html', context=params)

def contact_success(request):
    params = {
            'menu': menu,
            'premenu': premenu,
            }
    return render(request, 'demo/success.html', context=params)