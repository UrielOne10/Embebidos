# Instalacion

## Descargas
- [Espressif IDE](https://docs.espressif.com/projects/espressif-ide/en/latest/downloads.html)

## Pasos
1. Ya en el link de [Espressif IDE](https://docs.espressif.com/projects/espressif-ide/en/latest/downloads.html), seleccionamos:
  <p align="center">
    <img src="recursos/descarga.png" alt="ESP-IDE" width="300">
  </p>
2. Se descomprime el archivo descargado y entrar a la ruta:

  > .\Downloads\Espressif-IDE-4.0.0-win32.win32.x86_64\artifacts\win32\Espressif-IDE

3. Ejecutar como admin:
   
  > espressif-ide.exe

4. Elegir una direccion de *workspace*:
  <p align="center">
    <img src="recursos/directorio.png" alt="workspace" width="300">
  </p>
5. Seleecionamos que si:
  <p align="center">
    <img src="recursos/requerimientos.png" alt="workspace" width="300">
  </p>
6. Creamos nueva instalacion y seleccionamos instalacion facil:
  <p align="center">
    <img src="recursos/facil_instalacion.png" alt="workspace" width="300">
  </p>
7. Nos aseguramos de seleccionar el firmware de IDF:
  <p align="center">
    <img src="recursos/idf.png" alt="workspace" width="300">
  </p>

## Primer proyecto

1. Para la realizacion de un proyecto vamos a *Create a new Espressif IDF project*:
   
  <p align="center">
    <img src="recursos/proyecto.png" alt="workspace" width="300">
  </p>
  
2. Seleccionamos nuestra placa a programar:

  <p align="center">
    <img src="recursos/placa.png" alt="workspace" width="300">
  </p>
  
3. Y por simplicidad del proyecto usaremos los ejemplos que vienen por defecto, *blink* . Y aceptamos:

  <p align="center">
    <img src="recursos/blink.png" alt="workspace" width="300">
  </p>
  
4. Ahora realizamos el *build* del proyecto.
   
5. Cargamos el script a la placa.
   
    1. Buscamos el engrane donde se encuentra la placa a programar (barra de herramientas superior):
       
        <p align="center">
          <img src="recursos/engrane.png" alt="workspace" width="300">
        </p>
        
    2. Declaramos el puerto donde se encuentra la placa.
       
        <p align="center">
          <img src="recursos/puerto.png" alt="workspace" width="300">
        </p>
      
