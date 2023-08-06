from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README  
setup(
  name = 'TOPSIS-Bhawika-101803532',         
  packages = ['topsis_101803532'],
  version = '0.0.1',      
  license='MIT',        
  description = 'A python package to implement TOPSIS on a given dataset',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'BHAWIKA ARORA',                   
  author_email = 'bbhawika_be18@thapar.edu',  
  url = 'https://github.com/Bhawika16/TOPSIS-Bhawika-101803532',   # Provide either the link to your github or to your website
  install_requires=[          
          "pandas","numpy"
      ],
  include_package_data=True,    
  classifiers=[
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  entry_points={
        "console_scripts": [
            "topsis=topsis_101803532.topsis_bhawi:main",
        ]
    },
)