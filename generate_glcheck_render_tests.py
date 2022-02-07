#!/usr/bin/env python3

#outputs all tests to /auto/generated/render/*.html

from os import mkdir
from os.path import join as pathjoin, exists, abspath
from posixpath import split
from shutil import copytree, rmtree

from nbformat import read

import tests.auto.generate_tests as generate_tests

curDir = abspath(split(abspath(__file__))[0]) # hardcoded directory paths :-(
projectDir = curDir
testSrcDir = pathjoin(projectDir, 'tests', "auto")
buildSrcDir = pathjoin(projectDir, 'build')
generationTargetDir = pathjoin(curDir, 'glcheck-tests', 'render-tests')
dataSrcDir = pathjoin(testSrcDir, 'data')
testStructsSrcDir = pathjoin(projectDir, "tests", "test_structs")
testAssetsDir = pathjoin(generationTargetDir, "assets")
dataAssetDir = pathjoin(generationTargetDir, "data")
structAssetDir = pathjoin(generationTargetDir, "structs")

def replace_refs_to_test_structs(srccode: str) -> str:
    search_term = "../test_structs"
    replace_term = "./structs"
    return srccode.replace(search_term, replace_term, -1)

def preproc_src(string: str) -> str:
    string = replace_refs_to_test_structs(string)
    return string






testsys = generate_tests.TestSystem(projectDir)


if exists(generationTargetDir):
    rmtree(generationTargetDir)

mkdir(generationTargetDir)

copytree(buildSrcDir, testAssetsDir)
copytree(dataSrcDir, dataAssetDir)
copytree(testStructsSrcDir, structAssetDir)




for file in testsys.files:
    for example in file.examples:
        if example.name.find("Users") != -1:
            example.name = example.name[example.name.find("js_"):]
        with open(pathjoin(generationTargetDir, f"{example.name}.html"), "w") as f:
            f.write(
f"""
<html lang="en">
    <head>
        <title>{example.name}</title>
        <script src="./assets/3Dmol.js"></script>         
    </head>
    <body style="margin:0;padding:0">
        {"".join([f"<script>{preproc_src(pre)}</script>" for pre in example.prescripts])}
        {"".join([preproc_src(data) for data in example.datas])}
        {"".join([preproc_src(div) for div in example.divs])}
        {"<div id='gldiv' style='width: 100vw; height: 100vh; position: relative;'></div><script>var viewer=$3Dmol.createViewer($('#gldiv'));</script>" if not example.divs else ""}
        <script>
            var callback = function() {{ window.glcheck_renderDone = true;}};
            {preproc_src(example.script)}
            {"window.glcheck_renderDone = true;" if example.script.find("callback") == -1 else ""}
        </script>        
    </body>
</html>
"""
            )