import numpy as np
import astropy.io.fits as fits
from astropy import units as u
from PIL import Image
import arabic_reshaper
from bidi.algorithm import get_display
import json
from pathlib import Path
from glob import glob
from slugify import slugify

#from translations import translations_dicts
import argparse


class MplColorHelper:

  def __init__(self, cmap_name, start_val, stop_val):
    self.cmap_name = cmap_name
    self.cmap = plt.get_cmap(cmap_name)
    self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
    self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

  def get_rgb(self, val):
    return self.scalarMap.to_rgba(val)

class SpectralLineSet:
  def __init__(self, name,lines,linestyle):
    self.name = name
    self.lines=lines #each line value can be either a single line value or two values (min and max) for a band
    self.linestyle=linestyle #a tuple containing linestyle parameters

def font_loader(possible_fonts):
    usable_fonts=[]
    #find any fonts in the font folder of package and load them
    packaged_fonts_path = Path(__file__).parent / 'fonts/*ttf'
    packaged_font_files=glob(str(packaged_fonts_path))
    for font_file in packaged_font_files:
        font_manager.fontManager.addfont(font_file)
    loaded_font_list=[f.name for f in font_manager.fontManager.ttflist]
    #loop over fonts for the required script and add any that are available to the list of fonts to pass to matplotlib
    for font in possible_fonts:
        if font in loaded_font_list:
            usable_fonts.append(font)
    if "Arial Unicode" in loaded_font_list:
        usable_fonts.append("Arial Unicode") #add Arial Unicode font as backup
    if "DejaVu Sans" in loaded_font_list:
        usable_fonts.append("DejaVu Sans") #add default matplotlib font as backup
    plt.rcParams['font.family']=usable_fonts #pass fonts to matplotlib
    
#Begin argument parsing
parser = argparse.ArgumentParser(description='Make spectrum plots of stars')

parser.add_argument('--lang', help='add language code')
parser.add_argument('--text-direction', help='add the text direction, ltr=left to right or rtl=right to left, default is ltr')
parser.add_argument('--plot_dir', help='add directory for output plots. Default is plots directory in this package.')
parser.add_argument('--translations_file', help='add the JSON file containing translations. Default is translations/translations.json in this package.')
parser.add_argument('--output_format', help='add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba, svg, svgz, tif, tiff. Default is png.',default='png')
parser.add_argument('--translate_filenames', help='If True output filenames will be in requested language. If False output filenames will be in English. Default is False',default=False)

args = parser.parse_args()

if not args.translations_file:
    translations_path = Path(__file__).parent / "./translations/translations.json"
else:
    translations_path = Path(args.translations_file)
translations_file = open(translations_path)
translations_dicts = json.load(translations_file)
translations_file.close()

if not args.lang:
    need_language=True
else:
    if args.lang in translations_dicts.keys():
        language_code=args.lang
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

if not args.plot_dir:
    outfile_base = Path(__file__).parent / "./plots/"
else:
    outfile_base = Path(args.plot_dir)
data_file_path = Path(__file__).parent / "./data/mastar_example_spectral_types.fits"

#end argument parsing
#load translation file
text_list=translations_dicts[language_code]
possible_fonts=text_list['possible_fonts']


#important that arabic reshaper comes before bidi get_display
if language_code.startswith('ar'):
    text_list = {key:(arabic_reshaper.reshape(value) if type(value)==str else value) for key, value in text_list.items()}


text_list = {key:(get_display(value) if type(value)==str else value) for key, value in text_list.items()}

#check is cairo is required and load matplotlib
if text_list["matplotlib_cairo"]:
    import mplcairo
import matplotlib as mpl
if text_list["matplotlib_cairo"]:
    mpl.use("module://mplcairo.qt")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib import font_manager
from matplotlib import cm
    
text_list_en=translations_dicts['en']
font_loader(possible_fonts)

        
#setup spectra plot definitions
lambda_min=365
lambda_max=900
lambda_red=650
lambda_blue=450
bounds_box=[0.1,0.9,0.1,0.9]
bounds_box_bands=[0.3,0.9,0.1,0.9]
bounds_box_bands_offset=0.13
#next two lines are the start of a few different keys in the translation files
spectral_name_base='title'
spectral_title_base='spectrum_title'

