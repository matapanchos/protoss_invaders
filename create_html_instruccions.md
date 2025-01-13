- Prepare support for HTML
  - Import asyncio
  - Add all main loop to an asyncio main function
  - Add an await asyncio.sleep(0) to the main function
  - Exect the main function via asyncio.run(main())
- Añadir paquete pybag
- Abrir una terminal y ejecutar
```
pyinstaller $file_name --clean --onefile --noconsole
```
- Se creara el ejecutable en la carpeta dist
- Añadir a dicha carpeta los recursos usados para el programa
- Al compartir si se desea debe ser mediante un archivo comprimido