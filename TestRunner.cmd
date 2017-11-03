@echo off

set mypath=%cd%

set timelimit=5 10 15
set generator=dharma
set level=0 1
set repeat=50


for /L %%c in (1,1,%repeat%) do (
	for %%t in (%timelimit%) do (
	
		for %%l in (%level%) do (
			set dir=%mypath%\testrun\aborgardt.bwapp\
			set command=python SmartGrazer.py -c -x aborgardt.bwapp\level-%%l.json --overwrite smartgrazer.imps.smithy.generator=%generator% smartgrazer.imps.webber.timelimit=%%t
			echo "Command: %command% > %dir%level-%%l-%%c.json"
			
			if not exist "%dir%" (
				md "%dir%"
			)
			
			%command% > %dir%level-%%l-%%t-%%c.json 2>&1
		)
	)
)