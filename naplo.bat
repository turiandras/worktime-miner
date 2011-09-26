REM startup:eventID 12, shutdown:eventID 13
REM sequence: date,event
set count=%1
if "%1"=="" set count=30
wevtutil qe system "/q:*[System [(EventID=12 or EventID=13)]]" /f:text /rd:true /c:%count% | findstr "Event\ ID Date" > data.dat
napl.py
pause