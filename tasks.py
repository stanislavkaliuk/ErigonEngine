from invoke import task
import os
import sys
import shutil
import platform

@task
def clean(c, os=platform.system(), buildType="Debug"):
    shutil.rmtree("projects/{0}".format(os), ignore_errors=True)

@task
def build(c, os=platform.system(), buildType="Debug"):
        c.run("cmake --build projects/{0} -DCMAKE_BUILD_TYPE={1} -j16".format(os, buildType))

@task
def generate(c, os=platform.system(), buildType="Debug", compile=False):
    clean(c, os, buildType)
    c.run("cmake -DCMAKE_BUILD_TYPE={0} . -B projects/{1} -DCMAKE_SYSTEM_NAME={1}".format(buildType, os))
    if compile:
        build(c, os, buildType)