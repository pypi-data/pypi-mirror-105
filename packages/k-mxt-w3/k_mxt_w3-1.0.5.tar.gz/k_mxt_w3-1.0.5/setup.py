import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='k_mxt_w3',
                 version='1.0.5',
                 description='k-mxt and k-mxt-w clustering algorithms',
                 author='Anastasia Stepanova',
                 author_email='stacey.stepanova@gmail.com',
                 url='https://github.com/anstepanova/k_mxt_w',
                 zip_safe=False,
                 include_package_data=True,
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 install_requires=['attrs==21.2.0', 'coverage==5.5', 'iniconfig==1.1.1',
                                   'joblib==1.0.1', 'numpy==1.20.3', 'packaging==20.9',
                                   'pandas==1.2.4', 'plotly==4.8.2', 'pluggy==0.13.1',
                                   'py==1.10.0', 'pyparsing==2.4.7', 'pytest==6.2.4',
                                   'pytest-cov==2.11.1', 'scikit-learn==0.24.2',
                                   'scipy==1.6.3', 'six==1.16.0', 'threadpoolctl==2.1.0',
                                   'toml==0.10.2'],
                 packages=['k_mxt_w3'],
                 python_requires=">=3.9",
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                 ],
                 )
