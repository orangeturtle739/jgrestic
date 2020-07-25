cmake_minimum_required(VERSION 3.16.3)
project(jgrestic VERSION 1.0.0 LANGUAGES NONE)

find_package(Python3 COMPONENTS Interpreter REQUIRED)
find_program(BLACK black REQUIRED)
find_program(FLAKE8 flake8 REQUIRED)
find_program(MYPY mypy REQUIRED)
find_program(ISORT isort REQUIRED)
find_program(RESTIC restic REQUIRED)
find_program(DIRSTAMP dirstamp REQUIRED)

set(SITEDIR lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages)

configure_file(
    ${PROJECT_SOURCE_DIR}/support/run.in
    ${PROJECT_BINARY_DIR}/support/run
    @ONLY
)

file(
    COPY ${PROJECT_BINARY_DIR}/support/run
    DESTINATION ${PROJECT_BINARY_DIR}
    FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
)

configure_file(${PROJECT_SOURCE_DIR}/src/jgrestic/commands.py.in ${PROJECT_SOURCE_DIR}/src/jgrestic/commands.py)

add_custom_target(src_stamp
    ALL
    COMMAND ${DIRSTAMP} ${PROJECT_SOURCE_DIR}/src/jgrestic
    BYPRODUCTS ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
)
add_custom_command(
    COMMAND ${BLACK} --check --diff .
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/black.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/black.stamp
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/src
    DEPENDS ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
)
add_custom_command(
    COMMAND ${ISORT} --check
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/isort.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/isort.stamp
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/src
    DEPENDS ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
)
add_custom_command(
    COMMAND ${FLAKE8} --config=${PROJECT_SOURCE_DIR}/.flake8 .
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/flake8.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/flake8.stamp
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/src
    DEPENDS ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
)
add_custom_command(
    COMMAND ${MYPY} --config-file ${PROJECT_SOURCE_DIR}/.mypy.ini -p ${PROJECT_NAME}
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/mypy.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/mypy.stamp
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/src
    DEPENDS ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
)

add_custom_target(lint
    DEPENDS
        ${PROJECT_SOURCE_DIR}/src/jgrestic.stamp
        ${PROJECT_SOURCE_DIR}/src/black.stamp
        ${PROJECT_SOURCE_DIR}/src/isort.stamp
        ${PROJECT_SOURCE_DIR}/src/flake8.stamp
        ${PROJECT_SOURCE_DIR}/src/mypy.stamp
)

add_custom_command(
    COMMAND
        ${Python3_EXECUTABLE} support/python_install.py --prefix ${PROJECT_BINARY_DIR}/target --python ${Python3_EXECUTABLE} --site-packages-dir ${SITEDIR}
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/install.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/install.stamp
    DEPENDS
        lint
        ${PROJECT_SOURCE_DIR}/setup.py
    BYPRODUCTS
        ${PROJECT_BINARY_DIR}/target
        ${PROJECT_SOURCE_DIR}/dist
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

add_custom_target(build_python
    ALL
    DEPENDS ${PROJECT_SOURCE_DIR}/src/install.stamp
)

add_custom_command(
    COMMAND
        ${Python3_EXECUTABLE} support/python_install.py --prefix ${PROJECT_BINARY_DIR}/target --python ${Python3_EXECUTABLE} --site-packages-dir ${SITEDIR} --develop
    COMMAND touch ${PROJECT_SOURCE_DIR}/src/develop.stamp
    OUTPUT ${PROJECT_SOURCE_DIR}/src/develop.stamp
    DEPENDS
        ${PROJECT_SOURCE_DIR}/setup.py
    BYPRODUCTS
        ${PROJECT_BINARY_DIR}/target
        ${PROJECT_SOURCE_DIR}/dist
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

add_custom_target(develop
    DEPENDS
        ${PROJECT_SOURCE_DIR}/src/develop.stamp
        lint
)

add_custom_target(format
    COMMAND ${BLACK}
    COMMAND ${ISORT} --apply
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/src
)

install(DIRECTORY ${PROJECT_BINARY_DIR}/target/
    DESTINATION ${CMAKE_INSTALL_PREFIX}
    USE_SOURCE_PERMISSIONS
)
