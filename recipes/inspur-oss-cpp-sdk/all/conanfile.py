from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, export_conandata_patches, get, apply_conandata_patches
import os

required_conan_version = ">=1.53.0"


class InspurOssCppSdkConan(ConanFile):
    name = "inspur-oss-cpp-sdk"
    description = "浪潮云OSS C++ SDK"
    topics = ("inspur", "oss")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/OpenInspur/inspur-oss-cpp-sdk"
    license = "Apache License"
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("libcurl/[*]")
        self.requires("openssl/[*]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "INSPURCLOUD_OSS_CPP_SDK")
        self.cpp_info.set_property("pkg_config_name", "INSPURCLOUD_OSS_CPP_SDK")
        self.cpp_info.libs = ["inspurcloud-oss-cpp-sdk"]

