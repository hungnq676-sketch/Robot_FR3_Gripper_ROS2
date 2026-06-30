from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


PACKAGE_NAME = "fr3_with_custom_gripper_description"


def generate_launch_description():
    share = Path(get_package_share_directory(PACKAGE_NAME))
    urdf_path = share / "urdf" / "fairino3_v6_with_custom_gripper.urdf"
    rviz_path = share / "rviz" / "fr3_gripper_preview.rviz"
    robot_description = urdf_path.read_text(encoding="utf-8")

    # Preview uses its own JointState topic, so it does not consume /joint_states
    # from the real FR3 driver, MoveIt, or another RViz test.
    preview_joint_states = "/fr3_gripper_preview/joint_states"

    return LaunchDescription([
        # Explicitly pin the robot base to the RViz world frame.
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="fr3_gripper_preview_world_to_base",
            output="screen",
            arguments=["0", "0", "0", "0", "0", "0", "world", "base_link"],
        ),

        Node(
            package="joint_state_publisher_gui",
            executable="joint_state_publisher_gui",
            name="fr3_gripper_preview_joint_gui",
            output="screen",
            parameters=[{
                "robot_description": robot_description,
                "rate": 50,
                "use_mimic_tags": True,
                "zeros": {
                    "j1": 0.0,
                    "j2": 0.0,
                    "j3": 0.0,
                    "j4": 0.0,
                    "j5": 0.0,
                    "j6": 0.0,
                    "custom_gripper_actuation_joint": -1.0,
                    "custom_gripper_finger_1_joint_2": 0.0,
                    "custom_gripper_finger_2_joint_2": 0.0,
                    "custom_gripper_finger_3_joint_2": 0.0,
                },
            }],
            remappings=[("joint_states", preview_joint_states)],
        ),

        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            name="fr3_gripper_preview_state_publisher",
            output="screen",
            parameters=[{
                "robot_description": robot_description,
                "publish_frequency": 50.0,
            }],
            remappings=[("joint_states", preview_joint_states)],
        ),

        Node(
            package="rviz2",
            executable="rviz2",
            name="fr3_gripper_preview_rviz",
            output="screen",
            arguments=["-d", str(rviz_path)],
        ),
    ])
