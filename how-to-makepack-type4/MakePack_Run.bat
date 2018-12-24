set packname=%~n1
set mainpath=%~dp0
subst d: /D
subst d: %packname%
cd %packname%
..\MakePack ..\%packname%.txt
move /Y Pack %mainpath%
subst d: /D
cd %mainpath%
