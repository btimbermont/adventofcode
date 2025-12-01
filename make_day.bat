set "dayNumber=%~1"
set "folderName=day%dayNumber%"
mkdir "%folderName%"
set "dayFile=%folderName%\day%dayNumber%.py"
type nul > "%dayFile%"
set "initFile=%folderName%\__init__.py"
type nul > "%initFile%"
git add *