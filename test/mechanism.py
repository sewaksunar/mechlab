from mechlab.visual.stress_export import StressAnimationExporter

exporter = StressAnimationExporter(100, 50, 25)

exporter.export_mp4("stress_rotation.mp4")
# exporter.export_gif("stress_rotation.gif")
