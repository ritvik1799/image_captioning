#!/usr/bin/env python
# coding: utf-8

# In[8]:


from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from keras.layers import *
from keras.models import Model,load_model
from pickle import load


# In[24]:


def extract_feature(image):
  model_res = ResNet50(weights='imagenet',input_shape=(224,224,3))
  model_new = Model(model_res.input,model_res.layers[-2].output)



  img = load_img(image,target_size=(224,224))


  img = img_to_array(img)

  img = img.reshape(1,img.shape[0],img.shape[1],img.shape[2])
    # we can also use np.expand_dims(img,axis=0)

  img = preprocess_input(img)

  feature = model_new.predict(img)
    #since this will return 2d shape of [1,2048]
    #so we reshape it in 1d i.e 2048

  return feature


# In[5]:


word_to_index = load(open('./storage/word_to_index.pkl','rb'))
index_to_word = load(open('./storage/index_to_word.pkl','rb'))


# In[9]:


model = load_model("model_caption_38.h5")


# In[36]:


def predict_caption(photo):
    max_len = 33
    in_text = 'startseq'
    
    for i in range(max_len):
        sequence = [word_to_index[w] for w in in_text.split() if w in word_to_index]
        sequence = pad_sequences([sequence],maxlen = max_len,padding = 'post')
        
        y_pred = model.predict([photo,sequence])
        y_pred = y_pred.argmax()
        word = index_to_word[y_pred]
        
        in_text+= ' ' + word
        
        if word == 'endseq':
            break
    final_caption = in_text.split()[1:-1]
    final_caption = " ".join(final_caption)
    
    return final_caption


# In[40]:
def caption_this_image(image):
    enc = extract_feature(image)
    caption = predict_caption(enc)
    return caption


# In[ ]:




