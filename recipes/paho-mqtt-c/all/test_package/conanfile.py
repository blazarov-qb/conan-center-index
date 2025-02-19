from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
import os

class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeDeps", "VirtualRunEnv"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PAHO_MQTT_C_ASYNC"] = self.options["paho-mqtt-c"].asynchronous
        tc.variables["PAHO_MQTT_C_WITH_SSL"] = self.options["paho-mqtt-c"].ssl
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            bin_path = os.path.join(self.cpp.build.bindirs[0], "test_package")
            self.run(bin_path, env="conanrun")
