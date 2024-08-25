from setuptools import setup

setup(
    name='realsense workshop utils',
    version='0.0.2',    
    description='utils for the workshop',
    url='',
    author='Richard',
    author_email='',
    license='BSD 2-clause',
    packages=['workshop_utils'],
    install_requires=['pyrealsense2',
                      'numpy',
                      'opencv-python'                     
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)
