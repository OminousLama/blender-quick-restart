bl_info = {
    "name": "Restart Blender",
    "blender": (4, 0, 0),
    "category": "System",
    "description": "Restart Blender and automatically open current file.",
    "author": "OminousLama",
    "version": (1, 0),
    "location": "System > Restart Blender",
    "warning": "Make sure all changes are saved.",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
import subprocess
import sys

class SYSTEM_OT_restart_blender(bpy.types.Operator):
    """Restart Blender"""
    bl_idname = "wm.restart_blender"
    bl_label = "Restart Blender"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #region Prep
        blender_exe = bpy.app.binary_path
        file_path = bpy.data.filepath
	#endregion
	#region Cmd logic
        # cmd to restart opening current file if one is open
        restart_cmd = [blender_exe, file_path] if file_path else [blender_exe]

        # platform-specific adjustments
        if sys.platform == "win32":
            # win exept: ensure command runs detached process
            subprocess.Popen(restart_cmd, close_fds=True, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            # unix-like -> no flags are needed
            subprocess.Popen(restart_cmd)

        bpy.ops.wm.quit_blender()
	#endregion
	
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SYSTEM_OT_restart_blender.bl_idname)

def register():
    bpy.utils.register_class(SYSTEM_OT_restart_blender)
    bpy.types.TOPBAR_MT_file.append(menu_func)

def unregister():
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    bpy.utils.unregister_class(SYSTEM_OT_restart_blender)

if __name__ == "__main__":
    register()

