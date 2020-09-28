# ***************************************************************************
# *   Copyright (c) 2020 Bjoern Lemp <bl@bplan-gmbh.de>                     *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

__title__ = "FreeCAD FEM constraint body heat source task panel for the document object"
__author__ = "Bjoern Lemp"
__url__ = "http://www.freecadweb.org"

## @package task_constraint_bodyheatsource
#  \ingroup FEM
#  \brief task panel for constraint body heat source object


import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore

from femguiutils import selection_widgets

class _TaskPanel:
    def __init__(self, obj):
        
        self._obj = obj
        
        # geometry selection widget
        self._selectionWidget = selection_widgets.GeometryElementsSelection(
            obj.References,
            ["Solid"]
        )
                
        self.form = [self._selectionWidget]
        
    def accept(self):
        #FreeCAD.Console.PrintMessage("accept()\n")
        
        #FreeCAD.Console.PrintMessage(self._obj.References)
        self._obj.References = self._selectionWidget.references
        #FreeCAD.Console.PrintMessage(self._obj.References)
        self._recompute_and_set_back_all()
        
        
        return True

    def reject(self):
        #FreeCAD.Console.PrintMessage("reject()\n")
        self._recompute_and_set_back_all()
        return True

    def clicked(self, index):
        #FreeCAD.Console.PrintMessage("clicked()\n")
        pass

    def open(self):
        #FreeCAD.Console.PrintMessage("open()\n")
        pass

    def _recompute_and_set_back_all(self):
        doc = FreeCADGui.getDocument(self._obj.Document)
        doc.Document.recompute()
        self._selectionWidget.setback_listobj_visibility()
        if self._selectionWidget.sel_server:
            FreeCADGui.Selection.removeObserver(self._selectionWidget.sel_server)
        doc.resetEdit()

