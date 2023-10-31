<h3>How to create plots using this package</h3>
<p>The command to run code from this package is:</p>
<code>python3 spectral_types_plot.py</code>
<p>The following command line options are available:</p>
<code>-h, --help            show this help message and exit
  --lang LANG           add language code
  --plot_dir PLOT_DIR   add directory for output plots. Default is plots directory in this package.
  --translations_file TRANSLATIONS_FILE
                        add your own JSON file containing translations. Default is translations.json in this package.
  --output_format OUTPUT_FORMAT
                        add the output format for the plots. options: eps, jpg, jpeg, pdf, pgf, png, ps, raw, rgba,
                        svg, svgz, tif, tiff. Default is png.
  --translate_filenames TRANSLATE_FILENAMES
                        If True output filenames will be in requested language. If False output filenames will be in
                        English. Default is False</code>
<p>Example usage, for British English, using untranslated filenames, the default translation file, pdf output format and output directory "/home/user/plots/", one would use the command:</p>
<code>python3 spectral_types_plot.py --lang=en-gb --output_format=pdf --plot_dir=/home/user/plots/ </code>
<p>The package creates one plot for each of the seven spectral types (showing both a line of wavelength vs flux and a band plot showing light and dark patches on the spectrum) and two comparison plots showing all seven spectra (one with a line plot, one with a band plot).</p>
<hr/>
<h3>Credits</h3>
<p>Please credit all plots created by this package to IAU OAE/SDSS/Niall Deacon</p>
<p>These plots were generated using Sloan Digital Sky Survey (SDSS) spectroscopic data from the <a href="https://www.sdss4.org/dr17/mastar/">MaStar Stellar Library</a>. More information on the MaStar Stellar Library and SDSS can be found in Yan et al. (in prep), <a href="https://ui.adsabs.harvard.edu/abs/2019ApJ...883..175Y/abstract">Yan et al. (2019)</a> and the <a href="https://ui.adsabs.harvard.edu/abs/2022ApJS..259...35A/abstract"> Abdurro’uf et al. (2021)</a> and <a href="https://ui.adsabs.harvard.edu/abs/2017AJ....154...28B">Blanton et al. (2017)</a>.</p>

<p>https://github.com/astro4edu/stellar_spectra_plots/blob/main/TRANSLATION-CREDITS.md</p>
<hr/>
<h3>Important Caveats</h3>
<p>All of the spectra plotted have their fluxes normalised so that they all have a maximum of the same value. The line plots with multiple stars plotted together have the normalised spectra of each star offset by differing amounts for ease of comparison. The total flux emitted by a star depends on its temperature and size so while an O-type star appears faint in red light on these plots it will emit much more red light than a faint red star (red dwarf).</p>
