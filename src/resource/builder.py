
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

class Build:

    @staticmethod
    def flex(*args, direction="row", parent=None) -> QHBoxLayout:
        btn_div = QVBoxLayout(parent) if direction.lower() == "column" else QHBoxLayout(parent)
        for w in args:
            if w == "stretch":
                btn_div.addStretch()
            else:
                btn_div.addWidget(w)
        return btn_div

    @staticmethod
    def widget(widget, object_id=None, text=None,
               placeholder=None, items=None, width=None,
               height=None, parent=None, color=None):
        w = widget(parent)
        if object_id and hasattr(w, "objectName"): w.setObjectName(object_id)
        if text and hasattr(w, "setText"): w.setText(text)
        if placeholder and hasattr(w, "setPlaceholderText"): w.setPlaceholderText(placeholder)
        if items and hasattr(w, "addItems"): w.addItems(items)
        if width and height:
            w.setFixedSize(width, height)
        elif width:
            w.setFixedWidth(width)
        elif height:
            w.setFixedHeight(height)

        return w