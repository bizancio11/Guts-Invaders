# Guts Invaders

Juego arcade hecho con **Pygame**: una mezcla estilo Geometry Dash con aviones, enemigos voladores, obstáculos y disparos.

## Instalación

```bash
python -m pip install -r requirements.txt
```

## Ejecutar

```bash
python main.py
```

## Controles

- `ESPACIO`, `W`, `↑` o click: saltar.
- `F` o `J`: disparar.
- `R`: reiniciar después de perder.

## Objetivo

Salta sobre los pinchos, dispara a los enemigos y sobrevive el mayor tiempo posible mientras la velocidad aumenta.

## Usar tus propias imágenes

Crea archivos PNG dentro de la carpeta `assets/` con estos nombres exactos:

- `player.png` para el avión del jugador (`100x70`).
- `enemy_drone.png` para un enemigo (`70x42`).
- `enemy_ship.png` para otro enemigo (`70x42`).
- `spike.png` para el obstáculo del suelo (`54x62`).
- `bullet.png` para el disparo (`24x8`).

No es obligatorio que las imágenes tengan ese tamaño: el juego las escala automáticamente. Si falta un archivo, se usa el dibujo original generado por código.