#define spectral lines and bands
all_balmer_lines=SpectralLineSet(text_list['balmer_text'],[656.279,486.135,434.0472,410.1734,397.0075,388.9064,383.5397],'dashed')
some_balmer_lines=SpectralLineSet(text_list['balmer_text'],[656.279,486.135,434.0472,410.1734],'dashed')
he_i_lines=SpectralLineSet(text_list['helium_atoms_text'],[402.6191,414.4,438.7929,447.1,454.1,471.3146,492.1931,501.5678,587.56148,667.81517,706.51771],'dashdot')
he_ii_lines=SpectralLineSet(text_list['helium_ions_text'],[420.0,454.1,468.6],(0, (1, 10)))
ca_i_lines=SpectralLineSet(text_list['calcium_atoms_text'],[422.67,],(0, (3, 10, 1, 10)))
ca_ii_lines=SpectralLineSet(text_list['calcium_ions_text'],[393.36614,396.84673,849.8018,854.2089,866.2140],'dotted')
some_na_i_lines=SpectralLineSet(text_list['sodium_atoms_text'],[588.995 ,589.592], (0, (3, 1, 1, 1)))
more_na_i_lines=SpectralLineSet(text_list['sodium_atoms_text'],[588.995 ,589.592,818.33,819.4], (0, (3, 1, 1, 1)))
fe_i_lines=SpectralLineSet(text_list['iron_atoms_text'],[404.6,438.3,492.1,846.8,868.8],(0, (3, 5, 1, 5, 1, 5)))
tio_lines=SpectralLineSet(text_list['titanium_oxide_text'],[(617.0,629.0),(632.2,651.2),(656.9,685.2),(705.3,727),(766,786.1)], (0, (5, 1))) #note as TiO has broad bands it is a list of tuples with min and max wavelength

#make colour map
COL1 = MplColorHelper('rainbow',lambda_blue,lambda_red)

#load SDSS spectra
mastarall = fits.open(data_file_path)
data_table=mastarall[1].data
image_list=[]
x_list=[]
y_list=[]
for row in data_table:
    index=row['spectrum_selection'] #0=O, 1=B, 2=A, 3=F, 4=G, 5=K, 6
    x_tmp=0.1*row['WAVE'] #A->nm
    y_tmp=row['FLUX']
    mask_tmp=row['MASK']
    subset=np.where((x_tmp>lambda_min)&(x_tmp<lambda_max)&(y_tmp>0.0)&(y_tmp<6.0*np.median(y_tmp))&(mask_tmp==0))
    x=x_tmp[subset]
    y=y_tmp[subset]
    x_list.append(x)
    y_list.append(y)
    #next few lines read in columns in the data file to determine which spectral features to plot
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
    if row['show_some_na_i_lines']:
        spectral_features_to_plot.append(some_na_i_lines)
    if row['show_more_na_i_lines']:
        spectral_features_to_plot.append(more_na_i_lines)
    if row['show_fe_i_lines']:
        spectral_features_to_plot.append(fe_i_lines)
    if row['show_tio_lines']:
        spectral_features_to_plot.append(tio_lines)

    #print(min(y_tmp),max(y_tmp),np.median(y_tmp),max(y_tmp)/np.median(y_tmp))
    #spectrum = Spectrum1D(flux=y*u.Jy, spectral_axis=x*u.um)
    #g1_fit = fit_generic_continuum(spectrum)
    #y_fit = g1_fit(x*u.um)

    #Define a bunch of arrays for images & spectra etc
    tmp_array=[]
    tmp_array2=[]  #this will hold a black image for the background of the spectral bands plot
    tmp_spec1=[]
    tmp_spec2=[]  #black images for BG
    #step through wavelengths
    for i0 in range(lambda_min,lambda_max):
        index_tmp = np.argmin(np.abs(np.array(x)-i0)) #find nearest point on the spectrum
            
        tmp_list1=[0.0,0.0,0.0,0.0]
        tmp_list2=[0,0,0,255]                     #black image for BG

        #get the RGB(A) colours for that olour on the spectrum 
        if i0>lambda_red:
            tmp_list=list(COL1.get_rgb(lambda_red)) #if redder than lower limit of red light
            
        elif i0<lambda_blue:
            tmp_list=list(COL1.get_rgb(lambda_blue))  #if bluer than upper limit of blue light make it blue
        else:
            tmp_list=list(COL1.get_rgb(i0))
        #RGB values for this wavelength 
        tmp_list1[0]=255*tmp_list[0]
        tmp_list1[1]=255*tmp_list[1]
        tmp_list1[2]=255*tmp_list[2]
        #set the alpha channel (transparency) to be the flux at this wavelength divided by the maximum flux
        tmp_list1[3]=255*y[index_tmp]/y.max()
        #append this wavelength to the list of spectra
        tmp_spec1.append(tmp_list1)
        tmp_spec2.append(tmp_list2)
        #this is a hack to take into account the half pixel offset between image and the graph
        if i0!=lambda_min:
            tmp_spec1.append(tmp_list1)
            tmp_spec2.append(tmp_list2)
    #make 300px thick spectra bands
    for i0 in range(0,300):
        tmp_array.append(tmp_spec1)
        tmp_array2.append(tmp_spec2)
    
    #turn arrays into images
    tmp_array1=np.array(tmp_array).astype('uint8')
    tmp_array2=np.array(tmp_array2).astype('uint8')
    img_tmp = Image.fromarray(tmp_array1, mode='RGBA')
    img_tmp2 = Image.fromarray(tmp_array2, mode='RGBA')
    image_list.append((img_tmp,img_tmp2))
    #make the plot of the individual spectral type
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
    linewidths=[0.5] * len(segments)
    lc = LineCollection(segments, cmap='rainbow', norm=norm,linewidths=linewidths)
    
    lc.set_array(x)
    lc.set_linewidth(3)
    line = ax[1].add_collection(lc)
    ax[1].set_xlabel(text_list['xaxis_text'],fontsize=20)
    ax[1].set_ylabel(text_list['yaxis_text'],fontsize=20)
    
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
                    line_tmp1 = plt.Line2D((line_x,line_x),(line_y_max,line_y_min), color="k", linewidth=2,linestyle=spectral_feature.linestyle,label=spectral_feature.name)
                    fig.add_artist(line_tmp1)
                line_tmp1 = plt.Line2D((line_middle_x[0],line_middle_x[1]),(line_y_max,line_y_max), color="k", linewidth=2,linestyle=spectral_feature.linestyle,label=spectral_feature.name) 
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
                line_tmp1 = plt.Line2D((line_x,line_x),(line_y_max,line_y_min), color="k", linewidth=2,linestyle=spectral_feature.linestyle,label=spectral_feature.name)
            fig.add_artist(line_tmp1)
    legend_tmp=ax[1].legend(loc=row['legend_location'],title=text_list['spectral_features_title'], handlelength=5)
    leg_lines = legend_tmp.get_lines()
    plt.setp(leg_lines, linewidth=2)
    #add arrowheads to axes
    ax[1].plot(x.max(),0, '>k',markersize=10, clip_on=False)
    ax[1].plot(x.min(), 1.1*y.max(), '^k',markersize=10, clip_on=False)
    if args.translate_filenames:
        filename_tmp=slugify(text_list[spectral_name_base+str(index)])+'_'+language_code
    else:
        filename_tmp=slugify(text_list_en[spectral_name_base+str(index)])+'_'+language_code
    print("Saving: ",text_list_en[spectral_name_base+str(index)]+'\nTo: '+str(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format))))
    plt.savefig(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format)))
    
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



