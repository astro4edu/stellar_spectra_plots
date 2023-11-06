## What this repository does	
This repository creates a series of plots of stellar spectra in multiple languages. 

## How to create plots using this repository
The command to run code from this repository is:
`python3 spectral_types_plot.py`
The following command line options are available:
```-h, --help            show this help message and exit
  --lang LANG           add language code
  --plot_dir PLOT_DIR   add directory for output plots. Default is plots directory in this repository.
  --translations_file TRANSLATIONS_FILE
                        add your own JSON file containing translations. Default is translations.json in this package.
  --output_format OUTPUT_FORMAT
                        add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba,
                        svg, svgz, tif, tiff. Default is png.
  --translate_filenames TRANSLATE_FILENAMES
                        If True output filenames will be in requested language. If False output filenames will be in
                        English. Default is False
```
Example usage, for British English, using untranslated filenames, the default translation file, pdf output format and output directory "/home/user/plots/", one would use the command:
```python3 spectral_types_plot.py --lang=en-gb --output_format=pdf --plot_dir=/home/user/plots/ ```
The code creates one plot for each of the seven spectral types (showing both a line of wavelength vs flux and a band plot showing light and dark patches on the spectrum) and two comparison plots showing all seven spectra (one with a line plot, one with a band plot).
## Credits
Please credit all plots created by this code to IAU OAE/SDSS/Niall Deacon. Some of the characteristics of the plots were inspired by the plots created by the <a href="https://www.sdss4.org/dr17/mastar/">MaStar Stellar Library</a> team.
These plots were generated using Sloan Digital Sky Survey (SDSS) spectroscopic data from the <a href="https://www.sdss4.org/dr17/mastar/">MaStar Stellar Library</a>. More information on the MaStar Stellar Library and SDSS can be found in Yan et al. (in prep), <a href="https://ui.adsabs.harvard.edu/abs/2019ApJ...883..175Y/abstract">Yan et al. (2019)</a> and the <a href="https://ui.adsabs.harvard.edu/abs/2022ApJS..259...35A/abstract"> Abdurro’uf et al. (2021)</a> and <a href="https://ui.adsabs.harvard.edu/abs/2017AJ....154...28B">Blanton et al. (2017)</a>.
<!-- start-translation-credits -->
### Translation credits
###Portuguese-BR
Translator: Eduardo Penteado
<!-- end-translation-credits -->## What this repository does	
This repository creates a series of plots of stellar spectra in multiple languages. 

## How to create plots using this repository
The command to run code from this repository is:
`python3 spectral_types_plot.py`
The following command line options are available:
```-h, --help            show this help message and exit
  --lang LANG           add language code
  --plot_dir PLOT_DIR   add directory for output plots. Default is plots directory in this repository.
  --translations_file TRANSLATIONS_FILE
                        add your own JSON file containing translations. Default is translations.json in this package.
  --output_format OUTPUT_FORMAT
                        add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba,
                        svg, svgz, tif, tiff. Default is png.
  --translate_filenames TRANSLATE_FILENAMES
                        If True output filenames will be in requested language. If False output filenames will be in
                        English. Default is False
```
Example usage, for British English, using untranslated filenames, the default translation file, pdf output format and output directory "/home/user/plots/", one would use the command:
```python3 spectral_types_plot.py --lang=en-gb --output_format=pdf --plot_dir=/home/user/plots/ ```
The code creates one plot for each of the seven spectral types (showing both a line of wavelength vs flux and a band plot showing light and dark patches on the spectrum) and two comparison plots showing all seven spectra (one with a line plot, one with a band plot).
## Credits
Please credit all plots created by this code to IAU OAE/SDSS/Niall Deacon. Some of the characteristics of the plots were inspired by the plots created by the <a href="https://www.sdss4.org/dr17/mastar/">MaStar Stellar Library</a> team.
These plots were generated using Sloan Digital Sky Survey (SDSS) spectroscopic data from the <a href="https://www.sdss4.org/dr17/mastar/">MaStar Stellar Library</a>. More information on the MaStar Stellar Library and SDSS can be found in Yan et al. (in prep), <a href="https://ui.adsabs.harvard.edu/abs/2019ApJ...883..175Y/abstract">Yan et al. (2019)</a> and the <a href="https://ui.adsabs.harvard.edu/abs/2022ApJS..259...35A/abstract"> Abdurro’uf et al. (2021)</a> and <a href="https://ui.adsabs.harvard.edu/abs/2017AJ....154...28B">Blanton et al. (2017)</a>.
<!-- start-translation-credits -->
### Translation credits
Brazilian Portuguese
- Translator: Eduardo Penteado
