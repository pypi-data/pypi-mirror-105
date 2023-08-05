from setuptools import setup

setup(
    name='core_backend_bartab_utils',
    version='0.1.10',
    description='Common utils files used for any python3 BarTab repository',
    url='https://github.com/BarTabPayments/core_backend_bartab_utils',
    author='Cassio Hudson',
    author_email='cassio@bartabapp.co',
    license='BSD 2-clause',
    packages=['bartab_core'],
    install_requires=['mpi4py>=2.0',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