if args.translate_filenames:
    filename_tmp=slugify(text_list['bands_filename'])+'_'+language_code
else:
    filename_tmp=slugify(text_list_en['bands_filename'])+'_'+language_code

print("Saving: ",text_list_en['bands_title']+' - '+text_list_en['bands_filename']+'\nTo: '+str(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format))))
plt.savefig(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format)))
plt.close()
plt.figure()
plt.rcParams['figure.figsize']= 15,8
plt.rcParams.update({'font.size': 12})
plt.rcParams['axes.linewidth'] =1.0
plt.rc('axes.spines', **{'bottom':True, 'left':True, 'right':False, 'top':False})
fig, ax = plt.subplots(1)
#there min and max values are set in the next loop to define the upper and lower limits for the plots
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
    lc.set_linewidth(1)
    line = ax.add_collection(lc)
    if min(x)<x_min:
        x_min=min(x)
    if max(x)>x_max:
        x_max=max(x)
    if max(y)>y_max:
        y_max=max(y)
    #The y offsets were found by trial and error
    if ind<3:
        y_text_offset=0.3
    else:
        y_text_offset=0.3+0.2*(ind-2)
    ax.text(850.0,len(y_list)-ind-1.0+y_text_offset,text_list[spectral_title_base+str(ind)],fontsize=14)

ax.set_title(text_list['bands_title'],fontsize=30,pad=10)
ax.yaxis.set_ticklabels([])
#add arrowheads to axes
ax.plot(x_max,0, '>k',markersize=10, clip_on=False)
ax.plot(x_min, 1.01*y_max, '^k',markersize=10, clip_on=False)
ax.set_xlabel(text_list['xaxis_text'],fontsize=20)
ax.set_ylabel(text_list['yaxis_text'],fontsize=20)
ax.set_xlim(x_min,x_max)
ax.set_ylim(0.0, 1.01*y_max)



if args.translate_filenames:
    filename_tmp=slugify(text_list['lines_filename'])+'_'+language_code
else:
    filename_tmp=slugify(text_list_en['lines_filename'])+'_'+language_code
    
print("Saving: ",text_list_en['bands_title']+' - '+text_list_en['lines_filename']+'\nTo: '+str(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format))))
plt.savefig(outfile_base.joinpath(filename_tmp+'.'+str.lower(args.output_format)))
plt.close()
