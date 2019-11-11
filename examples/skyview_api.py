import numpy as np
import random
import skyview as sv


def create_volume(shape, dtype):

    volume = np.ones(shape, dtype=dtype)
    return volume


class SkyViewApplication:

    def __init__(self):

        self.viewer = sv.Viewer()
        self.annotation_texts = {}

    def handle_hover_enter(self, layer, annotation):

        print("Entering hover on annotation", annotation)

        text = layer.add_text(
            "annotation %d" % annotation.id,
            position=annotation.position)

        self.annotation_texts[annotation.id] = text

    def handle_hover_leave(self, layer, annotation):

        print("Leaving hover on annotation", annotation)

        layer.remove(self.annotation_texts[annotation.id])

    def handle_click(self, layer, annotation):

        print("Clicked on", annotation)

        if annotation.radius == 2.0:
            annotation.radius = 5.0
        else:
            annotation.radius = 2.0


if __name__ == "__main__":

    app = SkyViewApplication()

    # add three 3D+t volumes with different resolutions and offsets
    app.viewer.add_volume(
        "ch1",
        create_volume((10, 100, 100), np.float32),
        chunk_shape=(1, 10, 10),
        voxel_size=(1, 1, 1))
    # app.viewer.add_volume(
    #     "ch2",
    #     create_volume((10, 10, 100, 100), np.float32),
    #     chunk_shape=(1, 10, 10, 10),
    #     voxel_size=(1, 10, 1, 1))
    # app.viewer.add_volume(
    #     "ch3",
    #     create_volume((10, 50, 100, 100), np.float32),
    #     chunk_shape=(1, 10, 10, 10),
    #     offset=(0, 50, 0, 0))

    # create an annotation layer
    annotation_layer = app.viewer.add_annotation_layer("random spheres")

    # add spheres to it
    for k in range(10):

        annotation_layer.add_sphere(
            position=(
                k,  # t
                float(random.uniform(-10, 10)),  # z
                float(random.uniform(-10, 10)),  # y
                float(random.uniform(-10, 10))   # x
            ),
            color=(128, k*10, 243),
            radius=2.0
        )

    # register basic callbacks
    annotation_layer.register_callback(
        sv.Events.ON_HOVER_ENTER,
        lambda l, a: app.handle_hover_enter(l, a))
    annotation_layer.register_callback(
        sv.Events.ON_HOVER_LEAVE,
        lambda l, a: app.handle_hover_leave(l, a))
    annotation_layer.register_callback(
        sv.Events.ON_CLICK,
        lambda l, a: app.handle_click(l, a))

    # set initital viewer position
    app.viewer.set_position((5, -50, 50, 50))

    # opens viewer, blocks until closed
    app.viewer.show()
