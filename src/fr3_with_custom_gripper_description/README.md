# FR3 + custom gripper preview package

This package is a **clean, standalone RViz preview**. It uses one final static URDF:

```text
base_link -> ... -> wrist3_link -> custom_gripper_base_link
```

The only FR3-to-gripper connection is the fixed joint:

```xml
<joint name="wrist3_to_custom_gripper" type="fixed">
  <parent link="wrist3_link"/>
  <child link="custom_gripper_base_link"/>
  <origin xyz="0 0 0.100000" rpy="0 0 0"/>
</joint>
```

`j1` through `j6` are unchanged FR3 joints. The gripper cannot drive `j6`, because it is a child branch of `wrist3_link`.

## Install

Copy this folder into `~/FR3/src`, then:

```bash
cd ~/FR3
colcon build --packages-select fr3_with_custom_gripper_description --symlink-install
source install/setup.bash
ros2 launch fr3_with_custom_gripper_description view_fr3_gripper_preview.launch.py
```

The preview deliberately publishes manual joint states only on:

```text
/fr3_gripper_preview/joint_states
```

so it will not mix with a real robot driver publishing `/joint_states`.

## Slider meanings

```text
j1..j6                               FR3 arm joints
custom_gripper_actuation_joint       -1.0 = open, +0.9 = close
custom_gripper_finger_X_joint_2      leave at 0 for now
```

RViz starts with the root fixed at `world -> base_link`. Do not run a second `robot_state_publisher` for the same `base_link`, `shoulder_link`, ... frame names at the same time.
