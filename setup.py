from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='endless_bot',
      version='1.0',
      description='A bot endlessly playing Endless Lake',
      long_description=readme(),
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Scientific/Engineering :: Image Recognition'
      ],
      url='http://github.com/aisouard/endless_bot',
      author='Axel Isouard',
      author_email='axel@isouard.fr',
      license='MIT',
      packages=['endless_bot'],
      install_requires=[
            'appdirs==1.4.3',
            'cefpython3==56.1',
            'pygame==1.9.3',
            'PyOpenGL==3.1.0',
            'numpy==1.12.1+mkl',
            'opencv-python==3.2.0',
            'scikit-learn==0.18.1'
      ],
      zip_safe=False,
      entry_points={
            'console_scripts': ['endless_bot=endless_bot.main:main'],
      },
      test_suite='nose.collector',
      tests_require=['nose'])
