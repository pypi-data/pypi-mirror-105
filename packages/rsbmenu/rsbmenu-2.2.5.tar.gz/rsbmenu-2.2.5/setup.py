from setuptools import setup
from distutils.core import setup
setup(
      name="rsbmenu",
      version="2.2.5",
      description="This is a normal Menu widget",
      author="R.Raja subramanian",
      #url="https://github.com/RRajaSubramanian/Greenviz",
      author_email="rajasubramanian.r1@gmail.com",
      py_modules=["rsbmenu"],
      package_dir={"":"src"},
      #data_files=[("",["shiridi pic rezied.jpeg","bg5.jpg","raja12.jpeg","resized achuth pic.jpeg"])],
      include_package_data=True,
      #install_requires=["tkinter"]
      )

