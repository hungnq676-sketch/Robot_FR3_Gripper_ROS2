# Custom 3-finger gripper mesh URDF

This package contains:
- `meshes/gripper_body.stl`: merged fixed base + body mesh.
- `meshes/phalanx_1.stl`: first moving phalanx mesh.
- `meshes/phalanx_2.stl`: second moving phalanx mesh.
- `urdf/fr3_custom_3finger_gripper_mesh.urdf`: standalone mesh URDF.
- `launch/view_custom_gripper_mesh.launch.py`: RViz + joint slider launch.

The supplied STL coordinates are millimeters. The URDF applies mesh scale `0.001 0.001 0.001`.

The reference zero pose matches the supplied `gripper_body_with_fixed_phalanxes_initial.stl`, which was not a calibrated home pose. `custom_gripper_actuation_joint` is the only command joint. The three `finger_X_joint_1` joints mimic it; `finger_X_joint_2` are intentionally independent.

## Install into the FR3 workspace

```bash
cd ~/FR3/src
unzip ~/Downloads/fr3_custom_gripper_description.zip
cd ~/FR3
colcon build --packages-select fr3_custom_gripper_description --symlink-install
source install/setup.bash
ros2 launch fr3_custom_gripper_description view_custom_gripper_mesh.launch.py
```

In RViz:
- Add `RobotModel`.
- Set `Global Options -> Fixed Frame` to `custom_gripper_base_link`.
- Move `custom_gripper_actuation_joint` in the joint-state GUI. It should move all three `joint_1` meshes together.
- The three `joint_2` sliders remain independent.

For the existing FR3 merge workflow, use:
`~/FR3/install/fr3_custom_gripper_description/share/fr3_custom_gripper_description/urdf/fr3_custom_3finger_gripper_mesh.urdf`
as the `--gripper` input to the merge script after building and sourcing. The generated combined URDF must be launched while `~/FR3/install/setup.bash` is sourced so `package://fr3_custom_gripper_description/...` mesh URIs resolve.
