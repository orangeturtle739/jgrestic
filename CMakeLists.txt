cmake_minimum_required(VERSION 3.16.3)
project(jgrestic VERSION 0.2.2 LANGUAGES NONE)

find_package(unicmake REQUIRED)

find_program(RESTIC restic REQUIRED)
configure_file(${PROJECT_SOURCE_DIR}/src/jgrestic/commands.py.in ${PROJECT_SOURCE_DIR}/src/jgrestic/commands.py)

configure_file(
    ${PROJECT_SOURCE_DIR}/VERSION.in
    ${PROJECT_SOURCE_DIR}/VERSION
    @ONLY
)

add_custom_command(
    COMMAND touch ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.stamp
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.stamp
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/VERSION ${CMAKE_CURRENT_SOURCE_DIR}/setup.py
    VERBATIM
)

unicmake_python(
    PACKAGE_NAME jgrestic
    SETUP_STAMP ${CMAKE_CURRENT_SOURCE_DIR}/setup.py.stamp
)
