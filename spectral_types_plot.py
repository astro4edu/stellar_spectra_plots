import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import json
from astropy import units as u
from PIL import Image


from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm, ListedColormap


import matplotlib as mpl

from matplotlib import cm
from pathlib import Path
#from translations import translations_dicts
import sys


translations_path = Path(__file__).parent / "./translations.json"
translations_file = open(translations_path)
translations_dicts = json.load(translations_file)
translations_file.close()

if len(sys.argv)<2:
    need_language=True
else:
    if sys.argv[1] in translations_dicts.keys():
        language_code=sys.argv[1]
        need_language=False
    else:
        need_language=True
prompt_string="Available languages:"
for i0,key_tmp in enumerate(translations_dicts.keys()):
    if i0>0:
        prompt_string=prompt_string+', '
    prompt_string=prompt_string+key_tmp
prompt_string=prompt_string+'\nPlease enter a language code:'
while need_language:
    language_code=input(prompt_string)
    if language_code in  translations_dicts.keys():
        need_language=False
outfile_base = Path(__file__).parent / "./plots/"
data_file_path = Path(__file__).parent / "./data/mastar_example_spectral_types.fits"
#print(data_file_path)

lambda_min=365
lambda_max=900
lambda_red=700
lambda_blue=400
bounds_box=[0.1,0.9,0.1,0.9]
bounds_box_bands=[0.3,0.9,0.1,0.9]
bounds_box_bands_offset=0.13

text_list=translations_dicts['en_gb']
spectral_name_base='title'
spectral_title_base='spectrum_title'
class SpectralLineSet:
  def __init__(self, name,lines,linestyle):
    self.name = name
    self.lines=lines #each line value can be either a single line value or two values for a band
    self.linestyle=linestyle

all_balmer_lines=SpectralLineSet(text_list['balmer_text'],[656.279,486.135,434.0472,410.1734,397.0075,388.9064,383.5397],'dashed')
some_balmer_lines=SpectralLineSet(text_list['balmer_text'],[656.279,486.135,434.0472,410.1734],'dashed')
he_i_lines=SpectralLineSet(text_list['helium_atoms_text'],[396.4729,402.6191,412.0,414.3,438.7929,471.3146,492.1931,501.5678,587.56148,667.81517,706.51771],'dashdot')
he_ii_lines=SpectralLineSet(text_list['helium_ions_text'],[454.1,468.6],(0, (1, 10)))
ca_i_lines=SpectralLineSet(text_list['calcium_atoms_text'],[422.67,],(0, (3, 10, 1, 10)))
ca_ii_lines=SpectralLineSet(text_list['calcium_ions_text'],[393.36614,396.84673,849.8018,854.2089,866.2140],'dotted')
na_i_lines=SpectralLineSet(text_list['sodium_atoms_text'],[588.995 ,589.592,818.33,819.4], (0, (3, 1, 1, 1)))
tio_lines=SpectralLineSet(text_list['titanium_oxide_text'],[(617.0,629.0),(632.2,651.2),(656.9,685.2),(705.3,727),(766,786.1)], (0, (5, 1)))


#na_i_lines=SpectralLineSet(text_list[8],[588.995 ,589.592],(0, (3, 10, 1, 10)))


class MplColorHelper:

  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

  def get_rgb(self, val):
    return self.scalarMap.to_rgba(val)



COL1 = MplColorHelper('rainbow',lambda_blue,lambda_red)


