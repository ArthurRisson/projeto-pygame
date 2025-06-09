# pip install cx_freeze
import cx_Freeze
from cx_Freeze import setup, Executable
import sys
import os
executaveis = [ 
               cx_Freeze.Executable(script="main.py", icon="assets/icone.ico") ]
cx_Freeze.setup(
    name = "Sobrevivente no Trânsito",
    options={
        "build_exe":{
            "packages":["pygame"],
            "include_files":["assets"]
        }
    }, executables = executaveis
)

# python setup.py build
# python setup.py bdist_msi
