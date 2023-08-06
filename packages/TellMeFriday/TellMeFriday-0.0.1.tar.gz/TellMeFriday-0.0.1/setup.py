from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7'
]
setup(
   name='TellMeFriday',
   version='0.0.1',
   description='A simple tool based on gtts(google text to speech api)',
   long_description=open('README.txt').read(),
   long_description_content_type='text/markdown',
   url='',
   author='C Lokesh Kumar Reddy',
   author_email='lokeshkumarreddy.c@gmail.com',
   license='MIT',
   classifiers=classifiers,
   keywords='calculator',
   packages=find_packages(),
   install_requires=['gtts'] #external packages as dependencies
)