mastarall = fits.open(data_file_path)
data_table=mastarall[1].data
image_list=[]
x_list=[]
y_list=[]
for index, row in enumerate(data_table):
    x_tmp=0.1*row['WAVE']
    y_tmp=row['FLUX']
    mask_tmp=row['MASK']
    subset=np.where((x_tmp>lambda_min)&(x_tmp<lambda_max)&(y_tmp>0.0)&(y_tmp<6.0*np.median(y_tmp))&(mask_tmp==0))
    x=x_tmp[subset]
    y=y_tmp[subset]
    x_list.append(x)
    y_list.append(y)
    spectral_features_to_plot=[]
    if row['show_all_balmer_lines']:
        spectral_features_to_plot.append(all_balmer_lines)
    if row['show_some_balmer_lines']:
        spectral_features_to_plot.append(some_balmer_lines)
    if row['show_he_i_lines']:
        spectral_features_to_plot.append(he_i_lines)
    if row['show_he_ii_lines']:
        spectral_features_to_plot.append(he_ii_lines)
    if row['show_ca_i_lines']:
        spectral_features_to_plot.append(ca_i_lines)
    if row['show_ca_ii_lines']:
        spectral_features_to_plot.append(ca_ii_lines)
    if row['show_na_i_lines']:
        spectral_features_to_plot.append(na_i_lines)
    if row['show_tio_lines']:
        spectral_features_to_plot.append(tio_lines)
    #print(min(y_tmp),max(y_tmp),np.median(y_tmp),max(y_tmp)/np.median(y_tmp))
    #spectrum = Spectrum1D(flux=y*u.Jy, spectral_axis=x*u.um)
    #g1_fit = fit_generic_continuum(spectrum)
    #y_fit = g1_fit(x*u.um)
    
    tmp_array=[]
    tmp_array2=[]
    tmp_array3=[]
    tmp_array4=[]
    tmp_array5=[]
    tmp_spec1=[]
    tmp_spec2=[]
    for i0 in range(lambda_min,lambda_max):
        index_tmp = np.argmin(np.abs(np.array(x)-i0))
            
        tmp_list1=[0.0,0.0,0.0,0.0]
        tmp_list2=[0,0,0,255]                     #black image for BG                 
        if i0>lambda_red:
            tmp_list=list(COL1.get_rgb(lambda_red))
            
        elif i0<lambda_blue:
            tmp_list=list(COL1.get_rgb(lambda_blue))
        else:
            tmp_list=list(COL1.get_rgb(i0))
        tmp_list1[0]=255*tmp_list[0]
        tmp_list1[1]=255*tmp_list[1]
        tmp_list1[2]=255*tmp_list[2]
        tmp_list1[3]=255*y[index_tmp]/np.median(y)
        tmp_spec1.append(tmp_list1)
        tmp_spec2.append(tmp_list2)

    for i0 in range(0,300):
        tmp_array.append(tmp_spec1)
        tmp_array2.append(tmp_spec2)

        
        
        
    tmp_array1=np.array(tmp_array).astype('uint8')
    tmp_array2=np.array(tmp_array2).astype('uint8')
    img_tmp = Image.fromarray(tmp_array1, mode='RGBA')
    img_tmp2 = Image.fromarray(tmp_array2, mode='RGBA')
    image_list.append((img_tmp,img_tmp2))
    #img_tmp.show()
    plt.rcParams['figure.figsize']= 15,8
    plt.rcParams.update({'font.size': 12})
    mpl.rcParams['axes.linewidth'] =1.0
    plt.rc('axes.spines', **{'bottom':True, 'left':True, 'right':False, 'top':False})
    fig, ax = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 3],'width_ratios': [1]})
    ax[0].set_title(text_list[spectral_name_base+str(index)],fontsize=30,pad=10)
    ax[0].imshow(img_tmp2,extent=bounds_box, aspect='auto')
    ax[0].imshow(img_tmp,extent=bounds_box, aspect='auto')
    ax[0].axis('off')
    ax[1].yaxis.set_ticklabels([])
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    norm =plt.Normalize(lambda_blue,lambda_red)
    linewidths=[1.0] * len(segments)
    lc = LineCollection(segments, cmap='rainbow', norm=norm,linewidths=linewidths)
    
    lc.set_array(x)
    lc.set_linewidth(3)
    line = ax[1].add_collection(lc)
    ax[1].set_xlabel(text_list['xaxis_text'],fontsize=20)
    ax[1].set_ylabel(text_list['yaxis_text'],fontsize=20)
    
    #fig.colorbar(line, ax=axs)
    

    #print(x.min(),x.max())
    ax[1].set_xlim(x.min(),x.max())
    ax[1].set_ylim(0.0, 1.1*y.max())
    for spectral_feature in spectral_features_to_plot:
        
        line_tmp1 = plt.Line2D((0.1,0.1),(0.1,0.1), color="k", linewidth=1,linestyle=spectral_feature.linestyle,label=spectral_feature.name)
        ax[1].add_artist(line_tmp1)
        for line_tmp in spectral_feature.lines:
            if type(line_tmp) is tuple:
                line_middle_x=[]
                line_middle_y=[]
                for line_component in line_tmp:
                    index_tmp = np.argmin(np.abs(np.array(x_tmp)-line_component))
                    try:
                        y_average=(max(y_tmp[index_tmp-20:index_tmp+20]))
                        additional_offset=0.0
                    except:
                        y_average=y_tmp[index_tmp]
                        additional_offset=0.1
                    line_x=(bounds_box[1]-1.24*bounds_box[0])*(line_component-lambda_min)/(lambda_max-lambda_min)+1.25*bounds_box[0]
                    line_middle_x.append(line_x)
                    line_y_min=bounds_box[2]+(bounds_box[3]-bounds_box[2]-0.2)*(y_average/(1.1*max(y_tmp)))+additional_offset
                    line_y_max=0.7
                    line_tmp1 = plt.Line2D((line_x,line_x),(line_y_max,line_y_min), color="k", linewidth=1,linestyle=spectral_feature.linestyle,label=spectral_feature.name)
                    fig.add_artist(line_tmp1)
                line_tmp1 = plt.Line2D((line_middle_x[0],line_middle_x[1]),(line_y_max,line_y_max), color="k", linewidth=1,linestyle=spectral_feature.linestyle,label=spectral_feature.name) 
                fig.add_artist(line_tmp1) 
            else:
                index_tmp = np.argmin(np.abs(np.array(x_tmp)-line_tmp))
                try:
                    y_average=(max(y_tmp[index_tmp-20:index_tmp+20]))
                    additional_offset=0.0
                except:
                    y_average=y_tmp[index_tmp]
                    additional_offset=0.1
                
                line_x=(bounds_box[1]-1.24*bounds_box[0])*(line_tmp-lambda_min)/(lambda_max-lambda_min)+1.25*bounds_box[0]
                line_y_min=bounds_box[2]+(bounds_box[3]-bounds_box[2]-0.2)*(y_average/(1.1*max(y_tmp)))+additional_offset
                line_y_max=0.7
                line_tmp1 = plt.Line2D((line_x,line_x),(line_y_max,line_y_min), color="k", linewidth=1,linestyle=spectral_feature.linestyle,label=spectral_feature.name)
            fig.add_artist(line_tmp1)
    ax[1].legend(loc=row['legend_location'],title=text_list['spectral_features_title'])
    ax[1].plot(x.max(),0, '>k',markersize=10, clip_on=False)
    ax[1].plot(x.min(), 1.1*y.max(), '^k',markersize=10, clip_on=False)
    plt.savefig(outfile_base.joinpath(text_list[spectral_name_base+str(index)].replace(' ','_')+'_spectrum_'+language_code+'.png'))
    plt.close()
    
    plt.figure()

