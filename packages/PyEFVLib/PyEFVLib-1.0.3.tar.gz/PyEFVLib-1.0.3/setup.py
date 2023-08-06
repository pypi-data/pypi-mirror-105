from setuptools import setup

with open("README.md", "r") as f:
	long_description = f.read()

setup(
	name="PyEFVLib",
	version="1.0.3",
	description="A library that facilitates the implementation of the Element-based Finite Volumes Method (EbFVM) to solve partial differential equations (PDEs)",
	py_modules=["Vertex", "OuterFace", "GridData", "InnerFace", "Point", "Shape", "Region", "Facet", "MSHReader", "XDMFReader", "Boundary", "Element", "Grid", "BoundaryConditions", "CsvSaver", "VtuSaver", "VtmSaver", "MeshioSaver", "ProblemData", "Solver", "LinearSystem"],
	package_dir={"": "PyEFVLib"},
	classifiers=[
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	long_description=long_description,
	long_description_content_type="text/markdown",
	install_requires=[
		"numpy ~= 1.19.2",
		"pandas ~= 1.1.2",
		"scipy ~= 1.5.2",
		"meshio ~= 4.3.4",
	],
	url="https://github.com/GustavoExel/PyEFVLib",
	author="Gustavo Exel",
	author_email="gustavoexelgpe@gmail.com",

)