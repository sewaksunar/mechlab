import cairo

WIDTH, HEIGHT = 400, 400

# Create a surface and context
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(1, 1, 1)  # white
ctx.paint()

# Draw square element
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(100, 100, 200, 200)
ctx.stroke()

# Draw stress arrows
ctx.set_source_rgb(0, 0, 1)  # blue for σx
ctx.move_to(300, 200)
ctx.line_to(350, 200)
ctx.stroke()

ctx.set_source_rgb(1, 0, 0)  # red for σy
ctx.move_to(200, 100)
ctx.line_to(200, 50)
ctx.stroke()

ctx.set_source_rgb(0, 0.6, 0)  # green for τxy
ctx.move_to(300, 100)
ctx.line_to(350, 50)
ctx.stroke()

# Save output
surface.write_to_png("stress_element.png")
