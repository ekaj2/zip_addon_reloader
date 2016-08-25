# ##### BEGIN GPL LICENSE BLOCK ######
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import shutil
import os
import sys
import subprocess

import bpy
from bpy.types import Panel, Operator, Scene
from bpy.props import StringProperty

bl_info = {
    "name": "Zip Addon Reloader",
    "author": "Jake Dube",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "3D View > Tools > Zip Addon Reloader",
    "description": "An addon to reload zip addons.",
    "wiki_url": "",
    "category": "Development",
    }


class ZipAddonReloaderPanel(Panel):
    bl_label = "Zip Addon Reload"
    bl_idname = "3D_VIEW_PT_layout_ZIPADDONRELOAD"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_category = 'Tools'

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.operator("zip_reload.unload_addon", icon="QUESTION")
        layout.operator("zip_reload.install_addon", icon="QUESTION")
        layout.operator("zip_reload.enable_addon", icon="QUESTION")
        layout.prop(scene, "addon_dir")
        layout.prop(scene, "zip_dir")
        layout.prop(scene, "addon_name")


class ZipAddonUnloaderOperator(Operator):
    bl_label = "Unload Addon"
    bl_idname = "zip_reload.unload_addon"
    bl_description = "Unloads addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        zipf = os.path.join(scene.zip_dir, scene.addon_name)
        print(zipf)
        print(scene.addon_dir)
        shutil.make_archive(os.path.join(scene.zip_dir, scene.addon_name), 'zip', scene.addon_dir, scene.addon_name)

        # disable and remove addon
        bpy.ops.wm.addon_disable(module=scene.addon_name)
        bpy.ops.wm.addon_remove(module=scene.addon_name)

        subprocess.Popen([sys.argv[0]])
        bpy.ops.wm.quit_blender()

        return{'FINISHED'}


class ZipAddonLoaderOperator(Operator):
    bl_label = "Install Addon"
    bl_idname = "zip_reload.install_addon"
    bl_description = "Installs addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # install addon from file
        bpy.ops.wm.addon_install('EXEC_DEFAULT', overwrite=True, filepath=os.path.join(scene.zip_dir, scene.addon_name + ".zip"))
        # bpy.ops.wm.addon_install("/Users/Owl/Desktop/maze_gen.zip")

        return {'FINISHED'}


class ZipAddonEnablerOperator(Operator):
    bl_label = "Enable Addon"
    bl_idname = "zip_reload.enable_addon"
    bl_description = "Enables addon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # enable addon
        bpy.ops.wm.addon_enable(module=scene.addon_name)

        return {'FINISHED'}

classes = [ZipAddonReloaderPanel, ZipAddonUnloaderOperator, ZipAddonLoaderOperator, ZipAddonEnablerOperator]


def register():
    for i in classes:
        bpy.utils.register_class(i)

    Scene.zip_dir = StringProperty(name="Zip Directory", default="", subtype='FILE_PATH')
    Scene.addon_dir = StringProperty(name="Addon Directory", default="", subtype='FILE_PATH')
    Scene.addon_name = StringProperty(name="Addon Name", default="")


def unregister():
    for i in classes:
        bpy.utils.unregister_class(i)

    del Scene.zip_dir
    del Scene.addon_dir
    del Scene.addon_name


if __name__ == "__main__":
    register()
