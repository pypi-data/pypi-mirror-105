from setuptools import setup, find_packages
  

with open('README.md') as file:
    long_description = file.read()
long_description = 'A scripts to compute local entropy from DEM tif files.'
requirements = ['argparse', 'matplotlib', 'numpy', 'rasterio', 'scikit-image']
  

setup(
        name ='dem_entropy',
        version ='0.0.3',
        author='Rafael Grimson',
        author_email='rgrimson@gmail.com',
        url='https://github.com/rgrimson/dem_entropy',
        description ='A scripts to compute local entropy from DEM tif files.',
        long_description = long_description,
        #long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points = {'console_scripts': ['clem = dem_entropy.clem:main']},
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='clem entropy dem gis-tools',
        install_requires = requirements
)
