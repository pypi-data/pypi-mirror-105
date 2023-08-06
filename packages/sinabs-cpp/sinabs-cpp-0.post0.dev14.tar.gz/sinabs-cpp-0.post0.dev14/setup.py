import versioneer
from setuptools import setup
from torch.utils import cpp_extension
import warnings
import os


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # the function that checks compiler compatibility throws a warning even if
    # we're not going to use that compiler at the end, so we silence it.
    if cpp_extension.check_compiler_abi_compatibility("g++"):
        os.environ["CC"] = "g++"
        os.environ["CXX"] = "g++"
    elif cpp_extension.check_compiler_abi_compatibility("clang"):
        os.environ["CC"] = "clang"
        os.environ["CXX"] = "clang"
    elif cpp_extension.check_compiler_abi_compatibility("c++"):
        os.environ["CC"] = "c++"
        os.environ["CXX"] = "c++"
    else:
        pass


setup(
    version=versioneer.get_version(),
    packages=["sinabs", "sinabs.layers", "sinabs.layers.cpp"],
    ext_modules=[
        cpp_extension.CppExtension(
            'sinabs.cpp',
            ['csrc/main.cpp',
             'csrc/lif.cpp',
             'csrc/blif.cpp',
             'csrc/iaf.cpp',
             'csrc/threshold.cpp',
             'csrc/bitshift.cpp']
        )],
    cmdclass={'build_ext': cpp_extension.BuildExtension},
)