fig_tmp, ax_tmp = plt.subplots(len(image_list),2,gridspec_kw={'width_ratios': [1, 15]})
fig_tmp.suptitle(text_list['bands_title'],fontsize=30)
plt.gcf().text(0.24, 0.08,text_list['lambda_lower'], fontsize=14,ha='center')
plt.gcf().text(0.9, 0.08,text_list['lambda_upper'], fontsize=14,ha='center')
for index,image_tuple in enumerate(image_list):
    ax_tmp[index,1].imshow(image_tuple[1],extent=bounds_box_bands, aspect='auto')
    ax_tmp[index,1].imshow(image_tuple[0],extent=bounds_box_bands, aspect='auto')
    ax_tmp[index,0].text(0.5,0.5,text_list[spectral_title_base+str(index)],ha='center',va='center',fontsize=20)
    ax_tmp[index,0].axis('off')
    ax_tmp[index,1].axis('off')
    
plt.savefig(outfile_base.joinpath('spectra_bands_'+language_code+'.png'))
plt.figure()
plt.rcParams['figure.figsize']= 15,8
plt.rcParams.update({'font.size': 12})
plt.rcParams['axes.linewidth'] =1.0
plt.rc('axes.spines', **{'bottom':True, 'left':True, 'right':False, 'top':False})
fig, ax = plt.subplots(1)
y_max=0
x_min=1e6
x_max=0
for ind in range(0,len(y_list)):
    x=x_list[ind]
    y=y_list[ind]
    y=y/max(y)
    y=[len(y_list)-ind-1.0+z for z in y]
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    norm =plt.Normalize(lambda_blue,lambda_red)
    linewidths=[1.0] * len(segments)
    lc = LineCollection(segments, cmap='rainbow', norm=norm,linewidths=linewidths)
    
    lc.set_array(x)
    lc.set_linewidth(3)
    line = ax.add_collection(lc)
    if min(x)<x_min:
        x_min=min(x)
    if max(x)>x_max:
        x_max=max(x)
    if max(y)>y_max:
        y_max=max(y)
    if ind<3:
        y_text_offset=0.3
    else:
        y_text_offset=0.3+0.2*(ind-2)
    ax.text(850.0,len(y_list)-ind-1.0+y_text_offset,text_list[spectral_title_base+str(ind)],fontsize=14)

ax.set_title(text_list['bands_title'],fontsize=30,pad=10)
ax.yaxis.set_ticklabels([])
#ax.legend(loc=row['legend_location'],title=text_list['spectral_features_title'])
ax.plot(x_max,0, '>k',markersize=10, clip_on=False)
ax.plot(x_min, 1.01*y_max, '^k',markersize=10, clip_on=False)
ax.set_xlabel(text_list['xaxis_text'],fontsize=20)
ax.set_ylabel(text_list['yaxis_text'],fontsize=20)
ax.set_xlim(x_min,x_max)
ax.set_ylim(0.0, 1.01*y_max)
plt.savefig(outfile_base.joinpath('spectra_plots_'+language_code+'.png'))
