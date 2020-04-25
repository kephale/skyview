from setuptools import setup

setup(
        name='skyview',
        version='0.1',
        description='Python interface for SciView.',
        url='https://github.com/kephale/skyview',
        author='Kyle Harrington, Jan Funke, Caroline Malin-Mayor',
        author_email='kephale@kyleharrington.com',
        license='MIT',
        packages=[
            'skyview'
        ],
        install_requires=[
            "numpy",
            "pyimagej",
            "daisy",
            "zarr"
        ]
)
