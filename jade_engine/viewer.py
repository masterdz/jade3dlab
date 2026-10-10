import numpy as np
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from .mesh import LevelData


class GLViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.level_data = None
        self.blocks = []
        self.meshes = {}
        self.objects = []
        self.rotation_x = 20.0
        self.rotation_y = 45.0
        self.zoom = -50.0
        self.pan_x = 0.0
        self.pan_y = 0.0
        self.last_pos = None
        self.show_meshes = True
        self.show_objects = True
        self.show_wireframe = False
        self.bg_color = (0.15, 0.15, 0.18, 1.0)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def initializeGL(self):
        glClearColor(*self.bg_color)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, w / h if h > 0 else 1.0, 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.pan_x, self.pan_y, self.zoom)
        glRotatef(self.rotation_x, 1.0, 0.0, 0.0)
        glRotatef(self.rotation_y, 0.0, 1.0, 0.0)

        if self.show_meshes:
            self._draw_meshes()
        if self.show_objects:
            self._draw_objects()
        if not self.meshes and not self.objects:
            self._draw_blocks()

    def _draw_meshes(self):
        for mesh_id, mesh in self.meshes.items():
            verts = mesh.get('vertices')
            faces = mesh.get('faces')
            if verts is None or len(verts) == 0:
                continue
            if faces is None or len(faces) == 0:
                glDisable(GL_LIGHTING)
                glPointSize(2.0)
                glColor3f(0.5, 0.9, 1.0)
                glBegin(GL_POINTS)
                step = max(1, len(verts) // 20000)
                for v in verts[::step]:
                    glVertex3f(float(v[0]), float(v[1]), float(v[2]))
                glEnd()
                glEnable(GL_LIGHTING)
                continue
            if self.show_wireframe:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                glDisable(GL_LIGHTING)
                glColor3f(0.4, 0.8, 0.4)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                glEnable(GL_LIGHTING)
                glColor3f(0.7, 0.7, 0.7)
            glBegin(GL_TRIANGLES)
            for face in faces:
                for idx in face:
                    if idx < len(verts):
                        v = verts[idx]
                        glVertex3f(float(v[0]), float(v[1]), float(v[2]))
            glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_LIGHTING)

    def _draw_objects(self):
        glDisable(GL_LIGHTING)
        placed = 0
        for n, obj in enumerate(self.objects):
            pos = obj.get('pos')
            if pos is None:
                gx = (n % 8) * 4.0 - 14.0
                gz = (n // 8) * 4.0 - 14.0
                pos = (gx, 0.0, gz)
            else:
                placed += 1
            box = obj.get('box')
            if box is not None:
                (x0, y0, z0), (x1, y1, z1) = box
                cx, cy, cz = pos
                sx = max(abs(x1 - x0) / 2.0, 0.25)
                sy = max(abs(y1 - y0) / 2.0, 0.25)
                sz = max(abs(z1 - z0) / 2.0, 0.25)
            else:
                cx, cy, cz = pos
                sx = sy = sz = 1.0
            glPushMatrix()
            glTranslatef(cx, cy, cz)
            name = obj.get('name', '')
            if 'TEC' in name or 'Trigger' in name:
                glColor4f(0.0, 1.0, 1.0, 0.35)
            elif 'PORTAL' in name.upper():
                glColor4f(0.0, 1.0, 0.0, 0.35)
            elif 'CAM' in name.upper():
                glColor4f(1.0, 0.0, 1.0, 0.5)
            elif 'LUM' in name.upper() or 'Lampe' in name or 'Lanterne' in name:
                glColor4f(1.0, 1.0, 0.0, 0.5)
            else:
                glColor4f(0.5, 0.8, 1.0, 0.3)
            self._draw_box(sx, sy, sz)
            glPopMatrix()
        glEnable(GL_LIGHTING)

    def _draw_blocks(self):
        glDisable(GL_LIGHTING)
        import math as _math
        type_colors = {
            '.wow': (0.3, 0.6, 1.0),
            '.gao': (0.4, 1.0, 0.4),
        }
        n = max(1, len(self.blocks))
        cols = max(1, int(_math.ceil(_math.sqrt(n))))
        for idx, block_info in enumerate(self.blocks):
            type_str = block_info.get('type', '')
            color = type_colors.get(type_str, (0.5, 0.5, 0.5))
            glColor4f(color[0], color[1], color[2], 0.3)
            size = max(0.5, _math.log10(max(block_info.get('size', 100), 10)) - 1.0)
            gx = (idx % cols - cols / 2.0) * 4.0
            gz = (idx // cols - n / cols / 2.0) * 4.0
            glPushMatrix()
            glTranslatef(gx, 0.0, gz)
            self._draw_box(size, size, size)
            glPopMatrix()
        glEnable(GL_LIGHTING)

    def _draw_box(self, sx, sy, sz):
        s = 1.0
        verts = [
            (-s, -s, -s), (-s, -s, s), (-s, s, -s), (-s, s, s),
            (s, -s, -s), (s, -s, s), (s, s, -s), (s, s, s),
        ]
        faces = [
            (0, 1, 3, 2), (4, 5, 7, 6),
            (0, 1, 5, 4), (2, 3, 7, 6),
            (0, 2, 6, 4), (1, 3, 7, 5),
        ]
        glScalef(sx, sy, sz)
        glBegin(GL_QUADS)
        for face in faces:
            for idx in face:
                glVertex3f(*verts[idx])
        glEnd()

    def set_level(self, level_data: LevelData):
        self.level_data = level_data
        self._reset_view()
        self.update()

    def set_blocks(self, blocks, meshes, objects):
        self.blocks = blocks
        self.meshes = meshes
        self.objects = objects
        self._reset_view()
        pts = []
        for o in objects:
            if o.get('pos'):
                pts.append(o['pos'])
            if o.get('box'):
                pts.extend([o['box'][0], o['box'][1]])
        for m in meshes.values():
            v = m.get('vertices')
            if v is not None and len(v):
                pts.append((float(v[:, 0].min()), float(v[:, 1].min()), float(v[:, 2].min())))
                pts.append((float(v[:, 0].max()), float(v[:, 1].max()), float(v[:, 2].max())))
        if pts:
            import numpy as _np
            a = _np.array(pts, dtype=float)
            lo, hi = a.min(axis=0), a.max(axis=0)
            center, size = (lo + hi) / 2, float((hi - lo).max())
            self.pan_x, self.pan_y = float(-center[0]), float(-center[1])
            self.zoom = -max(size * 1.2, 10.0)
        self.update()

    def _reset_view(self):
        self.rotation_x = 20.0
        self.rotation_y = 45.0
        self.zoom = -50.0
        self.pan_x = 0.0
        self.pan_y = 0.0

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            return
        dx = event.pos().x() - self.last_pos.x()
        dy = event.pos().y() - self.last_pos.y()
        if event.buttons() & Qt.LeftButton:
            self.rotation_y += dx * 0.5
            self.rotation_x += dy * 0.5
        elif event.buttons() & Qt.MiddleButton:
            self.pan_x += dx * 0.05
            self.pan_y -= dy * 0.05
        self.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.last_pos = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        self.zoom += delta * 0.05
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self._reset_view()
            self.update()
        elif event.key() == Qt.Key_W:
            self.show_wireframe = not self.show_wireframe
            self.update()
        elif event.key() == Qt.Key_M:
            self.show_meshes = not self.show_meshes
            self.update()
        elif event.key() == Qt.Key_O:
            self.show_objects = not self.show_objects
            self.update()
