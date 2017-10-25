@echo off

set timeouts=5 10 15 20 25
set generators=dharma smarty
set runconfig=level-0.json level-1.json level-2.json

( for %%a in (%timeouts%) do (
	( for %%b in (%runconfig%) do (
		( for %%c in (%generators%) do (
			echo python SmartGrazer.py -c -x aborgardt.bwapp/%%b --overwrite smartgrazer.imps.smithy.generator=%%c smartgrazer.imps.webber.timelimit=%%a >> mylog.log
			python SmartGrazer.py -c -x aborgardt.bwapp/%%b --overwrite smartgrazer.imps.smithy.generator=%%c smartgrazer.imps.webber.timelimit=%%a
		))
	))	
)) >> mylog.log