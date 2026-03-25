# FPS Arena (Simple 3D)

A tiny 3D 1st-person arena shooter in the browser.

## Controls

- **Arrow Up / Down**: move forward / backward
- **Arrow Left / Right**: turn left / right
- **Space**: shoot (hold to keep firing)
- **Right Click**: shoot
- **R**: restart

## Notes

- Bullets are visible projectiles (you can see enemy shots flying toward you).

## Run locally

Because this is a static site, you just need any local web server (opening the HTML file directly may block module imports).

### Option 1: Python

From the `fps-arena/` folder:

```bash
python -m http.server 5173
```

Then open: http://localhost:5173

### Option 2: Node

```bash
npx serve .
```
