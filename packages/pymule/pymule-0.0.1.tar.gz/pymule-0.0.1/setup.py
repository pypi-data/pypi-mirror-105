import setuptools
from setuptools.command.build_ext import build_ext as _build_ext

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


setuptools.setup(
    name='pymule',  # Replace with your own username
    version='0.0.1',
    license='GPLv3',
    author='Yannick Ulrich for the MMCT',
    author_email='yannick.ulrich@psi.ch',
    description='The McMule analysis framework',
    url='https://gitlab.com/mule-tools/pymule',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: IPython',
        'Framework :: Jupyter',
        'Framework :: Matplotlib',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    cmdclass={'build_ext':build_ext},
    setup_requires=['numpy'],
    install_requires=[
        'scipy>=0.19.0',
        'cycler>=0.10.0',
        'matplotlib>=2.0.2'
    ],
    entry_points={
        'console_scripts': [
            'pymule = pymule.__main__:main'
        ]
    },
    package_data={'pymule': ['submit.sh']},
    include_package_data=True,
    python_requires='>=2.7'
)
