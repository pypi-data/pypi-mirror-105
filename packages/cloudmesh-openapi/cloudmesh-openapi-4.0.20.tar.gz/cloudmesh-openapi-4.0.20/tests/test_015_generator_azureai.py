###############################################################
# pytest -v --capture=no tests/test_015_generator_azureaiimage.py
# pytest -v  tests/test_015_generator_azureaiimage.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import time
from pprint import pprint

import pytest
import tests.util as util
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING

directory = "./tests/generator-azureai"
filename = "azure-ai-image-function.py"

location = f"{directory}/{filename}"


"cms openapi generate azure_ai_image --filename="./tests/generator-azureai/azure-ai-image-function.py" --all_functions"


@pytest.mark.incremental
class TestGenerator:

    def test_generate(self):
        """
        function to validate paths information
        """
        HEADING()

        Benchmark.Start()
        Shell.run(
            "cms openapi generate azure_ai_image --filename={location} --all_functions")
        Benchmark.Stop()

    def test_read_spec(self):
        """
        function to check if YAML synatx is correct or not
        """
        global spec

        HEADING()
        Benchmark.Start()
        spec = util.readyaml(location)
        keys = spec.keys()

        pprint(spec)
        pprint(keys)
        assert "openapi" in keys
        assert "info" in keys
        assert "servers" in keys
        assert "paths" in keys
        assert "A simple service" in str(spec)


class rest:

    def test_service(self):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()

        server_output = Shell.cms("openapi server start {filename}")
        assert server_output.__contains__("starting server")

        time.sleep(2)
        baseurl = "http://127.0.0.1:8080/cloudmesh"

        curl = f"curl {baseurl}/azure-ai-image-function"

        response = Shell.run(curl)
        assert response.__contains__("200")

        Shell.cms("openapi server stop azure-ai-image-function")
        response = Shell.run(curl)
        fail_message = "Failed to connect to 127.0.0.1 port 80: Connection refuse"
        assert response.__contains__(fail_message)

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
