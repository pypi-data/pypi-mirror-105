from setuptools import setup

setup(
    name='Boris-Ext', #pip install name
    version='1.1',    
    description='Import package for Boris Netsocks',
    url='https://github.com/SerbanL/Boris2/tree/master/PythonScripting/Netsocks.py',
    author='Serban Lepadatu',
    author_email='SLepadatu@uclan.ac.uk',
    license='BSD 2-clause',
    packages=['Boris'], #package name holding .py files.
    install_requires=['mpi4py>=2.0',
                      'numpy','matplotlib','more-itertools'                    
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8',

    ],
)