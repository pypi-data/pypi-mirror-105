import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="iconGenerate",
  version="0.0.2",
  author="Yukun Shang",
  author_email="ykshang4119@gmail.com",
  description="Generate icon images for iOS projects",
  url="https://github.com/Yukun4119/iconGenerate",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
  entry_points={
        'console_scripts': [
            'iconGenerate=iconGenerate:generateImg'
        ]
    }
)