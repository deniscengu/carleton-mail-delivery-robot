from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
   return LaunchDescription([
        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            parameters=[{'channel_type': 'serial',
                         'serial_port': '/dev/ttyUSB0',
                         'serial_baudrate': 115200,
                         'frame_id': 'laser',
                         'inverted': False,
                         'angle_compensate': True}],
            output='screen'
        ),
        Node(
            package='mail-delivery-robot',
            namespace='sensors',
            executable='camera_sensor',
            name='camera_sensor'
        ),
        Node(
           package='mail-delivery-robot',
           namespace='communication',
           executable='music_player',
           name='music_player'
        )
   ])