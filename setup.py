from setuptools import setup

package_name = 'killb6'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='killbot',
    maintainer_email='killbot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'killb6 = killb6.killb6:main',
            'manual = killb6.manual:main',
            'camera_control = killb6.camera_control:main',
            'camera_view = killb6.camera_view:main'
        ],
    },
)
