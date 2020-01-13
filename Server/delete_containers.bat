FOR /f "tokens=*" %%i IN ('docker container list -a -q') DO docker container stop %%i
FOR /f "tokens=*" %%i IN ('docker container list -a -q') DO docker container rm %%i