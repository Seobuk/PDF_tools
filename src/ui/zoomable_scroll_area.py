from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt

class ZoomableScrollArea(QScrollArea):
    """Scroll area that supports zooming with the mouse wheel.

    If the Ctrl key is pressed while scrolling, the assigned spin box's value
    will be changed, triggering any connected update logic (e.g. preview
    refresh). Regular scrolling behaviour is preserved otherwise.
    """
    def __init__(self, zoom_spin, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zoom_spin = zoom_spin

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            step = 5
            if delta > 0:
                new_val = min(self._zoom_spin.maximum(), self._zoom_spin.value() + step)
            else:
                new_val = max(self._zoom_spin.minimum(), self._zoom_spin.value() - step)
            self._zoom_spin.setValue(new_val)
            event.accept()
        else:
            super().wheelEvent(event)
