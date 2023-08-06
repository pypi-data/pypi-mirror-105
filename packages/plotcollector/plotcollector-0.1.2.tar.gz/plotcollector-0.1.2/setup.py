from setuptools import setup, find_packages

VERSION = '0.1.2' 
DESCRIPTION = 'Matplotlib figure viewer GUI'
LONG_DESCRIPTION = 'Matplotlib figure viewer QT5 GUI, provides a single interactive window for all figures with file save capabilities.'
URL = "https://github.com/dacts23/plotcollector/releases/download/plotcollector-0.1.2/plotcollector-0.1.2-py3-none-any.whl"
REPO = "https://github.com/dacts23/plotcollector"
setup(
        name="plotcollector", 
        version=VERSION,
        license="MIT",
        author="David Ávila",
        author_email="dacts_23@hotmail.com",
        url=REPO,
        download_url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data = {"plotcollector": ["plotcollector/data/window.ui"]},
        include_package_data=True,
        install_requires=["PyQt5","matplotlib","python-pptx"],
        keywords=['python', 'plotcollector', "matplotlib", "GUI"],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3"
            
        ]
)