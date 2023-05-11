for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set WORK_DIR=%%~dpnxJ

echo %WORK_DIR%

@REM conda create -n prefect-env python=3.8
call activate prefect-env
pip install -r requirements.txt
prefect config set PREFECT_API_URL=http://128.110.25.99:4200/api
