import bpy
import json
import os

def update_json_with_collision_paths(joint_xyzrpy_in_LocalFrame, collection, output_type, output_folder, output_path, data):
    for link in data["links"]:
        if link['collision'] or link['visual']:
            link_name = link["name"]
            bpy.ops.object.select_all(action='DESELECT')
            obj = bpy.data.objects.get(link_name)
            if obj:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj

                if joint_xyzrpy_in_LocalFrame:
                    temp_location = obj.location.copy()
                    temp_rotation = obj.rotation_euler.copy()
                    obj.location = [0] * 3
                    obj.rotation_euler = [0] * 3
                if output_type == 'glb': #选择输出为glb文件
                    export_path = f"{output_folder}/{link_name}.glb"
                    bpy.ops.export_scene.gltf(filepath=export_path, use_selection=True, export_format="GLB")
                elif output_type == 'obj': #选择输出为obj文件
                    export_path = f"{output_folder}/{link_name}.obj"
                    bpy.ops.wm.obj_export(filepath=export_path, export_selected_objects=Trueobj)
                else: #默认输出为stl文件
                    export_path = f"{output_folder}/{link_name}.stl"
                    bpy.ops.export_mesh.stl(filepath=export_path, use_selection=True)
                link["collision"] = export_path

                if joint_xyzrpy_in_LocalFrame:
                    obj.location = temp_location
                    obj.rotation_euler = temp_rotation

                bpy.ops.object.select_all(action='DESELECT')

                
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

def export_in_WorldFrame(joint_xyzrpy_in_LocalFrame, output_type, output_folder, output_path, data):
    target_collection = bpy.data.collections['Collection']
    update_json_with_collision_paths(joint_xyzrpy_in_LocalFrame, target_collection, output_type, output_folder, output_path, data)

    blend_output_path = output_folder + "/output_blend.blend"
    bpy.ops.wm.save_as_mainfile(filepath=blend_output_path)





