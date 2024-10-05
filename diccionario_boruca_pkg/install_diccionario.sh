#!/bin/bash

# Copy the executable to /usr/local/bin
sudo cp diccionario_boruca /usr/local/bin/diccionario_boruca
sudo chmod +x /usr/local/bin/diccionario_boruca

# Copy the icon to the appropriate icon directory
sudo cp diccionario_icon.svg /usr/local/share/icons/diccionario_icon.svg

# Create the applications directory if it doesn't exist
sudo mkdir -p /usr/local/share/applications/

# Create the .desktop file
echo "[Desktop Entry]
Name=Diccionario Boruca
Comment=Una applicacion de diccionario
Exec=/usr/local/bin/diccionario_boruca
Icon=/usr/local/share/icons/diccionario_icon.svg
Terminal=false
Type=Application
Categories=Utility;Education;" | sudo tee /usr/local/share/applications/diccionario_boruca.desktop

# Set permissions for the .desktop file
sudo chmod +x /usr/local/share/applications/diccionario_boruca.desktop

# Refresh application menu
killall -SIGUSR1 gnome-shell

echo "¡Instalación completa! Ahora puedes ejecutar Diccionario Boruca desde el menú de la aplicación."
