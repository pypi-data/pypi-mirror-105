#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "correctionlib" for configuration "Release"
set_property(TARGET correctionlib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(correctionlib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/correctionlib/lib/libcorrectionlib.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libcorrectionlib.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS correctionlib )
list(APPEND _IMPORT_CHECK_FILES_FOR_correctionlib "${_IMPORT_PREFIX}/correctionlib/lib/libcorrectionlib.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
