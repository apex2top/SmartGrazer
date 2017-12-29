@echo off

set FILE_LIST=(*.brf *.alg *.acr *.acn *.lof *.lol *.lot *.spl *.run.xml *.bcf *.ind *.ilg *.glo *.idx *.synctex.gz *.toc *.snm *.aux *.out *.nav *.log *.bbl *.blg *.glsdefs *.ist *.glg *.gls)

for %%i in %FILE_LIST% do DEL /F %%i